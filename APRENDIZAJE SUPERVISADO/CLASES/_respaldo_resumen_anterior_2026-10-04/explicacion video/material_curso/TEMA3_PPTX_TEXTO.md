# Texto extraído del PowerPoint del tema 3

Consulta el PPTX original para gráficos, fórmulas y distribución visual. Este archivo solo facilita buscar texto.

## Diapositiva 1

A PRENDIZAJE  S UPERVISADO José Gabriel García Pardo josegabriel.garciap@campusviu.es Tema 3 – Extracción de características 05MIAR

## Diapositiva 2

Índice Estadísticos unidimensionales 1.1. Conceptos básicos 1.2. Variables 1.3. Análisis de variables cualitativas 1.4. Análisis de variables cuantitativas Características bidimensionales 2.1. Introducción a los datos 2D 2.2. Procesado de imagen 2.3. Segmentación de imágenes 2.4. Descriptores de forma 2.5. Descriptores de textura

## Diapositiva 3

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 1. Estadísticos unidimensionales 3 1.1. Conceptos básicos Población –  Es el conjunto de ítems (instancias, ocurrencias, individuos, sujetos, elementos, filas, etc.) que se desea estudiar, analizar o sobre el que se quiere extraer una serie de conclusiones. Por ejemplo: Todos los lotes de un producto que se va a fabricar en masa mediante un determinado proceso industrial.  Muestra –  Corresponde a cualquier subconjunto de la población. Es de vital importancia que la muestra sea representativa de la población. Para conseguirlo, se aplica un proceso llamado  muestreo aleatorio .   El objetivo es llegar a conocer a la población partiendo del análisis de una muestra.  Inferencia estadística –  Proceso de razonamiento por el que se obtienen conclusiones (con un margen de error conocido) sobre la población, a partir del análisis realizado sobre el conjunto de muestra.  muestreo Población muestra análisis Conclusiones Inferencia estadística 2. Características bidimensionales

## Diapositiva 4

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 4 Intención de voto ante unas Elecciones Generales en España. Población    Número total de personas mayores de 18 años empadronadas en España.  Muestra representativa   Subconjunto balanceado de hombres y mujeres de diferente edad y distinta localización geográfica. Ejemplos de muestreos erróneos Población Muestra Complicaciones de un determinado fármaco contra el Covid-19 Población    Número total de personas en el mundo.  Muestra representativa   Subconjunto balanceado de hombres y mujeres de diferentes edades y con diferentes complexiones, hábitos, afecciones, etc. Calidad de los ingredientes de una tarta.  Población    La tarta.  Muestra    Una porción de la tarta que contenga un trozo de cada uno de los ingredientes.  fresa nata chocolate fresa nata chocolate 1.1. Conceptos básicos 1. Estadísticos unidimensionales 2. Características bidimensionales

## Diapositiva 5

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 5 Una  variable estadística  es cada una de las cualidades que poseen los individuos de una población. Es decir, una variable hace referencia al valor que toma una instancia (ítem, ocurrencia, observación, sujeto, fila, etc.) para una determinada característica (propiedad, atributo, columna, etc.). Dicho valor, como su propio nombre indica, puede variar en función del momento y/o del ítem en cuestión.  Las  variables nominales  son aquellas basadas en modalidades no numéricas que no admiten criterio de orden.  Las  variables discretas  son aquellas que solo pueden tomar un número finito de valores, es decir, son contables.  Las  variables continuas  son aquellas que pueden asumir un número infinito de valores en un rango continuo. Las  variables ordinales  son aquellas cualidades no numéricas en las que existen un criterio de orden.  1.2. Variables 1. Estadísticos unidimensionales 2. Características bidimensionales

## Diapositiva 6

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 6 El sexo de una persona El estado civil de una persona Variables cualitativas nominales Puesto conseguido en deporte Satisfacción del cliente Variables cualitativas ordinales El número de hijos El número de empleados Variables cuantitativas discretas La estatura El peso Variables cuantitativas continuas 1.2. Variables 1. Estadísticos unidimensionales 2. Características bidimensionales

## Diapositiva 7

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 7 Tablas de frecuencia Las  tablas de frecuencia  permiten resumir una muestra de datos cualitativos para facilitar su comprensión. De esta manera, se puede analizar la muestra de una población de manera organizada sin necesidad de recurrir a la muestra entera.  Ejemplo: Se pretende conocer cuál es el nivel educativo en Valencia entre las personas de 30 y 40 años.  Para ello, se selecciona una muestra representativa de K=500 individuos empadronados en Valencia y que, al menos, acabaron sus estudios de secundaria.  Tabla de frecuencia 1.3. Análisis de variables cualitativas 1. Estadísticos unidimensionales 2. Características bidimensionales

## Diapositiva 8

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 8 Representación de los datos 1.3. Análisis de variables cualitativas 1. Estadísticos unidimensionales 2. Características bidimensionales

## Diapositiva 9

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 9 Medidas de tendencia central 1.4. Análisis de variables cuantitativas 1. Estadísticos unidimensionales 2. Características bidimensionales Media 𝑥 = 1 𝑁 𝑖 =1 𝑁 𝑥 𝑖   Mediana Si N es impar,    Si N es par,    𝑋  es el valor en la posición  𝑁 2   𝑋 = 1 2 ( 𝑋 𝑁 2 + 𝑋 𝑁 2 +1 )   Moda Corresponde al valor más repetido del conjunto de datos  𝑋     Medidas de posición

## Diapositiva 10

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 10 Medidas de dispersión 1.4. Análisis de variables cuantitativas 1. Estadísticos unidimensionales 2. Características bidimensionales 𝜎 = 𝑖 =1 𝑁 ( 𝑥 𝑖 − 𝑥 ) 2 𝑁   Desviación típica Varianza  𝜎 2 = 𝑖 =1 𝑁 ( 𝑥 𝑖 − 𝑥 ) 2 𝑁   𝐴 = 𝑖 =1 𝑁 ( 𝑥 𝑖 − 𝑥 ) 3 𝑁 · 𝜎 3   Coeficiente de asimetría  Medidas de distribución Mide la simetría de la distribución de una variable respecto a la media aritmética. Curtosis 𝐾 = 𝑖 =1 𝑁 ( 𝑥 𝑖 − 𝑥 ) 4 𝑁 · 𝜎 4 −3   Mide el grado de apuntamiento o achatamiento de la distribución de frecuencia, respecto a una distribución normal  K>0 K=0 K<0

## Diapositiva 11

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 11 2.1. Introducción a los datos 2D 1. Estadísticos unidimensionales 2. Características bidimensionales Una  imagen   es una función bidimensional  f( x,y )  donde  x  e  y  representan las coordenadas espaciales y el valor de  f,  la intensidad de la imagen en dicho punto.  256 256

## Diapositiva 12

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 12 2.1. Introducción a los datos 2D 1. Estadísticos unidimensionales 2. Características bidimensionales 256 256 3

## Diapositiva 13

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 13 2.1. Introducción a los datos 2D 1. Estadísticos unidimensionales 2. Características bidimensionales R G B 239 151 147 (130, 155)

## Diapositiva 14

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 14 2.2. Procesado de imagen 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.1. Transformaciones de intensidad Cambio de brillo  Original – 50  Original + 50  Original

## Diapositiva 15

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 15 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.1. Transformaciones de intensidad Cambio de contraste  Original Original + 50  Original – 50  2.2. Procesado de imagen

## Diapositiva 16

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 16 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.1. Transformaciones de intensidad Transformación lineal a tramos Cambio de linealidad Negativo Ajuste del histograma Ecualización del histograma 2.2. Procesado de imagen

## Diapositiva 17

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 17 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.2. Conversiones del espacio de color RGB to CMYK Original C M Y K 2.2. Procesado de imagen

## Diapositiva 18

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 18 1. Estadísticos unidimensionales 2. Características bidimensionales https:// docs.opencv.org /3.4/d8/d01/ group __ imgproc __color__ conversions.html 2.2.2. Conversiones del espacio de color 2.2. Procesado de imagen

## Diapositiva 19

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 19 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.3. Transformaciones geométricas Traslación Una  traslación  es el desplazamiento de la posición de un objeto manteniendo las dimensiones de la imagen original. Si se conoce la magnitud del desplazamiento  ( 𝑡 𝑥 ,  𝑡 𝑦 )  en las direcciones  x  e  y , respectivamente,  se puede escribir la matriz de transformación  M  como:   2.2. Procesado de imagen

## Diapositiva 20

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 20 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.3. Transformaciones geométricas Cropping El  cropping  consiste en la selección y extracción de una determinada zona de la imagen que consideraremos como región de interés (ROI,  del inglés –  region  of  interest )  para centrar los algoritmos únicamente en esa parte específica. Esto es muy interesante cuando queremos extraer características únicamente de una región concreta y el resto de la imagen puede no nos interesa o introduce ruido.  2.2. Procesado de imagen

## Diapositiva 21

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 21 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.3. Transformaciones geométricas Rotación La  rotación  de una imagen consiste en aplicar un determinado ángulo  𝜃  a una matriz de rotación  M .  OpenCV  permite además  personalizar más la rotación  multiplicando por un factor de escala y modificando el centro de rotación.    2.2. Procesado de imagen

## Diapositiva 22

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 22 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.3. Transformaciones geométricas Perspectiva La  transformación de perspectiva  consiste en la rotación de la superficie de proyección (superficie de perspectiva) en un cierto ángulo alrededor  𝜃 . La idea de la transformación de perspectiva es: dada una imagen en el plano 2D, colocarla en una posición cualquiera del espacio 3D y después proyectarla sobre el plano de imagen Z=1.    Original Perspectiva Cropping 2.2. Procesado de imagen

## Diapositiva 23

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 23 1. Estadísticos unidimensionales 2. Características bidimensionales 2.2.3. Transformaciones geométricas Flipping Las técnicas de  flipping  permiten voltear la imagen de diversas maneras para obtener la posición más conveniente a la hora de resolver un problema. Este método puede ser útil cuando las imágenes de una base de datos están adquiridas de manera diferente y es necesario establecer una posición estándar para poder extraer características uniformes.  Original Flip  horizontal Flip  vertical Flip   hor . +  vert . 2.2. Procesado de imagen

## Diapositiva 24

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 24 2.3. Segmentación de imágenes 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3.1. Introducción Normalmente, para extraer características basadas en  descriptores de forma , es necesario, previamente, llevar a cabo alguna técnica de segmentación que permita delimitar la región de interés que se desea analizar.  Los  algoritmos de segmentación  se basan en particionar la imagen digital en diferentes segmentos (objetos) para simplificar la representación de la imagen y facilitar la comprensión de su contenido.  Las técnicas de segmentación permiten  asignar una etiqueta a cada píxel  de la imagen de manera que los píxeles con la misma etiqueta comparten características similares.  Existen dos tipos de segmentación: Segmentación semántica . Consiste en un problema de clasificación a nivel de píxel que permite asignar una etiqueta de objeto a cada píxel para delimitar regiones de interés. Por ejemplo, diferenciar un grupo de personas del fondo de la imagen.  Segmentación de instancia.  Consiste en una tarea más compleja que implica llevar a cabo una detección de objetos para asignar una etiqueta de instancia a cada objeto. Es decir, la segmentación de instancia permite identificar objetos que comparten las mismas propiedades como objetos independientes. Por ejemplo, diferenciar cada persona de un grupo de personas en una imagen.

## Diapositiva 25

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 25 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3.1. Introducción Detección de objetos Segmentación semántica Segmentación de instancia 2.3. Segmentación de imágenes

## Diapositiva 26

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 26 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3.2. Aplicaciones Sistemas de ayuda al diagnóstico mediante análisis de imágenes médicas . Por ejemplo: resonancia magnética, TAC, imagen histológica, imágenes de fondo de ojo, radiografías, ultrasonido, etc.  Reconocimiento de objetos.  Por ejemplo, detección de peatones, localización de objetos en imágenes por satélite (carreteras, bosques, cultivos, etc.) Reconocimiento de patrones en temas de seguridad . Por ejemplo, reconocimiento de caras  ( face   recognition ),  reconocimiento de huellas dactilares ( fingerprint   recognition )  o reconocimiento del iris.  Sistemas de control de tráfico y conducción autónoma.  Por ejemplo, detección de señales de tráfico, reconocimiento de matrículas,  self   driving .  2.3. Segmentación de imágenes

## Diapositiva 27

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 27 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3.3. Técnicas Métodos de  umbralización  ( thresholding ) Métodos de agrupación  ( clustering ) Detección de bordes Crecimiento de regiones  ( región  growing ) Watershed   Autoencoders   (Redes Neuronales Convolucionales) Métodos basados en el espacio de color 2.3. Segmentación de imágenes

## Diapositiva 28

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 28 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3. Segmentación de imágenes 2.3.3. Técnicas Thresholding  para  binarizar Original Imagen de grises Histograma Máscara Conversión a escala de grises Cálculo del histograma Umbralización MÉTODO DE OTSU

## Diapositiva 29

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 29 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3. Segmentación de imágenes 2.3.3. Técnicas Thresholding  para  binarizar  -  Otsu El  método de  Otsu  es un procedimiento no paramétrico que permite obtener el umbral óptimo maximizando la varianza entre clases. Búsqueda exhaustiva.  Algoritmo.  Se parte de una imagen con  N  píxeles que puede tomar  L  valores de grises diferentes   𝑐 1 = 0,1,2,..,  𝑡   𝑐 2 = 𝑡 +1,  𝑡 +2, …,  𝐿   𝑡 =50   𝑐 1   𝑐 2   𝐿 =256   1.  Los píxeles se dividen en dos clases 2.  Se define la probabilidad del nivel de gris  i 𝑝 𝑖 = 𝑓 𝑖 𝑁 ,   siendo  𝑓 𝑖  la frecuencia de repetición del nivel de gris  i     3.  Se calculan las medias para cada una de las clases  𝜇 1 = 𝑖 =1 𝑡 𝑖 · 𝑝 𝑖 𝜔 1 ( 𝑡 )   𝜇 2 = 𝑖 = 𝑡 +1 𝐿 𝑖 · 𝑝 𝑖 𝜔 2 ( 𝑡 )   𝜔 1 𝑡 = 𝑖 =1 𝑡 𝑝 𝑖   donde 𝜔 2 𝑡 = 𝑖 = 𝑡 +1 𝐿 𝑝 𝑖   5.  Se calcula la varianza entre clases 𝜎 2 = 𝜔 1 𝜇 1 − 𝜇 𝑇 2 + 𝜔 2 𝜇 2 − 𝜇 𝑇 2   4.  Se obtiene la intensidad media total de la imagen 𝜇 𝑇 = 𝜔 1 · 𝜇 1 + 𝜔 2 · 𝜇 2   6.  Se selecciona como el umbral óptimo aquel que maximiza la varianza 𝑡 ∗ = 𝑀𝑎𝑥 { 𝜎 2 𝑡 }

## Diapositiva 30

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 30 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3. Segmentación de imágenes 2.3.3. Técnicas Espacios de color Original Extraer el canal de interés Cálculo del histograma Umbralización Histograma Segmentación ROI Canal Rojo

## Diapositiva 31

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 31 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3. Segmentación de imágenes 2.3.3. Técnicas Detección de bordes Original Detección de bordes Rellenar con 0s Bordes de imagen Máscara Filtro gaussiano para reducir ruido Imagen filtrada MÉTODO DE CANNY Cuando hablamos de  bordes de una imagen , hablamos de los píxeles donde hay un  cambio de intensidad .

## Diapositiva 32

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 32 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3. Segmentación de imágenes 2.3.3. Técnicas Detección de bordes  -   Canny 1. Detector de bordes con Sobel El  operador  Sobel   se basa en el  cálculo de la primera derivada  para obtener el  gradiente de la intensidad  de una imagen en cada píxel. Es decir,  mide   cambios de intensidad en la imagen . Para ello, aplica  dos  máscaras de convoluciones  con  kernels  de 3x3 elementos , uno para los  cambios horizontales  y otro para los  verticales . De esta manera, se obtienen  𝑮 𝒙  y  𝑮 𝒚   que representan  las aproximaciones de las derivadas de intensidades.    En cada píxel de la imagen,  se combinan las aproximaciones de las derivadas  para obtener la  magnitud   𝑮  y la  dirección  𝚯   del  gradiente . La dirección de los píxeles puede ser en estos ángulos (0, 45, 90, o 135)   2. Filtrado de bordes mediante la supresión non-máximum  Esta técnica permite  adelgazar los bordes  basándose en el  gradiente . El objetivo  es eliminar los píxeles  que  no corresponden a un borde . Se  compara  el valor de intensidad de  cada píxel con  el valor de intensidad de los  píxeles vecinos en la dirección del gradiente . Si es  mayor , ese píxel se considera  borde . 3.  Umbralización  por histéresis El umbral por histéresis se centra en establecer  dos umbrales (uno máximo y otro mínimo) .  Si el valor del píxel es  mayor   que  el  umbral máximo , el píxel se considera parte del  borde . Si el valor del píxel es  menor que  el  umbral mínimo , el píxel  no  se considera parte del  borde . Si el valor del píxel está  entre el mínimo y el máximo umbral , será  borde si está conectado a  un píxel que sí es parte del  borde .

## Diapositiva 33

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 33 1. Estadísticos unidimensionales 2. Características bidimensionales 2.3. Segmentación de imágenes 2.3.3. Técnicas Métodos de  umbralización  ( thresholding ) Métodos de agrupación  ( clustering ) Detección de bordes Crecimiento de regiones ( región  growing ) Watershed   Autoencoders  (Redes Neuronales Convolucionales) Métodos basados en el espacio de color

## Diapositiva 34

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 34 2.4. Descriptores de forma 1. Estadísticos unidimensionales 2. Características bidimensionales Los  descriptores geométricos  analizan la forma estructural de  objetos binarios  y sus  contornos. Se pueden utilizar para  identificar objetos  y  reconocer patrones  en una imagen.  2.4.1. Descriptores geométricos Algunos ejemplos son: Área    Mide el número de píxeles que contiene la región de interés. Bounding  box ( bbox )  Consiste en el rectángulo más pequeño capaz de albergar la región de interés (rectángulo rojo).  Área de la  bbox    Número de píxeles que contiene la  bounding  box.  Convex   hull   image    Consiste en el polígono convexo más pequeño capaz de albergar la región de interés (polígono  cyan ).  Área de la  convex   image     Mide el número de píxeles dentro de la  convex   image . Excentricidad   Es la relación de la distancia entre los focos de la elipse y su longitud del eje principal. Una elipse con excentricidad=0 es un círculo, mientras que una excentricidad =1 denota un segmento de línea.  Diámetro equivalente   Consiste en el diámetro de un círculo cuya área sea la misma que la región de interés

## Diapositiva 35

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 35 2.4. Descriptores de forma 1. Estadísticos unidimensionales 2. Características bidimensionales 2.4.1. Descriptores geométricos Extensión    Se define como el ratio de píxeles en la región con respecto al número total de píxeles contenidos en la  bounding  box.  Longitud del eje mayor   Se refiere a la longitud del eje mayor de una elipse que tiene el mismo segundo momento central normalizado que la región. Longitud del eje menor   Igual para el eje menor de la elipse. Orientación   Es el ángulo que forma la elipse anterior con respecto al eje horizontal. El valor se expresa en grados en un rango de [-90, 90]. Perímetro   Se define como el número de píxeles que forman parte del contorno del objeto de interés.  Solidez   Corresponde con la proporción de píxeles que contiene el área respecto a la  convex   hull   image . En el caso de polígonos regulares, su valor será 1.  A partir de estos descriptores se podrían extraer otros de interés como: Compacidad    Mide la circularidad del objeto. Se calcula como el cociente entre el área y el perímetro al cuadrado.  Diámetro de  Feret    Se define como el cociente entre el área del objeto y la  bounding  box.

## Diapositiva 36

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.1. Matriz de coocurrencias  La  matriz de coocurrencias  mide la frecuencia en la que un píxel con nivel de intensidad  i  es adyacente de un píxel con nivel de intensidad  j.  La adyacencia se define a través de un  número de píxeles vecinos  d   y una  orientación (ángulo,  𝜶 ) .  A partir de estos valores, es posible extraer diferentes características como: el  contraste , la  correlación , la  disimilitud , la  homogeneidad , la  energía  y la  segundo momento angular .    1 2 3 4 5 6 7 8 1 1 3 0 0 1 0 0 0 2 0 0 0 1 0 0 1 0 3 1 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 2 5 0 0 0 0 0 1 0 0 6 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 8 1 0 0 0 0 0 0 0 1 1 5 6 3 1 2 7 4 8 1 2 1 2 4 8 𝛼  = 0º d = 1   Imagen Matriz de coocurrencias 8x8 35

## Diapositiva 37

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.1. Matriz de coocurrencias  37

## Diapositiva 38

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.2.  Scale-Invariant   Feature   Transform  (SIFT) El  algoritmo SIFT  se utiliza en aplicaciones que involucran un escalado de la imagen. Sirve para la detección de esquinas, bordes o texturas, siendo estable frente a perturbaciones y transformaciones que pueda sufrir la imagen. Es invariante a posición, escala, rotación, iluminación y contraste. El algoritmo consta de las siguientes fases: Detección de extremos en la escala-espacio . La escala-espacio se crea aplicando convoluciones entre la imagen original ( I)  y un  kernel  gaussiano ( G ) con diferentes escalas ( 𝜎 ). 𝐿 𝑥 , 𝑦 , 𝜎 = 𝐺 𝑥 , 𝑦 , 𝜎 ∗ 𝐼 𝑥 , 𝑦 ,      𝐺 𝑥 , 𝑦 , 𝜎 = 1 2 𝜋 𝜎 2 𝑒 − 𝑥 2 + 𝑦 2 /2 𝜎 2 Todas las imágenes ( 𝐿 ) generadas forman una “octave”. Este proceso se repite para obtener varias “octaves”, donde el tamaño de cada una de ellas es la mitad de la anterior.    38 𝑂𝑐𝑡𝑎𝑣𝑒  1   𝑂𝑐𝑡𝑎𝑣𝑒  2   𝑂𝑐𝑡𝑎𝑣𝑒  3   𝑂𝑐𝑡𝑎𝑣𝑒  4

## Diapositiva 39

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.2.  Scale-Invariant   Feature   Transform  (SIFT) 2.     Diferencia de Gaussianas (DOG).  Se genera un set de imágenes basado en la diferencia de las imágenes tras ser  convolucionadas  con el  kernel  gaussiano. Estas diferencias de gaussianas son muy buenas para encontrar puntos de interés en las imágenes. El procedimiento se aplica para todas las octaves como la diferencia entre una imagen con dos escalas diferentes, por ejemplo,  𝜎   y  k 𝜎 .   𝑂𝑐𝑡𝑎𝑣𝑒  1   3.     Detección de posibles puntos de interés.  Cada píxel de una imagen es comparada con los 8 píxeles vecinos de esa misma imagen, y con los 9 píxeles (en esa misma posición) en las escalas directamente posterior y anterior. Si el valor del píxel es un extremo local (mayor o menor intensidad), ese píxel se convierte en un posible punto de interés.  𝑂𝑐𝑡𝑎𝑣𝑒  1   39

## Diapositiva 40

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 40 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.2.  Scale-Invariant   Feature   Transform  (SIFT) 4.     Localización de puntos de interés.  El punto anterior genera muchos posibles puntos de interés, por lo que en este paso hay que quedarse únicamente con los que son útiles. Se aplican series de Tylor (segundo orden) sobre cada posible punto de interés para lidiar con los  keypoints  de bajo contraste. Si la intensidad es menor que un determinado umbral (0.03), se rechaza. Además, la Diferencia de  Gausianas  ( DoG ) presenta una alta respuesta para bordes, por lo que muchos  keypoints  se detectan cerca de los bordes. No obstante, tenemos que eliminar aquellos que no sean robustos al ruido. Para ello, se utiliza la “ Hessian   matrix  (H)” de 2x2 que permite obtener la curvatura principal.  5.       Asignación de la orientación.  Una vez ya tenemos localizados los  keypoints  estables frente a cambios de escala, bajo contraste y ruido, asignamos una orientación a cada punto de interés para hacerlo invariante a las rotaciones. Se selecciona un vecindario alrededor de un punto de interés y se calcula la magnitud y la dirección del gradiente.  La  orientación  se calcula mediante un histograma de 36  bins  que cubre los 360 grados. Si por ejemplo la dirección del gradiente en un punto es 57.17 grados, esto corresponde al  bin  50-59 del histograma. La cantidad que se añade a dicho  bin  es la  magnitud  del gradiente, por ejemplo, 16.64. Tras hacer esto con todos los píxeles del vecindario del punto de interés, el histograma tendrá un pico en cada punto. El valor más alto del histograma y aquellos picos mayores del 80% se tienen en cuenta para calcular la orientación. Esto crea puntos de interés con la misma localización y escala, pero diferentes direcciones.  𝐺𝑥 =55−46=9 Gy = 56   −  42 = 14   𝑀𝑎𝑔𝑛𝑖𝑡𝑢𝑑 = 𝐺 =16.64   𝐷𝑖𝑟𝑒𝑐𝑐𝑖 ó 𝑛 = Θ =57.17

## Diapositiva 41

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 41 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.2.  Scale-Invariant   Feature   Transform  (SIFT) 4.     Localización de puntos de interés.  El punto anterior genera muchos posibles puntos de interés, por lo que en este paso hay que quedarse únicamente con los que son útiles. Se aplican series de Tylor (segundo orden) sobre cada posible punto de interés para lidiar con los  keypoints  de bajo contraste. Si la intensidad es menor que un determinado umbral (0.03), se rechaza. Además, la Diferencia de  Gausianas  ( DoG ) presenta una alta respuesta para bordes, por lo que muchos  keypoints  se detectan cerca de los borde. No obstante, tenemos que eliminar aquellos que no sean robustos al ruido. Para ello, se utiliza la “ Hessian   matrix  (H)” de 2x2 que permite obtener la curvatura principal.  5.       Asignación de la orientación.  Una vez ya tenemos localizados los  keypoints  estables frente a cambios de escala, bajo contraste y ruido, asignamos una orientación a cada punto de interés para hacerlo invariante a las rotaciones. Se selecciona un vecindario alrededor de un punto de interés y se calcula la magnitud y la dirección del gradiente.  La  orientación  se calcula mediante un histograma de 36  bins  que cubre los 360 grados. Si por ejemplo la dirección del gradiente en un punto es 57.17 grados, esto corresponde al  bin  50-59 del histograma. La cantidad que se añade a dicho  bin  es la  magnitud  del gradiente, por ejemplo, 16.64. Tras hacer esto con todos los píxeles del vecindario del punto de interés, el histograma tendrá un pico en cada punto. El valor más alto del histograma y aquellos picos mayores del 80% se tienen en cuenta para calcular la orientación. Esto crea puntos de interés con la misma localización y escala, pero diferentes direcciones.

## Diapositiva 42

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 42 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.2.  Scale-Invariant   Feature   Transform  (SIFT) 6.     Descriptor del punto de interés.  Una vez cada punto de interés tiene su localización, escala y orientación, es momento de calcular el descriptor que permite identificar un mismo punto en una imagen transformada a partir de la original. Para ello, se coge una ventana de 16x16 alrededor del punto de interés. Dicha ventana se divide en bloques de 4x4 y para cada bloque, se calculan la magnitud y las orientaciones de los píxeles obteniendo un histograma de orientación de 8  bins . De esta manera, se obtienen 16 histogramas de 8  bins , dando lugar a un  figerprint  de 128 características.   Ventana de 16x16 keypoint bloque Descriptor de 128 características

## Diapositiva 43

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 43 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.3.  Speeded -Up  Robust   Features  (SURF) 1.   Cálculo de la matriz Hessiana.  A diferencia de SIFT, que se basaba en el cálculo de diferencia de gaussianas ( DoG ), este algoritmo se basa en el cálculo de la Hessiana  H . Esta matriz representa la derivada segunda para cada dirección en cada punto (horizontal, vertical y diagonal). Se calcula el determina de  H  que expresa el cambio local alrededor de un punto  x. A diferencia de SIFT, donde se genera una pirámide gaussiana de imágenes (imágenes cada vez más pequeñas, en SURF se genera una  pirámide gaussiana de filtros.  En cada escala se duplica el tamaño del filtro (horizontal y vertical). Finalmente, se calculan los máximos locales del determinante a diferentes escalas.  El  descriptor SURF  es una versión mejorada del algoritmo SIFT para la detección y descripción de puntos de interés. Se puede utilizar para el reconocimiento o el tracking de objetos, para reconstrucción 3D, segmentación basada en movimiento, etc. La principal ventaja es que es hasta 3 veces más rápido que el algoritmo SIFT y esto permite ser aplicado en problemas que requieren solución en tiempo real. El algoritmo consta de las siguientes etapas:

## Diapositiva 44

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 44 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.3.  Speeded -Up  Robust   Features  (SURF) Lo que se hace es  aproximar los filtros a una estructura más simple  mediante el cálculo de la Hessiana para acelerar el proceso.  𝜕 2 𝜕 𝑥 2 𝑔 ( 𝜎 )   𝜕 2 𝜕 𝑦 2 𝑔 ( 𝜎 )   𝜕 2 𝜕 𝑥𝑦 𝑔 ( 𝜎 )   𝐿 𝑥𝑥 ( 𝑥 , 𝜎 )   𝐿 𝑦𝑦 ( 𝑥 , 𝜎 )   𝐿 𝑥𝑦 ( 𝑥 , 𝜎 )

## Diapositiva 45

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 45 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.3.  Speeded -Up  Robust   Features  (SURF) Se calcula la  imagen integral   O(x)  a partir de la imagen original. Cada nuevo píxel de la imagen integral corresponde a la suma de todos los píxeles previos por filas y por columnas. Aunque el cálculo de la matriz integral pueda ser un poco costoso, solo hay que calcularla una vez, ya que las dimensiones de la imagen no van a cambiar. De esta manera, el cálculo de las máscaras (recordemos que en SURF lo que varía es la máscara de filtros) se obtiene muy rápido a partir de sumas y restas de valores  pre-calculados .

## Diapositiva 46

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 46 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.3.  Speeded -Up  Robust   Features  (SURF) 2. Cálculo de la orientación.  Una vez localizados los puntos de interés mediante el cálculo de la matriz Hessiana, se calculan las derivadas horizontales y verticales sobre la imagen original. Pero, en este caso, aprovechando que se tiene calculada la imagen integral, se realizan derivadas por bloque (wavelet). Estas derivadas se basan en sumar o restar un determinado valor a los píxeles que aparecen en la ventana. El tamaño de la máscara se ajusta en función de la escala (s). En la escala original la máscara sería 4x4 píxeles. Los cálculos se realizan para todos los píxeles de la ventana de vecindad alrededor del punto de interés para evitar el ruido. Esto da lugar a un valor de orientación de gradiente para cada píxel de la ventana. Estos valores se representan en un diagrama circular que se recorre en arcos de 60º para encontrar el región donde hay más cantidad de puntos. Dichos puntos corresponde a la dirección del gradiente de cada píxel de la ventana de vecindad.

## Diapositiva 47

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 47 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.3.  Speeded -Up  Robust   Features  (SURF) 3. Cálculo del descriptor SURF.  Se selecciona una ventana de 20x20 píxeles alrededor del punto de interés. A partir de dicha ventana, se obtienen 16 subregiones de 5x5 píxeles cada una. Para cada subregión se calcula la derivada wavelet y se extraen 4 características en un vector  𝜈 . De esta forma, para cada ventana de 20x20 píxeles se obtienen 4*16=64 características que describen el punto de interés.    Subregión de 5x5 píxeles También es posible extender la versión del algoritmo SURF  128 características para aumentar el nivel de distinción. Las sumas de  𝑑 𝑥  y  | 𝑑 𝑥 |   se   computan   por   separado   para   𝑑 𝑦 <0  y  𝑑 𝑦 ≥ 0 .  Lo mismo para  𝑑 𝑦   𝑦  | 𝑑 𝑦 | .  De esta manera, se duplican el número de características por subregión, dando lugar a 8*16=128 características.

## Diapositiva 48

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 48 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.5.3.  Histogram   of   oriented   gradients  (HOG) El  histograma de gradientes  utiliza la distribución de la dirección de los gradientes como características, ya que la magnitud del gradiente presenta una alta respuesta a los cambios de intensidad elevados. Esto permite obtener información sobre la forma de los objetos.  El algoritmo consta de los siguientes pasos: 1.   Cálculo de los gradientes de la imagen . Se calculan los gradientes horizontales y verticales mediante el filtrado de la imagen con un  kernel  de tamaño 1. Se puede aplicar el algoritmo de Sobel visto anteriormente. Una vez se han obtenido las matrices  𝐺 𝑥  y  𝐺 𝑦  que representan las aproximaciones de las derivadas de intensidades, se calcula la magnitud y la dirección del gradiente.

## Diapositiva 49

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 49 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 2.   Cálculo de gradientes en celdas de 8x8 . El hecho de escoger celdas de 8x8 píxeles es porque cada píxel tendrá 2 valores (magnitud y dirección), lo que da lugar a un total de 128 números. Estos 128 valores se pueden representar en un histograma de 9  bins  correspondiente a los ángulos 0, 20, 40, 60, 80, 100, 120, 140 y 160. Estas 9 características dan lugar a una representación óptima que no solo es la más compacta, sino que también es robusta frente al ruido.  Como se puede observar, la dirección del gradiente se evalúa entre 0 y 180 grados, en lugar de 0 y 360. Esto se denomina “ unsigned ”  gradients  porque la dirección del gradiente se representa en valor absoluto. 2.5.3.  Histogram   of   oriented   gradients  (HOG)

## Diapositiva 50

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 50 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 3.   Cálculo del histograma de gradientes de 9-bins . Una vez calculadas la magnitud y la dirección de los gradientes de cada píxel en la celda de 8x8, se construye un histograma de 9-bins donde cada  bin  representa una dirección y el valor de dicho  bin  viene determinado por la magnitud.  Si la dirección coincide con la etiqueta de un  bin  específico, entonces se añade íntegramente el valor de su magnitud a dicho  bin  (azul). Si la dirección toma valores entre dos  bins , la magnitud correspondiente se añadirá a los dos  bins  de manera proporcional (rojo). Nota: En el caso de que la dirección sea mayor de 180º, la magnitud se añadirá de manera proporcional entre los  bins  de 160 y 0, ya que 0 equivale a 180.  Finalmente, se crea el histograma de gradientes con las contribuciones de todos los píxeles de la celda 8x8.  2.5.3.  Histogram   of   oriented   gradients  (HOG)

## Diapositiva 51

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 51 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales 4.   Normalización del histograma de gradientes.  El objetivo es que el descriptor sea invariante frente a variaciones en la intensidad de los píxeles, es decir, invariante a los cambios de contraste y/o luminosidad. Para ello, se recorre la imagen en tamaños de ventana de 16x16, es decir, en cada paso se cogerán 4 celdas de 8x8. De esta manera, se obtendrán 4 histogramas de 9  bins  que dan lugar a un vector de características de 36 elementos. Estos elementos se normalizan de acuerdo a una regla (L1 o L2, por ejemplo). Después, la ventana se desplaza una celda (8 píxeles) y se vuelven a calcular y normalizar los 36 elementos. 2.5.3.  Histogram   of   oriented   gradients  (HOG) 5.   Cálculo del  histogram   of   oriented   gradients  (HOG).  En nuestro caso particular, el tamaño de la imagen era de 128x64 píxeles. Por tanto, en el eje horizontal hay 7 celdas de 16x16 píxeles (con solapamiento de celdas como se muestra en la animación) y en el eje vertical, 15 celdas. Puesto que en cada celda de 16x16 píxeles obteníamos un vector de características con 36 elementos, el descriptor final tendrá un total de 7*15*36=3780 características que son representativas de la imagen bajo estudio.

## Diapositiva 52

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 52 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales Los  Local  Binary   Patterns  (LBP)  consisten en un operador que describe patrones de la imagen a nivel local proporcionando buenos resultados en aplicaciones de reconocimiento de texturas y en identificación de objetos y formas. El algoritmo para extraer los LBP consiste en un protocolo de ventana deslizante donde el valor del píxel central se modifica a partir del valor de intensidad de sus píxeles vecinos. Paso 1. Se calcula la diferencia de intensidad entre los píxeles vecinos y el píxel central. Paso 2. Se construye una matriz auxiliar a partir de la  umbralización  de las diferencias con 0s en los valores negativos y 1s en los positivos.  Paso 3. La matriz construida da lugar a una cadena binaria que se multiplica por una matriz de referencia. Paso 4. Se suman todos los valores que resultan de la multiplicación anterior y se establece el valor del píxel central.  2.5.4. Local  Binary   Patterns  (LBP) 01011100 4 + 8 + 16 + 64 =  92 20 -5 0 0 2 3 4 5 6 7 0 1 4 8 16 𝟐 𝟐   𝟐 𝟒   𝟐 𝟑   𝟐 𝟔   8 16 32 128 64 4 64

## Diapositiva 53

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 53 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales Para hacer el descriptor  invariante a transformaciones de intensidad , aparecen los  𝑳𝑩 𝑷 𝑷 , 𝑹 ,  donde  P  es el número de píxeles vecinos alrededor del píxel de interés y  R , es el radio de dicha frecuencia.  P  determina el espacio angular y  R  la resolución espacial.    2.5.4. Local  Binary   Patterns  (LBP) Sin embargo, el descriptor en este punto es sensible a transformaciones de rotación. Para eliminar ese efecto, se define el operador  𝐿𝐵𝑃 𝑃 , 𝑅 𝑟𝑖  que asigna un identificador único a todas aquellas cadenas binarias que presentan el mismo número de transiciones.  Se llama transición a los cambios de 0 a 1, y viceversa, que aparecen en una cadena.

## Diapositiva 54

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 54 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales Por ejemplo, dadas dos cadenas binarias diferentes (11100001 y 01111000), cuyo número de transiciones es el mismo, se asigna un único identificador normalizado poniendo todos los 0s a la izquierda y los 1s a la derecha. De esta manera, ambas cadenas quedarían representadas por la cadena 00001111, donde se observan 2 transiciones (una de 0 a 1 y otra de 1 a 0).  Así pues, siendo  P=8  el número de píxeles vecinos, los LBP normales podían tener hasta  2 8 =256  posibles valores de patrones diferentes, mientras que el nuevo descriptor invariante a la rotación  𝐿𝐵𝑃 𝑃 , 𝑅 𝑟𝑖  presenta únicamente ( P+1) *4=36 valores distintos.    2.5.4. Local  Binary   Patterns  (LBP)

## Diapositiva 55

T EMA  3 - E XTRACCIÓN  D E  C ARACTERÍSTICAS 55 2.5. Descriptores de textura 1. Estadísticos unidimensionales 2. Características bidimensionales Más adelante se dedujo que muchos de esos 36 patrones presentaban información redundante, así que se introdujo el concepto de  uniformidad  dando lugar al descriptor   𝑳𝑩𝑷 𝑷 , 𝑹 𝒓𝒊 𝒖 𝟐    LBP uniformemente invariante a rotación. Se demostró que los patrones con un número de transiciones menor o igual a 2 tenían una capacidad discriminativa mucho mayor que el resto, por lo que se definieron dichos patrones como  LBP uniformes . El número total de  LBPs  uniformes es  P+1 . En el caso anterior, donde  P=8 , observamos que hay 9 LBP uniformes (cuadro azul), ya que dichos patrones presentan un número de transiciones menor o igual a 2. El resto de los LBP no uniformes (los 27 restantes) se agrupan todos en un único conjunto “no uniforme” . De esta manera, el descriptor  LBP uniformemente invariante a rotación    𝑳𝑩𝑷 𝑷 , 𝑹 𝒓𝒊 𝒖 𝟐  presenta P+2 posibles valores: de 0 a 8 para los patrones uniformes y la etiqueta adicional para los patrones no uniformes   2.5.4. Local  Binary   Patterns  (LBP) Imagen LBP Original Histograma LBP

## Diapositiva 56

A PRENDIZAJE  S UPERVISADO José Gabriel García Pardo josegabriel.garciap@campusviu.es Tema 3 – Extracción de características 05MIAR

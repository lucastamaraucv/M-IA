# Aprendizaje supervisado, desde cero y paso a paso

Esta es la puerta de entrada al curso. No necesitas saber programación ni ingeniería para seguir las primeras escenas. Cada apartado enseña **una idea** y termina con **una sola pregunta**. Contéstala antes de avanzar. Si no puedes explicar el «por qué», vuelve al ejemplo; todavía no hace falta memorizar el nombre técnico.

Los títulos ayudan a encontrar apartados, pero en una tutoría el nombre formal se presenta cuando la intuición quede clara. El desplegable bajo cada pregunta contiene el nombre original y su definición precisa: ábrelo **después** de responder. Luego aplica la idea a un caso nuevo con el tutor antes de marcarla como firme. Usa [la guía de profundización](07_explicacion_profunda_por_bloques.md) para fórmulas, código y límites. Las escenas y cifras didácticas son **hipotéticas, no datos del curso**; las ideas atribuidas al curso proceden de los resúmenes `02` a `06`. Donde el material no da teoría completa, lo indico.

| BATCH | Pregunta principal | Apartados |
|---|---|---|
| 1. Antes de entrenar | ¿Qué queremos averiguar y con qué información? | 1.1–1.10 |
| 2. Comprobar resultados | ¿Cómo sabemos si funcionará con casos nuevos? | 2.1–2.10 |
| 3. Describir los datos | ¿Qué partes de una tabla o imagen ayudan a decidir? | 3.1–3.5 |
| 4. Predecir números | ¿Cómo estimamos una cantidad desconocida? | 4.1–4.3 |
| 5. Elegir categorías | ¿Cómo decidimos entre dos o más clases? | 5.1–5.4 |

## BATCH 1. Antes de entrenar

### 1.1. Decide qué respuesta necesitas

Quieres ayudar a estudiantes que podrían reprobar. Antes de mirar datos, concreta la decisión: «a mitad del curso quiero saber quién necesita apoyo para ofrecerle tutoría». Esa frase dice **qué** quieres saber y **cuándo** debes saberlo.

Es como preparar una mochila: primero preguntas a dónde vas y cuánto durará el viaje. De lo contrario, puedes llenarla bien y aun así olvidar lo necesario. En un proyecto con datos, elegir un programa antes de fijar la decisión produce el mismo problema.

La nota final llega demasiado tarde para una alerta a mitad del curso. Una predicción solo ayuda si usa información disponible cuando todavía puedes actuar. Esta idea abre el proceso de trabajo descrito en el archivo `02`, sección 1.

**Compruébalo:** ¿por qué una predicción hecha al terminar el curso no sirve para decidir a mitad del curso a quién ofrecer apoyo?

<details><summary>Nombre original del curso — abre después de responder</summary>

CRISP-DM; primera fase: comprensión del negocio (archivo `02`, sección 1).


**Significado preciso:** CRISP-DM es una forma de organizar un proyecto de datos. Su primera fase aclara el objetivo práctico antes de preparar datos o elegir un modelo.
</details>

### 1.2. Distingue el caso, las pistas y la respuesta

Piensa en una cesta de frutas. Cada fruta es un caso. Su color y firmeza son pistas que puedes observar. «Está madura» es la respuesta que quieres conocer.

En una tabla ocurre igual: cada fila es un caso; las columnas que conoces antes de decidir son pistas; otra columna contiene la respuesta en los casos pasados. El archivo `02`, sección 3, da nombres precisos a esos tres papeles. Ábrelos después de responder.

**Compruébalo:** si quieres saber si una fruta está madura usando color y firmeza, ¿por qué «madura» cumple un papel distinto del color?

<details><summary>Nombre original del curso — abre después de responder</summary>

Instancia, atributo y clase o variable objetivo (archivo `02`, sección 3).


**Significado preciso:** Instancia = un caso o fila. Atributo = una pista conocida. Variable objetivo o clase = la respuesta que se quiere predecir.
</details>

### 1.3. Aprende de ejemplos con respuesta conocida

Supón que alguien te muestra frutas y te dice cuáles estaban maduras. Con suficientes ejemplos podrías reconocer pistas útiles. Si nadie te dice cuáles estaban maduras, todavía puedes agrupar frutas parecidas, pero no sabes qué grupo significa «madura».

Esa diferencia separa dos tipos de tarea. En una tienes ejemplos con la respuesta correcta y aprendes a predecirla. En la otra buscas grupos o patrones sin esa respuesta. El archivo `02`, sección 2, explica ambas formas de aprendizaje.

**Compruébalo:** ¿por qué agrupar frutas por aspecto no basta, por sí solo, para saber cuál grupo corresponde a las maduras?

<details><summary>Nombre original del curso — abre después de responder</summary>

Aprendizaje supervisado y aprendizaje no supervisado (archivo `02`, sección 2).


**Significado preciso:** Supervisado = aprende con casos cuya respuesta se conoce. No supervisado = busca patrones sin una respuesta etiquetada para cada caso.
</details>

### 1.4. Una cantidad o una categoría

Si preguntas «¿cuánto costará esta casa?», la respuesta puede ser una cantidad como ciento veinte mil. Si preguntas «¿se venderá este mes?», la respuesta pertenece a categorías como «sí» y «no».

El tipo de respuesta determina qué tarea estás resolviendo: predecir una cantidad o elegir una categoría. Una categoría puede estar escrita con números, como `0=no` y `1=sí`; esos números siguen siendo etiquetas, no convierten la tarea en predicción de una cantidad. El curso presenta esta distinción en el archivo `02`, sección 2.

**Compruébalo:** si `1` significa «sí» y `0` significa «no», ¿por qué predecir esa columna sigue siendo elegir una categoría?

<details><summary>Nombre original del curso — abre después de responder</summary>

Regresión y clasificación (archivo `02`, sección 2).


**Significado preciso:** Regresión = predecir una cantidad. Clasificación = predecir una categoría.
</details>

### 1.5. Reserva casos para comprobar lo aprendido

Imagina que practicas con un examen y luego te califican con exactamente las mismas preguntas. Una buena nota podría indicar que las memorizaste. Para saber si entendiste, necesitas preguntas nuevas.

Un *modelo* es la regla que se obtiene de los ejemplos. *Entrenar* significa aprender esa regla. Separa los casos pasados en dos partes antes de entrenar: una para aprender y otra para comprobar. Los casos reservados no deben participar en las reglas aprendidas. El archivo `03`, secciones 0–1, desarrolla esta separación.

```text
[gris: casos pasados] → [verde: aprender] + [azul: comprobar con casos reservados]
```

**Compruébalo:** ¿por qué medir el resultado con los mismos casos usados para aprender puede dar una impresión demasiado buena?

<details><summary>Nombre original del curso — abre después de responder</summary>

Conjunto de entrenamiento (*training set*) y conjunto de test (*test set*) (archivo `03`, sección 0).


**Significado preciso:** Entrenamiento = casos que enseñan la regla. Test = casos reservados para evaluarla al final.
</details>

### 1.6. Rellenar un dato ausente también es aprender una regla

En una lista faltan algunas edades. Decides sustituir cada espacio vacío por una edad «central» calculada a partir de edades conocidas. Esa edad central es una regla obtenida de los datos.

Por eso debes calcularla solo con los casos destinados a aprender. Si usas también los casos reservados para comprobar, ya dejaste que influyan en la preparación. El archivo `02`, sección 7, presenta la sustitución de ausencias; la conexión con la evaluación está en el archivo `03`.

**Compruébalo:** ¿por qué calcular la edad de reemplazo usando también los casos reservados contamina la comprobación?

<details><summary>Nombre original del curso — abre después de responder</summary>

Imputación de valores ausentes; fuga de información (*data leakage*) como advertencia metodológica.


**Significado preciso:** Imputación = sustituir un dato ausente según una regla. Fuga de información = dejar que datos reservados influyan en una regla que debería aprenderse solo con entrenamiento.
</details>

### 1.7. Un número raro merece una explicación antes de borrarlo

En una tabla de edades aparece `250`. Puede ser un error de escritura; también podría significar que la columna no contiene edades en años. Borrarlo de inmediato impide averiguar qué ocurrió.

Un valor muy distinto de los demás es una señal para investigar. Primero pregunta cómo se registró y qué representa. Después decide si corregirlo, conservarlo o excluirlo. El archivo `02`, sección 6, estudia estos valores extremos.

**Compruébalo:** ¿por qué encontrar un valor sorprendente no demuestra por sí solo que deba eliminarse?

<details><summary>Nombre original del curso — abre después de responder</summary>

Valor atípico o *outlier* (archivo `02`, sección 6).


**Significado preciso:** Outlier = observación muy alejada de las demás; puede ser error o un caso real.
</details>

### 1.8. Cambiar números a una escala común

**Problema real.** En una tabla, la edad se mide en decenas y el ingreso en miles. Si buscas casos «cercanos» comparando directamente esos números, el ingreso puede dominar solo por estar escrito en una escala mayor.

**Analogía cotidiana: la escala es lo difícil aquí.** Comparar una longitud escrita en metros con otra escrita en centímetros sin convertir las unidades puede engañarte. Cambiar la escala hace posible comparar; no vuelve importante una medida que antes no lo era.

Una forma de transformar una columna toma el menor valor observado como referencia baja y el mayor como referencia alta. Los valores intermedios quedan ubicados entre ambas referencias. El archivo `02`, sección 5, desarrolla la fórmula. Aprende las referencias solo con los casos de entrenamiento.

**Compruébalo:** ¿por qué cambiar la escala de una columna puede alterar qué casos parecen cercanos aunque los casos no hayan cambiado?

<details><summary>Nombre original del curso — abre después de responder</summary>

Normalización (*normalization*), según el archivo `02`, sección 5.

**Significado preciso:** transformación que usa los extremos observados en entrenamiento para situar cada valor en una escala relativa. Un caso futuro puede quedar fuera del intervalo inicial.

</details>

### 1.9. Medir cuánto se aleja un valor del promedio

**Problema real.** En otra columna, quieres saber si un valor está cerca o lejos de lo habitual, sin que importe su unidad original.

**Analogía cotidiana: aquí importa la distancia respecto a lo habitual.** Si en tu familia todos caminan casi la misma distancia diaria, un kilómetro extra puede ser llamativo. Si las distancias varían mucho, ese kilómetro extra puede ser normal.

La transformación resta el promedio de la columna y divide por una medida de cuánto suelen variar sus valores. Así, `0` significa «igual al promedio»; un valor positivo queda por encima y uno negativo por debajo. El archivo `02`, sección 5, muestra la fórmula. Aprende promedio y variación solo con entrenamiento.

**Compruébalo:** ¿por qué el mismo aumento de una unidad puede parecer grande en una columna que varía poco y pequeño en otra que varía mucho?

<details><summary>Nombre original del curso — abre después de responder</summary>

Estandarización (*standardization*) y puntuación `z`, según el archivo `02`, sección 5.

**Significado preciso:** a cada valor se le resta la media de entrenamiento y se le divide por su desviación estándar de entrenamiento.

</details>

### 1.10. Elegir pistas que estarán disponibles cuando decidas

**Problema real.** Para anticipar quién reprobará a mitad del curso, tienes asistencia, tareas entregadas y nota final. La nota final parece una pista excelente, pero todavía no existirá cuando debas tomar la decisión.

**Intuición (apoyo pedagógico).** Para decidir si llevar paraguas antes de salir, puedes mirar el cielo; no puedes usar como pista saber cómo terminó el paseo.

Elegir pistas consiste en conservar datos que ayudan a la tarea y que estarán disponibles a tiempo. Una pista medida después del resultado puede hacer que la evaluación parezca excelente y fallar en la práctica. El archivo `02`, sección 8, trata la elección de atributos.

**Compruébalo:** ¿por qué una pista muy relacionada con la respuesta puede ser inútil si solo aparece después de que debes decidir?

<details><summary>Nombre original del curso — abre después de responder</summary>

Selección de atributos (*feature selection*), según el archivo `02`, sección 8.

**Significado preciso:** proceso de escoger qué columnas de entrada usará el modelo; si se eligen según su relación con la respuesta, la elección se aprende solo con entrenamiento.

</details>

## BATCH 2. Comprobar resultados

### 2.1. Memorizar casos no es aprender una regla útil

Alguien puede recordar de memoria todas las respuestas de un cuestionario y fallar cuando cambian las preguntas. Un modelo también puede funcionar muy bien con casos que ya vio y fallar con casos nuevos.

Para detectarlo, compara su error en los casos usados para aprender con su error en los reservados. Si el primero es bajo y el segundo alto, puede estar ajustándose demasiado a los detalles conocidos. Si ambos son altos, puede no estar captando una regla útil. El archivo `03`, sección 0, introduce estas situaciones.

**Compruébalo:** ¿por qué acertar los casos ya vistos no demuestra que el modelo acertará casos nuevos?

<details><summary>Nombre original del curso — abre después de responder</summary>

Sobreajuste (*overfitting*) y subajuste (*underfitting*) (archivo `03`, sección 0).


**Significado preciso:** Sobreajuste = el modelo se adapta demasiado a casos conocidos y falla en nuevos. Subajuste = la regla es insuficiente y falla incluso en los conocidos.
</details>

### 2.2. Una sola división puede engañar por azar

Si pruebas un restaurante una sola vez, tal vez te tocó su mejor o peor día. Algo parecido ocurre al reservar una sola parte de los datos: la nota depende en parte de qué casos quedaron allí.

Una primera solución consiste en entrenar con una parte y evaluar con otra. Sirve como prueba, pero una sola nota no muestra cuánto variaría al cambiar la división. Esta es la idea de la separación simple del archivo `03`, sección 1.

**Compruébalo:** ¿por qué una única nota puede cambiar si reservas otros casos para la prueba?

<details><summary>Nombre original del curso — abre después de responder</summary>

Validación *hold-out* (archivo `03`, sección 1).


**Significado preciso:** Hold-out = reservar una parte de los casos para evaluar y aprender con el resto.
</details>

### 2.3. Repite la prueba cambiando la parte reservada

Divide los casos en tres grupos. En la primera vuelta reservas el primero y aprendes con los otros dos. En la segunda reservas el segundo. En la tercera reservas el tercero. Obtienes tres notas y ves cuánto cambian.

```text
Vuelta 1: [azul: prueba] [verde: aprende] [verde: aprende]
Vuelta 2: [verde: aprende] [azul: prueba] [verde: aprende]
Vuelta 3: [verde: aprende] [verde: aprende] [azul: prueba]
```

El archivo `03`, sección 2, explica esta repetición. Cada vuelta construye un modelo nuevo; nadie ha probado el mismo modelo tres veces.

**Compruébalo:** ¿por qué cambiar el grupo reservado ayuda a descubrir si la primera nota fue excepcional?

<details><summary>Nombre original del curso — abre después de responder</summary>

Validación cruzada *k-fold* (*cross-validation*) (archivo `03`, sección 2).


**Significado preciso:** K-fold = dividir en k grupos, llamados pliegues, y repetir k veces dejando fuera un pliegue distinto. En el dibujo, k=3.
</details>

### 2.4. Elegir la mejor configuración también puede engañar

Supón que pruebas diez maneras de preparar un plato y anuncias como calidad habitual la nota de la mejor. Esa nota fue precisamente la que usaste para elegir: puede ser demasiado optimista.

En modelos ocurre igual cuando comparas configuraciones, como cuántos casos parecidos consultar. Usa unas pruebas para elegir la configuración y otra prueba separada para estimar qué tan bien funciona **todo el proceso, incluida esa elección**. El archivo `03`, sección 3, describe esta separación en dos niveles.

**Compruébalo:** ¿por qué la prueba usada para elegir la mejor configuración no debería ser también la nota final que anuncias?

<details><summary>Nombre original del curso — abre después de responder</summary>

Ajuste de hiperparámetros y validación anidada (*nested cross-validation*) (archivo `03`, sección 3).


**Significado preciso:** Hiperparámetro = ajuste que se elige antes de aprender la regla. Validación anidada = una ronda interna para elegirlo y otra externa para evaluar el proceso completo.
</details>

### 2.5. El error de una cantidad puede medirse de varias maneras

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

Las fórmulas y un cálculo completo están en la guía de profundización, sección 2.6. El archivo `03`, sección 4, contiene MAE, MSE, RMSE y MAPE. La fórmula de R² está en el archivo `05`, sección 1. El MAPE directo falla cuando la cantidad real es cero; el notebook usa una variante que evita dividir directamente entre cero.

**Compruébalo:** ¿por qué los pares de errores `[10,10]` y `[0,20]` tienen el mismo MAE y distinto RMSE?

<details><summary>Nombre original del curso — abre después de responder</summary>

MAE, MSE, RMSE, MAPE y coeficiente de determinación R² (archivos `03`, sección 4; `05`, sección 1).


**Significado preciso:** MAE promedia tamaños de errores; MSE promedia sus cuadrados; RMSE saca raíz a MSE; MAPE los expresa respecto al valor real; R² compara con predecir siempre la media real.
</details>

### 2.6. Antes de contar aciertos, decide qué llamas «positivo»

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

<details><summary>Nombre original del curso — abre después de responder</summary>

Matriz de confusión: TP (*true positive*), FN (*false negative*), FP (*false positive*) y TN (*true negative*) (archivo `03`, sección 5).


**Significado preciso:** La matriz de confusión separa aciertos y errores según lo que ocurrió realmente y lo que se predijo; TP, FN, FP y TN son sus cuatro casillas.
</details>

### 2.7. Una nota general puede esconder el error importante

En el ejemplo anterior hay diez fraudes y noventa compras legítimas. Si un sistema dice «legítima» para todas, acierta noventa de cien veces. Sin embargo, no detecta ningún fraude.

Por eso conviene mirar más de una medida: la proporción de aciertos totales, la proporción de alertas que eran fraudes y la proporción de fraudes encontrados. El archivo `03`, sección 5, da sus fórmulas. La medida útil depende de qué error cuesta más y de cuántas falsas alarmas puedes aceptar.

**Compruébalo:** ¿por qué acertar noventa de cien compras puede ser inútil si tu tarea principal es encontrar fraudes?

<details><summary>Nombre original del curso — abre después de responder</summary>

Exactitud (*accuracy*), precisión (*precision*) y sensibilidad (*recall*) (archivo `03`, sección 5).


**Significado preciso:** Exactitud = proporción de aciertos totales. Precisión = proporción de alertas correctas. Sensibilidad = proporción de positivos reales que se detectaron.
</details>

### 2.8. La misma probabilidad puede llevar a decisiones distintas

Un termómetro marca veinticuatro grados. Una persona abre la ventana a partir de veinte; otra espera a veinticinco. La medida no cambió: cambió la regla de acción.

Un modelo puede estimar `0,4` como probabilidad de fraude. Si alertas a partir de `0,5`, no alertas; si alertas a partir de `0,3`, sí. Esa cifra de corte decide qué acción tomas. Al bajarla suelen aparecer más alertas, tanto acertadas como falsas. El archivo `06`, sección 1.1, explica esta regla cuando el modelo da una probabilidad.

**Compruébalo:** ¿por qué bajar el umbral puede cambiar una alerta sin cambiar lo que el modelo estimó?

<details><summary>Nombre original del curso — abre después de responder</summary>

Umbral de decisión (*decision threshold*) (archivo `06`, sección 1.1).


**Significado preciso:** Umbral de decisión = valor a partir del cual una puntuación o probabilidad se convierte en una clase o acción.
</details>

### 2.9. Resumir dos exigencias sin olvidar ninguna

**Problema real.** Un detector de fraude puede emitir pocas alertas muy acertadas y aun así dejar pasar muchos fraudes. Otro puede encontrar casi todos los fraudes, pero molestar a demasiadas compras legítimas.

**Intuición (apoyo pedagógico).** Para evaluar a un guardia, no basta saber si casi todas sus alarmas eran correctas; también importa si vio los problemas que realmente ocurrieron. Una sola cifra puede resumir ambas proporciones, aunque siempre conviene mirar las dos por separado.

El archivo `03`, sección 5, presenta una medida que combina la precisión de las alertas y la sensibilidad para encontrar casos positivos. Una medida combinada ayuda a comparar, pero no decide por ti cuánto cuesta cada tipo de error.

**Compruébalo:** ¿por qué una medida que solo mira si las alertas son correctas puede ocultar muchos fraudes no detectados?

<details><summary>Nombre original del curso — abre después de responder</summary>

F1-score o medida F1, según el archivo `03`, sección 5.

**Significado preciso:** media armónica de precisión y sensibilidad; será baja si una de las dos es baja. Su fórmula está en la guía de profundización.

</details>

### 2.10. Repetir muestras permitiendo casos repetidos

**Problema real.** Tienes un conjunto de casos y quieres observar cuánto cambia una medida cuando reconstruyes muestras a partir de él.

**Intuición (apoyo pedagógico).** Metes nombres en una bolsa, sacas uno, lo anotas y lo devuelves antes de sacar el siguiente. Como vuelve a la bolsa, puede salir otra vez; otros nombres quizá no salgan nunca.

Repitiendo el procedimiento obtienes muestras distintas y ves cómo varía una medida. Esto no es la misma división en grupos sin repetición que vimos antes. El archivo `03`, sección 2-bis, muestra ejemplos de este muestreo.

**Compruébalo:** ¿por qué un caso puede aparecer varias veces en una misma muestra de este tipo?

<details><summary>Nombre original del curso — abre después de responder</summary>

Bootstrap o *bootstrapping*, según el archivo `03`, sección 2-bis.

**Significado preciso:** muestreo con reemplazo repetido a partir de los casos disponibles para estudiar la variación de una estimación.

</details>

## BATCH 3. Describir los datos

**Fuentes del tema.** El archivo `04` resume notebooks prácticos. El PowerPoint original del profesor está en la carpeta `CLASES` y también en `explicacion video/material_curso/`. Las escenas y explicaciones siguientes son apoyo pedagógico; comprueba la teoría y las figuras en el PPTX. La definición del diámetro de Feret de su diapositiva 35 es conflictiva; consulta `explicacion video/ERRATAS_Y_LIMITES.md` antes de enseñarla.

### 3.1. Una etiqueta no es una cantidad

Tienes camisetas azules, verdes y rojas. Puedes contar cuántas hay de cada color. Si escribes `1=azul`, `2=verde` y `3=roja`, los números son solo códigos: el color rojo no es «tres veces» el azul.

Con datos como la ciudad de residencia ocurre lo mismo: sus códigos son arbitrarios. En nivel de estudios sí hay un orden, pero no sabemos que la distancia entre «secundaria» y «grado» sea igual a la distancia entre «grado» y «doctorado». El notebook de variables cualitativas del archivo `04` cuenta categorías y las muestra con gráficos.

**Compruébalo:** ¿por qué cambiar el código de «azul» de `1` a `8` no cambia el color ni la cantidad de camisetas azules?

<details><summary>Nombre original del curso — abre después de responder</summary>

Variable cualitativa o categórica; frecuencia absoluta (archivo `04`, sección 1).


**Significado preciso:** Variable cualitativa = valores que son categorías. Frecuencia absoluta = número de casos de cada categoría.
</details>

### 3.2. El promedio puede ocultar lo que vive la mayoría

Cinco personas cobran `[2, 2, 2, 2, 12]` unidades. Si sumas y divides entre cinco, obtienes `4`. Pero cuatro personas cobran `2`. El valor central al ordenar es `2`.

El promedio y el valor central responden preguntas distintas. El notebook de variables cuantitativas del archivo `04` calcula el valor típico, cuánto se alejan los demás y en qué lugar queda cada dato al ordenarlos. Antes de elegir una medida, mira si unos pocos valores extremos cambian mucho el resumen.

**Compruébalo:** ¿por qué decir solo «el ingreso típico es 4» puede dar una imagen engañosa de estas cinco personas?

<details><summary>Nombre original del curso — abre después de responder</summary>

Variable cuantitativa; media, mediana, tendencia central y dispersión (archivo `04`, sección 2).


**Significado preciso:** Variable cuantitativa = valores que representan cantidades. Media = suma dividida por número de casos. Mediana = valor central después de ordenar.
</details>

### 3.3. Una imagen es una tabla enorme de luces y colores

Una fotografía parece una escena continua, pero digitalmente está formada por pequeños puntos llamados *píxeles*. Cada píxel tiene un valor de luz o color. Cambiar esos valores puede hacer más visible un borde o separar mejor un objeto del fondo.

Los notebooks de imágenes del archivo `04` muestran maneras de cambiar qué tan claros u oscuros son los píxeles. Ese cambio no «entiende» el objeto; solo modifica la imagen. Si resalta también puntos que no pertenecen al objeto, la etapa siguiente puede empeorar.

**Compruébalo:** ¿por qué aumentar el contraste de una foto no significa que ya hayas identificado qué parte de ella es el objeto?

<details><summary>Nombre original del curso — abre después de responder</summary>

Imagen digital y transformación de intensidad (archivo `04`, sección 3).


**Significado preciso:** Píxel = unidad pequeña de una imagen digital. Transformación de intensidad = regla que cambia sus valores de claridad u oscuridad.
</details>

### 3.4. Primero separa el objeto del fondo

Quieres medir una hoja puesta sobre una mesa. Antes de medir, dibujas qué zona pertenece a la hoja. Si marcas también su sombra, tu medida describirá hoja más sombra.

En imágenes, separar los puntos del objeto y del fondo produce una máscara. Piensa en una plantilla: deja pasar lo que se medirá y tapa lo demás. Los notebooks de segmentación del archivo `04` muestran esta etapa.

```text
[gris: imagen] → [ámbar: zona candidata] → [verde: máscara elegida]
```

**Compruébalo:** ¿por qué una medida perfecta aplicada a una máscara que incluye la sombra seguiría describiendo mal la hoja?

<details><summary>Nombre original del curso — abre después de responder</summary>

Segmentación de imágenes y máscara (archivo `04`, sección 4).


**Significado preciso:** Segmentación = separar regiones de una imagen. Máscara = representación que indica qué píxeles pertenecen a la región elegida.
</details>

### 3.5. Mide una característica que ayude a decidir

Una vez aislada la hoja, puedes contar cuánto espacio ocupa o medir su contorno. Esos números resumen aspectos de la forma. También puedes medir patrones de luz de su superficie si la textura ayuda a distinguirla.

Los notebooks de forma y textura del archivo `04` muestran medidas como área y perímetro. También construyen una tabla de qué tonos de gris aparecen juntos —la matriz GLCM— para comparar parches de cielo y hierba. No todas las medidas ayudan a todas las tareas: para reconocer tamaño, el área puede servir; para distinguir superficies, quizá sirva más la textura.

**Compruébalo:** ¿por qué el área no sirve para distinguir una superficie lisa de una rugosa del mismo tamaño?

<details><summary>Nombre original del curso — abre después de responder</summary>

Extracción de características; descriptores de forma y textura; GLCM (*gray-level co-occurrence matrix*) (archivo `04`, secciones 5–6).


**Significado preciso:** Descriptor = número que resume una propiedad. Los de forma miden la región; los de textura resumen patrones de tonos, a menudo mediante la GLCM.
</details>

## BATCH 4. Predecir números

### 4.1. Sumar aportes para estimar una cantidad

Una factura puede tener una cuota fija y un cargo por cada hora de uso. Si la cuota es `10` y cada hora añade `2`, tres horas producen `10+2×3=16`.

La regla que se aprende usa esa forma: una base más un aporte por cada dato de entrada. Aprende los números de esos aportes mirando casos pasados y buscando que sus predicciones se alejen lo menos posible de las cantidades reales. El archivo `05`, sección 1, estudia una forma de hacerlo que da más peso a errores grandes al elevarlos al cuadrado. La factura solo explica la suma; los aportes aprendidos no prueban que una variable cause el resultado.

**Compruébalo:** si el cargo aprendido por hora es `2`, ¿por qué la predicción sube `2` al añadir una hora mientras todo lo demás queda igual?

<details><summary>Nombre original del curso — abre después de responder</summary>

Regresión lineal múltiple y mínimos cuadrados ordinarios (*ordinary least squares*, OLS) (archivo `05`, sección 1).


**Significado preciso:** Regresión lineal múltiple = suma de una base y aportes de varios atributos. OLS elige esos aportes minimizando errores al cuadrado.
</details>

### 4.2. Una línea recta puede quedarse corta

Una pelota lanzada hacia arriba primero sube y luego baja. Si dibujas su altura a lo largo del tiempo, una sola línea recta no sigue ambos tramos.

Puedes dar a la regla una nueva pista calculada a partir del tiempo, como «tiempo al cuadrado». Sigue sumando aportes, pero esa pieza permite que la predicción forme una curva. El notebook del archivo `05`, sección 2, muestra esta construcción. Una curva muy flexible puede copiar detalles de los casos conocidos y fallar en nuevos; se elige su complejidad usando pruebas reservadas.

**Compruébalo:** ¿por qué una curva muy flexible podría acertar los casos conocidos y fallar con casos nuevos?

<details><summary>Nombre original del curso — abre después de responder</summary>

Regresión polinómica (*polynomial regression*) (archivo `05`, sección 2).


**Significado preciso:** Regresión polinómica = crear potencias de los atributos, como x², para que una suma de aportes pueda seguir una curva.
</details>

### 4.3. Estimar desde casos parecidos

Para calcular cuánto tardará un trayecto nuevo, miras viajes anteriores con distancia y tráfico parecidos. Si tres viajes semejantes tardaron `10`, `12` y `20` minutos, una estimación sencilla es su promedio: `14` minutos.

Una regla basada en casos parecidos hace esa búsqueda de semejanza con números. Debes decidir qué datos definen «parecido», cómo medir la diferencia y cuántos casos consultar. El archivo `05`, sección 3, muestra que una columna con valores en miles puede pesar mucho más que otra con valores entre cero y uno, aunque no sea más útil.

**Compruébalo:** ¿por qué cambiar la manera de medir «parecido» puede cambiar qué viajes se eligen y, con ello, la predicción?

<details><summary>Nombre original del curso — abre después de responder</summary>

Vecinos más cercanos para regresión (*k-nearest neighbors*, KNN) (archivo `05`, sección 3).


**Significado preciso:** KNN para regresión = encontrar k casos cercanos según una distancia y combinar sus valores para estimar el caso nuevo.
</details>

## BATCH 5. Elegir categorías

### 5.1. Convertir pistas en una probabilidad estimada

Cuando miras el cielo, reúnes pistas como nubes y viento antes de decidir si llevar paraguas. Una pista puede inclinarte hacia «lloverá» y otra hacia «no lloverá».

El método del archivo `06`, sección 1, combina los datos en una puntuación y la transforma en un número entre cero y uno. Ese número se interpreta como probabilidad estimada de una clase, según el ajuste del modelo. Después se compara con una cifra de corte para tomar la decisión. Cambiar esa cifra no vuelve a calcular la probabilidad.

**Compruébalo:** ¿por qué una puntuación sin límite necesita transformarse antes de interpretarla como probabilidad?

<details><summary>Nombre original del curso — abre después de responder</summary>

Regresión logística (*logistic regression*, LOGR) y función sigmoide (archivo `06`, sección 1).


**Significado preciso:** Regresión logística = combina atributos en una puntuación. La función sigmoide convierte esa puntuación en un valor entre cero y uno.
</details>

### 5.2. Decidir mediante preguntas sucesivas

Para elegir ropa puedes preguntar: «¿Llueve?». Si no, preguntas: «¿Hace frío?». Cada respuesta te lleva por un camino hasta una decisión.

El método del archivo `06`, sección 2, aprende preguntas sobre los datos. Cada pregunta divide los casos en grupos; al final de una ruta hay una respuesta. Demasiadas preguntas pueden crear reglas para casos muy particulares y fallar con nuevos casos. Por eso se controla su tamaño y se evalúa con datos reservados.

```text
                 [ámbar: ¿llueve?]
                 /                \
   [verde: sí → paraguas]      [gris: no → otra pregunta]
```

**Compruébalo:** ¿por qué añadir más preguntas al árbol puede mejorar los casos conocidos sin garantizar mejores respuestas para casos nuevos?

<details><summary>Nombre original del curso — abre después de responder</summary>

Árbol de decisión; CART en los ejemplos del curso (archivo `06`, sección 2).


**Significado preciso:** Árbol de decisión = secuencia de preguntas que divide casos hasta llegar a una predicción. CART es una forma de construirlo.
</details>

### 5.3. Elegir una pregunta que separe mejor los grupos

**Problema real.** En un grupo hay frutas maduras y verdes mezcladas. Puedes preguntar «¿es amarilla?» o «¿es grande?». La mejor pregunta es la que deja grupos más uniformes para la respuesta que quieres conocer.

**Intuición (apoyo pedagógico).** Si ordenas calcetines oscuros y claros, una separación ayuda cuando cada montón queda con menos mezcla. No basta con crear dos montones; importa cómo quedaron.

El archivo `06`, sección 2.4, menciona dos maneras de medir cuánta mezcla queda. Ambas valen cero cuando un grupo contiene una sola clase. Para juzgar una pregunta, mira cómo cambia la mezcla en los grupos que produce, considerando también cuántos casos caen en cada uno.

**Compruébalo:** ¿por qué una pregunta que deja dos grupos casi puros puede ser más útil que otra que deja ambos muy mezclados?

<details><summary>Nombre original del curso — abre después de responder</summary>

Impureza de Gini y entropía; el archivo `06`, sección 2.4, las menciona como criterios de partición.

**Significado preciso:** dos funciones distintas que cuantifican la mezcla de clases en un nodo. Sus fórmulas y un ejemplo calculado están en la guía de profundización; no tienen la misma escala numérica.

</details>

### 5.4. Reconoce lo que el ejemplo de SVM muestra y lo que no explica

Si dibujas dos grupos de puntos en una hoja, podrías intentar trazar una separación entre ellos. Esa imagen ayuda a imaginar una clasificación, pero no explica todavía cómo se elige matemáticamente la separación.

El archivo `06`, sección 3, muestra código que usa `SVC` con `C=10` (valor elegido en el ejemplo) y kernel `rbf` (valor predeterminado de esa herramienta). «Kernel» es el nombre técnico de una función que permite comparar casos de otra manera; su mecanismo no queda explicado en este material. El código permite observar cómo entrenar, predecir y evaluar, pero no enseña cómo se elige matemáticamente la separación.

**Compruébalo:** ¿qué te falta saber, además de que el código funciona, para explicar cómo se separan los grupos?

<details><summary>Nombre original del curso — abre después de responder</summary>

Máquina de vectores de soporte (*support vector machine*, SVM); implementación `SVC` con kernel RBF (archivo `06`, sección 3).


**Significado preciso:** SVM = familia de clasificadores. SVC es la herramienta usada en el notebook; C y el kernel son configuraciones del modelo.
</details>

---

## Cómo continuar después de responder

Tras cada pregunta, el tutor debe seguir [tu prompt más reciente](prompt_tutor_chat_v11.md): escuchar tu respuesta, corregirla sin adelantarse y conectar la intuición con el término original. Después debe darte **un caso nuevo**, esperar tu solución y marcar la idea como firme solo si puedes aplicarla. Al terminar la sesión, debe entregar notas de una línea y un bloque de estado para retomarla. Para números, fórmulas, código y comparaciones ya justificadas, abre el apartado correspondiente de la guía de profundización.

# Aprendizaje supervisado: explicación para entender, aplicar y analizar

Esta guía acompaña los archivos `02` a `06`. Es un **mapa de consulta**, no una sesión completa: abre un solo apartado por turno y detente en su pregunta. Los encabezados son etiquetas para navegar; en una tutoría oral, el nombre formal se presenta después de verificar la intuición. **Fuente del curso** indica contenido localizable en los resúmenes. **Apoyo pedagógico** señala mis analogías, ejemplos y deducciones. **Ampliación externa** señala conocimientos útiles que no atribuyo al curso. Ninguna respuesta a las preguntas se incluye inmediatamente después de ellas.

| BATCH | Tema | Qué deberías poder hacer al terminar |
|---|---|---|
| 1 | Fundamentos y preparación | Definir la tarea, reconocer qué datos se pueden usar y preparar los datos sin contaminar la evaluación. |
| 2 | Validación y métricas | Estimar rendimiento en datos nuevos y elegir una métrica según el costo de los errores. |
| 3 | Características | Convertir variables e imágenes en números que conserven la información relevante. |
| 4 | Regresión | Explicar y comparar OLS, regresión polinómica y KNN para predecir números. |
| 5 | Clasificación | Explicar y comparar regresión logística, árboles y el uso de SVM mostrado en el curso. |

**Ruta de estudio:** lee un solo bloque conceptual y responde una sola pregunta antes de abrir el siguiente. Una respuesta correcta puede mostrar comprensión; para considerar el concepto *firme*, tendrás que aplicarlo a un caso nuevo y justificar una limitación. Los ejemplos numéricos de esta guía son inventados. Si estudias con un tutor, pídele que reserve la prueba nueva y la línea «Para tus notas» hasta después de tu respuesta.

---

## BATCH 1. Fundamentos y preparación de datos

### 1.1. ¿Qué problema resolvemos antes de elegir un algoritmo?

**Problema real.** Quieres saber si un estudiante necesitará apoyo durante el próximo mes. Tienes registros anteriores: asistencia, tareas entregadas y resultado final. La primera decisión no es qué modelo usar. Es definir *a quién* quieres predecir, *en qué momento* y *qué información existe en ese momento*.

**Intuición cotidiana (apoyo pedagógico).** Es como preparar una maleta para un viaje: antes de escoger objetos necesitas saber destino, duración y restricciones. Un modelo elegido antes de definir la tarea puede ser técnicamente correcto y resolver el problema equivocado.

**Concepto (fuente del curso, Tema 1).** CRISP-DM organiza el trabajo en seis fases: comprensión del negocio, comprensión de los datos, preparación de los datos, modelado, evaluación y despliegue. Es un ciclo: un hallazgo en evaluación puede obligarte a redefinir la pregunta o volver a preparar los datos.

**Aplicación.** En el ejemplo, “necesitará apoyo durante el próximo mes” es la respuesta que queremos conocer. Los datos de entrada deben estar disponibles *antes* de ese mes. Si una columna contiene la calificación al terminarlo, usarla sería conocer parte de la respuesta por adelantado. Define además qué decisión tomarás con la predicción: ofrecer tutoría, por ejemplo. Eso determina qué error cuesta más.

**Análisis.** Un buen resultado estadístico no basta si el dato llega tarde, la predicción no cambia ninguna decisión o la población futura difiere de la histórica.

**Compruébalo:** si el modelo predice el abandono al final del semestre, ¿por qué la nota final no debería entrar como atributo al hacer una alerta a mitad del semestre?

### 1.2. Instancia, atributo, objetivo y tipo de aprendizaje

**Problema real.** Una tabla de estudiantes tiene una fila por estudiante. Cada fila contiene asistencia y número de tareas. La columna “aprobó” registra el resultado.

**Intuición (apoyo pedagógico).** Para decidir si una fruta está madura, miras su color y firmeza; “madura o no” es lo que quieres conocer. La fruta concreta es una observación, las señales son atributos y el resultado es el objetivo.

**Concepto (fuente del curso, Tema 1).** Una *instancia* es un caso; los *atributos* describen el caso; la *clase* o variable objetivo es lo que se intenta predecir. En aprendizaje supervisado existen ejemplos con objetivo conocido. En el no supervisado se buscan estructuras sin esa etiqueta de respuesta. Si el objetivo es numérico continuo hablamos de **regresión**; si pertenece a categorías, de **clasificación**.

**Matiz.** “Numérico” no significa necesariamente regresión: los códigos `0` y `1` pueden representar categorías. Y una variable de entrada categórica puede usarse en un problema de regresión después de codificarla.

**Compruébalo:** si predices el precio de una casa, ¿por qué la zona es una pista de entrada y no la respuesta buscada?

### 1.3. Separar antes de aprender reglas de preparación

**Problema real.** En una tabla faltan edades. Quieres sustituirlas por la mediana. Si calculas esa mediana con toda la tabla, los casos reservados para evaluar influyen en la regla que aprenderá el modelo.

**Intuición (apoyo pedagógico).** Si un profesor prepara la hoja de respuestas mirando el examen que usará para evaluar, la nota ya no mide una capacidad independiente. Del mismo modo, calcular transformaciones con todos los datos permite que el conjunto de evaluación influya en el entrenamiento.

**Idea (fuente: archivo `02`, secciones 4–8; conexión con archivo `03`, sección 0).** Primero se reserva la parte que evaluará el modelo. Después se aprende en el conjunto de entrenamiento cualquier regla que dependa de los datos, como la mediana para reemplazar ausencias. La misma regla se aplica a los casos reservados y a los futuros. Así, la evaluación sigue siendo una prueba con datos que no determinaron la preparación.

**Secuencia (apoyo pedagógico).**

```text
[gris: tabla completa] → [verde: entrenamiento] ── aprende la mediana ──┐
                      → [azul: evaluación]   ← aplica la misma mediana ──┘
```

**Compruébalo:** si calculas la mediana con toda la tabla antes de separar los casos de evaluación, ¿por qué la prueba deja de ser independiente?

### 1.4. Normalizar y estandarizar son transformaciones distintas

**Problema real.** La edad está entre `20` y `60`, mientras el ingreso puede estar en miles. Si una técnica calcula distancias, la escala de ingreso puede dominar aunque no sea el atributo más informativo.

**Intuición (apoyo pedagógico).** Para comparar longitudes medidas en centímetros con otras medidas en metros, primero eliges una escala común. Cambiar la unidad no vuelve las medidas más relevantes; solo evita que una unidad domine por su tamaño numérico.

**Mapa de variables (fuente: archivo `02`, sección 5; ejemplo pedagógico).**

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `x` | Valor original de un atributo | Fila observada | Edad `40` | Se transforma con reglas aprendidas en entrenamiento. |
| `min`, `max` | Extremos usados para normalizar | Solo entrenamiento | `20`, `60` | `x'=(x-min)/(max-min)`; `40` pasa a `0,5`. |
| `μ` | Media para estandarizar | Solo entrenamiento | `40` | Se resta a cada valor nuevo. |
| `σ` | Desviación estándar | Solo entrenamiento | `10` | `z=(x-μ)/σ`; `50` pasa a `1`. |
| `x'` | Valor normalizado | Fórmula con `x`, `min` y `max` | `0,5` para edad `40` | Es una escala nueva; con datos futuros puede quedar fuera de `[0,1]`. |

**Procedimiento.** En normalización `x'=(x-min)/(max-min)`; en estandarización `z=(x-μ)/σ`. Aprende los valores de referencia solo en entrenamiento. Un caso futuro menor que el mínimo observado puede normalizarse a un número negativo; no lo recortes automáticamente. Si `max=min` o `σ=0`, la fórmula exige un tratamiento especial.

**Compruébalo:** si el máximo del entrenamiento es `60` y un caso futuro vale `70`, ¿por qué su valor normalizado puede superar `1` sin que la fórmula esté mal?

### 1.5. Ausencias, extremos y elección de atributos

**Problema real.** Algunas filas tienen edad ausente; otra dice que una persona tiene `250` años. También hay una columna registrada después del resultado que quieres predecir.

**Intuición (apoyo pedagógico).** Antes de hacer un promedio de gastos, averiguas si un recibo vacío significa «no compró» o «se perdió el recibo». Esas dos situaciones requieren decisiones distintas.

**Idea (fuente: archivo `02`, secciones 6–8).** Imputar reemplaza un valor ausente siguiendo una regla; un valor extremo puede ser error o caso real; seleccionar atributos decide qué información entra al modelo. Son decisiones separadas. Investiga el significado de las ausencias y extremos antes de corregirlos. La mediana de imputación y cualquier selección guiada por la respuesta se aprenden solo dentro de entrenamiento.

**Extremos.** La media y la desviación estándar son sensibles a ellos; la mediana suele resistir mejor. Eliminar automáticamente un extremo puede borrar justo el caso que necesitas detectar.

**Selección.** Una variable puede parecer predictiva porque revela indirectamente la respuesta o porque fue medida después del evento. Evalúa disponibilidad temporal y relación con el objetivo.

**Compruébalo:** ¿por qué no conviene eliminar automáticamente el registro de `250` años sin investigar antes de dónde salió?

---

## BATCH 2. Validación y métricas

### 2.1. ¿Qué significa que un modelo generalice?

**Problema real.** Un modelo acierta casi todos los casos que estudió. Quieres saber cómo funcionará con estudiantes nuevos.

**Intuición (apoyo pedagógico).** Repetir las respuestas de un cuestionario conocido no demuestra que puedas resolver otro cuestionario. Necesitas probar con preguntas que no viste mientras aprendías.

**Concepto (fuente del curso, Tema 2).** Entrenamiento ajusta el modelo; test estima el rendimiento en casos nuevos. *Sobreajuste*: error de entrenamiento bajo, error en datos nuevos alto. *Subajuste*: ambos errores altos porque el modelo es demasiado limitado o sus atributos no contienen suficiente señal.

**Matiz.** Una diferencia entre entrenamiento y test sugiere sobreajuste, pero revisa también cambios de población, errores de preparación y azar por muestra pequeña. Una única división no revela toda esa variación.

**Compruébalo:** si el error es alto tanto en entrenamiento como en casos nuevos, ¿por qué el modelo podría estar aprendiendo una regla demasiado simple?

### 2.2. Una división para probar con casos nuevos

**Problema real.** Entrenas con cien casos y mides el error usando esos mismos cien. El resultado puede describir memoria, no capacidad de predecir casos nuevos.

**Intuición (apoyo pedagógico).** Para saber si aprendiste a cocinar una receta, alguien prueba un plato que no preparaste mientras seguías indicaciones. La analogía termina ahí: los datos reservados también deben representar los casos que aparecerán después.

**Idea (fuente: archivo `03`, secciones 0–1).** Divide los datos antes de ajustar el modelo. Entrenamiento permite aprender sus parámetros. Si vas a comparar configuraciones, usa validación para elegirlas. Reserva test para la estimación final. Una configuración elegida antes de ajustar, como el número de vecinos, es un *hiperparámetro*; un coeficiente aprendido durante el ajuste es un *parámetro*.

```text
[gris: datos] → [verde: entrenamiento y elección] + [azul: test reservado]
```

**Compruébalo:** si eliges la configuración que mejor funciona en el test, ¿por qué ese test deja de ser una prueba final independiente?

### 2.3. Repetir la prueba con k-fold

**Problema real.** Una única división puede dar una nota afortunada o desafortunada. Quieres ver cómo cambia el resultado al reservar partes distintas.

**Intuición (apoyo pedagógico).** Para juzgar a un cocinero, pruebas platos preparados en ocasiones separadas. Un solo plato podría ser excepcional por azar. En cada ocasión, el plato evaluado debe quedar fuera de la preparación de ese intento.

**Idea (fuente: archivo `03`, sección 2).** Divide los datos en `k` partes. En cada vuelta deja una parte para evaluar y usa las otras para entrenar. Al terminar, resume las `k` notas. Cada caso sirve una vez como evaluación, aunque el modelo entrenado cambia en cada vuelta.

```text
Vuelta 1: [azul: evalúa] [verde: entrena] [verde: entrena]
Vuelta 2: [verde: entrena] [azul: evalúa] [verde: entrena]
Vuelta 3: [verde: entrena] [verde: entrena] [azul: evalúa]
```

**Compruébalo:** ¿por qué las tres vueltas del diagrama dan más información sobre la variabilidad del rendimiento que una sola división?

### 2.4. Elegir configuraciones y estimar rendimiento por separado

**Problema real.** Pruebas muchas profundidades de árbol y conservas la que obtiene mejor nota. Esa mejor nota puede reflejar parte del azar de las pruebas.

**Intuición (apoyo pedagógico).** Si eliges al ganador entre muchos estudiantes por un único ejercicio, la nota del ganador tiende a parecer mejor que su rendimiento habitual. Necesitas otro ejercicio para estimarlo.

**Idea (fuente: archivo `03`, sección 3).** En validación anidada, el ciclo interno compara configuraciones usando solo el entrenamiento del ciclo externo. El ciclo externo reserva casos para estimar el rendimiento de *todo el procedimiento de elección*. Toda transformación aprendida de los datos también se ajusta dentro de cada entrenamiento interno. Al terminar la evaluación, se puede volver a ajustar la búsqueda con todos los datos destinados al desarrollo para obtener el modelo que se usará.

```text
Exterior: [verde: datos para elegir] [azul: evaluación exterior]
Interior: [verde: ajuste] [ámbar: comparación de configuraciones]
```

**Compruébalo:** ¿por qué la parte exterior no debe participar en la elección de la profundidad?

### 2.5. Bootstrap para estudiar variabilidad

**Problema real.** Quieres saber cuánto cambia una estimación si vuelves a construir una muestra a partir de los mismos datos.

**Idea (fuente: archivo `03`, sección 2-bis).** En bootstrap se extraen casos *con reemplazo*: después de elegir un caso, puede volver a elegirse. Algunos se repiten y otros no entran en esa muestra. Repitiendo el proceso observas cómo varía una estimación. El notebook del curso incluye un ejemplo básico y otro repetido; no presupongas que utiliza automáticamente todos los casos no extraídos para evaluar un modelo.

**Compruébalo:** ¿por qué un mismo caso puede aparecer dos veces en una muestra bootstrap y no en una partición normal sin reemplazo?

### 2.6. Métricas de regresión: cada una responde una pregunta distinta

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

**Problema real.** Dos modelos predicen precios. Uno suele fallar por poco pero comete un error enorme; el otro falla moderadamente casi siempre. La mejor medida depende del costo del error.

**Intuición (apoyo pedagógico).** Si evaluaras tiros al blanco, podrías medir la distancia típica al centro o penalizar más una desviación enorme. También podrías preguntar si tus tiros superan la estrategia de apuntar siempre al lugar promedio. La analogía no determina el costo real: ese costo viene del problema.

**Fórmulas.** `MAE = promedio(|e_i|)` mide error absoluto típico en unidades de `y`. `MSE = promedio(e_i²)` castiga más los errores grandes y queda en unidades cuadradas. `RMSE = √MSE` recupera las unidades originales. `MAPE = promedio(|e_i/y_i|) × 100 %` expresa error relativo. Si `y_i=0`, el cociente directo no está definido; el notebook del Tema 2 usa una variante con `max(ε, |y_i|)` en el denominador. `R² = 1 - SSE/SST` compara con predecir siempre `ȳ`; puede ser negativo si el modelo es peor que esa referencia. Si `SST=0`, esta fórmula requiere tratamiento especial.

**Ejemplo calculado.** Valores reales `[10, 20, 30]`; predicciones `[12, 18, 24]`. Errores `[-2, 2, 6]`. `MAE=(2+2+6)/3=3,33`; `MSE=(4+4+36)/3=14,67`; `RMSE≈3,83`. La media real es `20`, así que `SST=100+0+100=200`, `SSE=44` y `R²=1-44/200=0,78`. Para MAPE, las proporciones son `2/10`, `2/20` y `6/30`: `16,67 %` de promedio.

**Trampa frecuente.** `RMSE` no es la media de los errores absolutos; la raíz se aplica *después* de promediar los cuadrados. Cambiar el orden cambia el número.

**Compruébalo:** dos modelos tienen el mismo MAE, pero uno comete un error aislado mucho mayor. ¿Por qué podrían tener RMSE distinto?

### 2.7. Métricas de clasificación: define primero qué es “positivo”

**Mapa de la matriz de confusión (fuente: archivo `03`, sección 5; caso pedagógico).** Define “fraude” como positivo.

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `TP` | Fraude real y alerta | Real positivo, predicho positivo | `8` | Aumenta precisión y sensibilidad. |
| `FN` | Fraude real sin alerta | Real positivo, predicho negativo | `2` | Reduce sensibilidad. |
| `FP` | Compra legítima con alerta | Real negativo, predicho positivo | `12` | Reduce precisión. |
| `TN` | Compra legítima sin alerta | Real negativo, predicho negativo | `78` | Aumenta exactitud. |

**Problema real.** Un filtro detecta fraudes. No detectar un fraude y bloquear una compra legítima son errores distintos.

**Intuición (apoyo pedagógico).** En una revisión de equipaje, importa tanto cuántos objetos peligrosos detectas como cuántas maletas inocentes detienes. Un porcentaje general de aciertos puede esconder uno de esos dos errores.

**Cálculo.** Hay `100` compras; `10` son fraude. Exactitud o *accuracy* `=(TP+TN)/100=86 %`. Precisión `=TP/(TP+FP)=8/20=40 %`: de las alertas, cuatro de cada diez son fraude. Sensibilidad o *recall* `=TP/(TP+FN)=8/10=80 %`: se detectan ocho de cada diez fraudes. `F1=2×precisión×sensibilidad/(precisión+sensibilidad)≈53,33 %`; resume el equilibrio entre precisión y sensibilidad.

**Análisis.** Un clasificador que dijera “legítima” a todo lograría `90 %` de exactitud, pero detectaría `0 %` de fraudes. Si el costo de un fraude no detectado es alto, observa la sensibilidad y cuántas falsas alarmas puedes asumir.

**Compruébalo:** ¿por qué el clasificador que siempre dice “legítima” puede tener mayor exactitud y ser peor para detectar fraudes?

### 2.8. El umbral cambia la decisión, no la probabilidad calculada

**Problema real.** Un modelo da a una compra una probabilidad estimada de fraude. Debes decidir a partir de qué valor activar una alerta.

**Intuición (apoyo pedagógico).** Un termómetro marca la misma temperatura aunque decidas abrir la ventana a partir de veinte o de veinticinco grados. Cambió tu regla de acción, no la medición.

**Idea (apoyo pedagógico; conexión con archivo `06`, sección 1.1).** El umbral convierte una puntuación o probabilidad en una clase. Bajarlo suele detectar más positivos reales y también activar más falsas alarmas, porque más casos quedan por encima de la línea de decisión. El efecto exacto depende de las puntuaciones observadas.

**Compruébalo:** si una compra tiene probabilidad estimada `0,4`, ¿por qué puede cambiar su clase predicha al bajar el umbral sin volver a entrenar el modelo?

---

## BATCH 3. Extracción de características

**Nota de fuente.** El archivo `04` resume notebooks prácticos. El PowerPoint original del tema 3 está en la carpeta `CLASES` y también en `explicacion video/material_curso/`. Lo siguiente explica los procedimientos observables de los notebooks y añade intuiciones propias; para la teoría y las figuras del profesor, consulta el PPTX. La diapositiva 35 contiene una definición conflictiva del diámetro de Feret, documentada en `explicacion video/ERRATAS_Y_LIMITES.md`.

### 3.1. De una observación a un atributo útil

**Problema real.** Quieres identificar el tipo de objeto de una fotografía. El modelo necesita una representación numérica. La foto original contiene gran cantidad de píxeles, muchos irrelevantes para la decisión.

**Intuición (apoyo pedagógico).** Para reconocer una fruta puedes fijarte en tamaño, forma y color, sin memorizar cada punto de su superficie. Un atributo resume algo observable que puede ayudar a distinguir casos.

**Concepto.** Extraer características transforma datos originales en variables útiles para analizar o modelar. “Útil” depende de la tarea: el color puede servir para madurez y resultar poco informativo para tamaño. Antes de convertir, pregunta qué distinción debe preservar la representación.

**Compruébalo:** ¿por qué el mismo descriptor puede ser útil para una tarea y casi inútil para otra?

### 3.2. Contar categorías sin inventar distancias

**Problema real.** Tienes niveles de estudios de una población. Quieres saber cuántas personas hay en cada nivel.

**Intuición (apoyo pedagógico).** Puedes contar cuántas camisetas son azules o verdes. Asignarles códigos `1` y `2` facilita guardarlas en una tabla, pero no convierte “verde menos azul” en una medida con sentido.

**Idea (fuente: archivo `04`, notebook de variables cualitativas).** Cuenta la frecuencia de cada categoría y muéstrala con barras o sectores. Si las categorías tienen orden, conserva ese orden al presentar los resultados. Un código numérico de categoría no indica por sí mismo una distancia cuantitativa entre niveles.

**Matiz.** Los niveles de estudios sí tienen un orden, pero los códigos numéricos no demuestran que la distancia entre dos niveles consecutivos sea siempre igual.

**Compruébalo:** ¿por qué la media de los códigos `1=secundaria` y `2=grado` no describe un nivel de estudios real?

### 3.3. Resumir una variable cuantitativa sin ocultar su distribución

**Problema real.** Cinco ingresos son `[2, 2, 2, 2, 12]`. Quieres describir lo habitual y la variación.

**Intuición (apoyo pedagógico).** Si cuatro compras cuestan poco y una cuesta mucho, el gasto promedio sube, aunque la mayoría de las compras no se parezca a ese promedio.

**Idea (fuente: archivo `04`, notebook de variables cuantitativas).** La media y la mediana resumen el centro de maneras distintas; medidas de posición ubican valores ordenados; medidas de dispersión muestran cuánto varían; gráficos como el histograma muestran la forma. El notebook calcula y representa estas familias; las interpretaciones siguientes son apoyo pedagógico.

| Familia | Qué pregunta responde | Ejemplo | Precaución |
|---|---|---|---|
| Tendencia central | ¿Dónde se agrupan los valores? | Media, mediana | La media se mueve mucho por valores extremos. |
| Posición | ¿Qué valor deja cierta fracción por debajo? | Cuartiles, percentiles | Requiere ordenar los valores. |
| Dispersión | ¿Cuánto cambian los valores? | Rango, desviación estándar | Un centro igual puede esconder variaciones distintas. |
| Distribución | ¿Qué forma tiene el conjunto? | Histograma, asimetría | El aspecto del histograma depende de sus intervalos. |

**Ejemplo calculado.** La media es `(2+2+2+2+12)/5=4` y la mediana es `2`, el valor central al ordenar. Decir solo “ingreso típico: 4” oculta que cuatro de cinco casos valen `2`.

**Compruébalo:** ¿por qué la mediana describe mejor el valor de la mayoría en este ejemplo?

### 3.4. Imágenes: transformación, segmentación y descripción

**Problema real.** En una imagen hay un objeto de interés sobre un fondo. Para clasificar su forma necesitas aislarlo antes de medirlo.

**Intuición (apoyo pedagógico).** Para medir el contorno de una hoja sobre una mesa, primero decides qué parte de la foto es hoja y qué parte es mesa. Si incluyes la sombra, el perímetro medido cambia.

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

**Compruébalo:** si el umbral de segmentación incorpora parte del fondo, ¿por qué podría aumentar el área aunque el objeto real no haya cambiado?

---

## BATCH 4. Modelos de regresión

### 4.1. Regresión lineal: qué aprende OLS

**Problema real.** Quieres predecir el consumo eléctrico a partir de temperatura y horas de uso.

**Intuición (apoyo pedagógico).** Imagina una factura con una cuota fija más un cargo por cada hora de uso. La cuenta muestra cómo se suman aportes. Aquí termina la analogía: la factura define cargos, mientras que un coeficiente aprendido de datos no demuestra que una variable cause el resultado.

**Concepto (fuente: archivo `05`, sección 1).** La regresión lineal combina atributos mediante coeficientes. OLS elige coeficientes para minimizar la suma de errores al cuadrado en entrenamiento. La ecuación es lineal en los parámetros `w`; el atributo `x` puede haberse transformado antes de entrar.

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `x₁`, `x₂` | Atributos | Datos del caso | Horas `3`, temperatura `25` | Se introducen en la ecuación. |
| `w₀` | Intercepto | Entrenamiento | `10` | Valor predicho cuando los atributos valen cero; puede no tener interpretación real si cero está fuera de los datos. |
| `w₁`, `w₂` | Coeficientes | Entrenamiento | `2`, `0,5` | Multiplican sus respectivos atributos. |
| `ŷ` | Predicción | `w₀+w₁x₁+w₂x₂` | `10+2×3+0,5×25=28,5` | Se compara con el resultado real al evaluar. |

**Análisis.** Un coeficiente cambia si los atributos están correlacionados. No lo interpretes como efecto causal solo porque el modelo prediga bien. Un error grande pesa más por el cuadrado, de modo que OLS puede ser sensible a valores extremos. Evalúa residuos y rendimiento fuera de entrenamiento.

**Precisión matemática.** Minimizar suma de cuadrados y minimizar MSE da los mismos coeficientes para un conjunto fijo, porque MSE solo divide por `n`; las cifras de ambas funciones de costo son distintas. OLS puede resolverse por distintos procedimientos computacionales: el objetivo matemático no exige un método iterativo particular.

**Compruébalo:** si `w₁=2`, ¿cómo cambia la predicción al aumentar una hora de uso y mantener fija la temperatura?

### 4.2. Regresión polinómica: crear curvatura sin cambiar la idea básica

**Problema real.** La relación entre horas de estudio y resultado mejora al principio, pero luego se aplana. Una recta puede quedarse corta.

**Intuición (apoyo pedagógico).** Una pelota lanzada hacia arriba primero sube y luego baja. Una recta no puede seguir ambos tramos; una curva sí. La analogía ilustra la forma, no afirma que todas las relaciones reales sean parabólicas.

**Concepto (fuente: notebook del Tema 4).** Se crean atributos como `x²` y se ajusta un modelo lineal sobre `[x, x²]`: `ŷ=w₀+w₁x+w₂x²`. Es no lineal respecto a `x`, pero lineal respecto a `w₀,w₁,w₂`. Con varios atributos también pueden aparecer interacciones, según la transformación elegida.

**Análisis (ampliación externa).** Aumentar el grado da más flexibilidad y también más riesgo de sobreajuste: para `n` valores de entrada distintos, un polinomio de grado `n−1` puede pasar exactamente por los `n` puntos. Eso no garantiza buenas predicciones nuevas. Elige grado usando validación, con la creación de términos y cualquier escalado dentro de cada entrenamiento. Fuera del rango observado, las potencias pueden crecer de forma poco razonable.

**Compruébalo:** ¿por qué un polinomio de grado alto puede ajustar muy bien los datos conocidos y fallar con nuevos casos?

### 4.3. KNN para regresión: predicción desde vecinos

**Problema real.** Un caso nuevo se parece a varios casos conocidos. Puedes estimar su valor a partir de los más cercanos.

**Intuición (apoyo pedagógico).** Para estimar cuánto tarda un trayecto desconocido, consultas trayectos anteriores con distancia y tráfico parecidos. Cuáles consideras “parecidos” cambia la respuesta.

**Concepto (fuente del curso, Tema 4).** KNN conserva casos de entrenamiento. Para un caso nuevo calcula distancias, elige `k` vecinos y combina sus valores objetivo; en la versión básica usa la media. Puede ponderarlos por distancia si se configura así.

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular o inferir |
|---|---|---|---|---|
| `k` | Número de vecinos | Hiperparámetro elegido con validación | `3` | Determina cuántos objetivos se combinan. |
| `d` | Distancia entre casos | Atributos y métrica elegida | Euclídea o Manhattan | Ordena los vecinos; cambia con escalas y atributos. |
| `y₁…yₖ` | Objetivos de vecinos | Entrenamiento | `10, 12, 20` | Media simple `14`; con pesos puede cambiar. |
| `ŷ` | Predicción nueva | Agregación de vecinos | `14` | Se compara con el valor real solo al evaluar. |

**Trampa metodológica.** Si un atributo está en miles y otro entre cero y uno, el primero puede dominar la distancia. Estandarizar con entrenamiento suele importar para KNN. `k` muy pequeño vuelve la predicción sensible a ruido; `k` muy grande mezcla casos menos similares. **Ampliación externa:** con muchos atributos, las distancias pueden perder capacidad para distinguir vecinos útiles.

**Compruébalo:** si agregas a KNN una variable irrelevante medida en miles, ¿por qué podrían cambiar los vecinos elegidos?

---

## BATCH 5. Modelos de clasificación

### 5.1. Regresión logística: de una puntuación a una probabilidad

**Problema real.** Debes predecir si un estudiante aprobará. La combinación de sus atributos puede dar cualquier número, pero una probabilidad debe estar entre cero y uno.

**Intuición (apoyo pedagógico).** Reúnes indicios en una puntuación. Después los conviertes en una escala acotada: puntuaciones muy bajas se acercan a cero; muy altas se acercan a uno.

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

**Compruébalo:** si el modelo da `p=0,4`, ¿por qué la clase predicha puede cambiar al bajar el umbral de `0,5` a `0,3`?

### 5.2. Árboles: preguntas sucesivas que dividen casos

**Problema real.** Clasificas si se puede jugar tenis según clima. Una sola condición quizá no baste, pero varias preguntas encadenadas pueden separar los ejemplos.

**Intuición (apoyo pedagógico).** Para elegir ropa preguntas primero si llueve; según la respuesta, preguntas si hace frío. Cada pregunta crea grupos más concretos.

**Concepto (fuente del curso, Tema 5).** Un árbol divide recursivamente el conjunto según atributos y umbrales. Cada hoja produce una predicción. Para elegir cortes se usan criterios como Gini o entropía: prefieren grupos con menos mezcla de clases. La *ganancia* de una división compara la impureza antes y después, ponderando por tamaño de los grupos.

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular o inferir |
|---|---|---|---|---|
| `p_c` | Proporción de clase `c` en un nodo | Casos de entrenamiento del nodo | `3/4` positivos | Alimenta Gini y entropía. |
| Gini | `1-Σp_c²` | Proporciones del nodo | Con `3/4` y `1/4`: `0,375` | Es `0` si el nodo es puro. |
| Entropía | `-Σp_c log₂ p_c` | Proporciones del nodo | Con `3/4` y `1/4`: `≈0,811` bits | Es `0` si el nodo es puro; se toma `0 log 0 = 0`. |
| Profundidad | Número de cortes a lo largo de una ruta | Crecimiento o límite configurado | `3` | Más profundidad permite reglas más específicas. |

**Trampa metodológica.** Gini y entropía no tienen la misma escala numérica. No compares sus valores brutos para declarar ganador a uno; compara cómo cada criterio ordena divisiones dentro del mismo procedimiento. Un árbol sin límites puede aprender peculiaridades del entrenamiento. Poda o restringe profundidad, tamaño mínimo de hojas u otras opciones mediante validación.

**Compruébalo:** ¿por qué un corte que deja dos hojas bastante puras suele ser preferible a uno que mantiene ambas muy mezcladas?

### 5.3. SVM: qué puedes afirmar a partir del material disponible

**Fuente del curso.** El archivo `06` documenta una llamada a `sklearn.svm.SVC`, con `C=10` y el kernel predeterminado `rbf`, además del flujo de evaluación. Esos materiales no desarrollan la teoría del hiperplano, margen, vectores de soporte ni kernels. Por eso este bloque separa el uso observado de una intuición adicional.

**Intuición externa breve (apoyo pedagógico, pendiente de fuente teórica adicional).** Un clasificador SVM busca una frontera entre clases; algunos ejemplos cercanos a esa frontera son decisivos para colocarla. Con un kernel como RBF, la frontera puede ser curva en el espacio original. El parámetro `C` influye en cuánto penaliza ciertos errores de clasificación durante el ajuste. Esto orienta la lectura del código, pero no sustituye una explicación rigurosa de la optimización ni del kernel.

**Aplicación respaldada por el notebook.** Identifica `X` e `y`, separa datos, ajusta `SVC`, predice sobre datos no usados para ajustar y evalúa con métricas de clasificación. Si estandarizas, calcula la escala solo con entrenamiento. Para comparar con logística o árboles, usa el mismo protocolo de validación y elige la métrica según la tarea.

**Compruébalo:** ¿por qué ejecutar correctamente el notebook no basta para afirmar que comprendes cómo SVM elige su frontera?

---

## Cierre: decidir qué modelo y qué métrica usar

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

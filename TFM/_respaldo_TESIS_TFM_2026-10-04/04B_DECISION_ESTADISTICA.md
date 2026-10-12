# Procedimiento para decidir el análisis estadístico

**Tipo:** recomendación metodológica, no requisito impuesto por la VIU. Úsalo después de definir pregunta, datos, particiones y métrica primaria. El resultado puede ser **«no realizar una prueba de hipótesis»** con una justificación clara. Nunca elijas una técnica solo porque otra tesis la utilizó.

## Paso 1. Completa la ficha de diseño

```text
Pregunta exacta que se contrastará:
Resultado primario y unidad de medida:
Unidad independiente real:
Número de unidades independientes:
Número de modelos y comparaciones previstas:
¿Mismas unidades para todos los modelos? Sí/No
¿Un conjunto de datos o varios conjuntos independientes?
¿Hay dependencia temporal, espacial, familiar, por persona o por dispositivo?
¿Los parámetros/umbrales se eligieron sin usar el test final? Sí/No
¿El análisis es confirmatorio o exploratorio?
¿Qué magnitud de diferencia sería útil en la práctica?
```

Si no puedes completar la **unidad independiente** y el origen de las mediciones, no selecciones una prueba. Regresa a datos y protocolo.

## Paso 2. Decide el objetivo del análisis

| Objetivo | Salida mínima | Prueba formal |
|---|---|---|
| Describir rendimiento del sistema | Métrica, tamaño de muestra, distribución de errores, incertidumbre apropiada. | No obligatoria. |
| Comparar métodos para elegir uno en este problema | Diferencia pareada, costo y robustez en el test reservado. | Solo si el diseño permite una prueba válida. |
| Afirmar superioridad general en muchas tareas | Resultados por conjunto de datos independiente y rangos. | Puede requerir Wilcoxon/Friedman y análisis posterior. |
| Evaluar impacto en un uso real | Métricas ligadas al uso, incertidumbre y costos/efectos. | Depende de la unidad de decisión y del diseño; el valor p no basta. |

## Paso 3. Sigue la rama que corresponde

### A. Un conjunto de datos, un test final, dos clasificadores sobre los mismos casos

1. Guarda para cada unidad su etiqueta real y las dos predicciones con el mismo umbral fijado previamente.
2. Calcula la métrica y su diferencia, con intervalo de incertidumbre adecuado a la unidad.
3. Si la pregunta formal es si difieren sus **errores de clasificación** en esos casos pareados, considera **McNemar** a partir de los desacuerdos. Comprueba que las unidades pareadas sean independientes entre sí y que haya cantidad suficiente de desacuerdos para la aproximación usada; si no, usa la variante exacta apropiada o limita la afirmación.
4. McNemar no evalúa diferencias de AUC, calibración, coste ni generalización a otros datasets. Para esas preguntas, diseña un análisis específico.

### B. Un conjunto de datos con validación cruzada o repetición de particiones

1. Usa exactamente las mismas particiones para comparar métodos.
2. Informa distribución de resultados, diferencias y sensibilidad a las particiones/semillas.
3. **No trates cada fold como una muestra independiente** en una prueba t o Wilcoxon ordinaria: los conjuntos de entrenamiento se solapan. Si necesitas inferencia formal, consulta un método diseñado para validación repetida y justifica sus supuestos con el director; de lo contrario, describe incertidumbre y límites sin prueba.
4. Si hay un test final verdaderamente reservado, úsalo una sola vez para la conclusión principal después de fijar el modelo.

### C. Dos clasificadores evaluados en varios conjuntos de datos independientes

1. Obtén una métrica agregada por método y por dataset con protocolo comparable.
2. Calcula la diferencia **por dataset**: esa es la muestra para comparar métodos.
3. Presenta diferencias, signos, magnitud y distribución. Si la hipótesis y supuestos lo permiten, considera **Wilcoxon de rangos con signo**; revisa la simetría aproximada de diferencias y el tratamiento de empates/cero. Si no procede, usa una descripción o prueba de signos justificada.
4. No sustituyas el número de datasets por el número de folds o registros.

### D. Tres o más métodos en varios datasets independientes

1. Forma una matriz completa: filas = datasets, columnas = métodos, celdas = la misma métrica.
2. Presenta resultados y rangos por dataset. Si corresponde, usa **Friedman** como contraste global.
3. Si el análisis posterior compara pares, fija qué pares importan y aplica un procedimiento de comparaciones múltiples justificable. Informa las diferencias además del valor p.
4. Si faltan métodos o hay protocolos no comparables en algunos datasets, no rellenes celdas artificialmente; revisa diseño o limita alcance.

### E. Series temporales, unidades agrupadas o experimentos con dependencia

1. Identifica la estructura dependiente antes de estimar intervalos: tiempo, personas, centros, sesiones o activos.
2. No uses un bootstrap de registros individuales ni una prueba de observaciones independientes si rompe esa estructura. Considera remuestreo por bloque/grupo, períodos de evaluación verdaderamente separados o un modelo estadístico apropiado, con justificación documentada.
3. Si el número de grupos/períodos independientes es insuficiente, comunica el resultado como evidencia limitada; no fabriques potencia estadística aumentando el número de ventanas solapadas.

## Paso 4. Especifica incertidumbre y tamaño del efecto

- Indica qué varía: muestra de casos, datasets, períodos, particiones, semillas o anotadores. Un intervalo solo tiene sentido respecto de esa fuente de variación.
- Da diferencia absoluta en la métrica primaria y, si es útil, una diferencia relativa con denominador definido. Añade límites de incertidumbre cuando el diseño lo permita.
- Para métricas calculadas sobre casos independientes, un intervalo bootstrap puede ser apropiado; remuestrea unidades completas. Si hay grupos o series, preserva esa dependencia.
- Informa costo de ejecución o inferencia cuando forma parte del objetivo. Un pequeño aumento de métrica puede carecer de utilidad con costo desproporcionado.
- No conviertas `p < 0,05` en regla universal de éxito. Decide previamente el criterio práctico y reporta incertidumbre, magnitud y límites.

## Paso 5. Prepara la salida reproducible

Registra: hipótesis primaria, técnica, versión de software, supuestos, datos usados, unidad independiente, número de comparaciones, tratamiento de empates, nivel de confianza/umbral elegido, valores calculados, código y conclusión limitada al diseño. Si se exploran pruebas después de ver los resultados, identifícalas como exploratorias.

## Fuentes primarias y alcance

- [Demšar (2006), JMLR](https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf): comparación de clasificadores sobre **múltiples datasets**; advierte sobre aplicar pruebas ordinarias a folds correlacionados.
- [SciPy, `wilcoxon`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html): hipótesis, tratamiento de ceros y opciones de cálculo.
- [scikit-learn, validación cruzada](https://scikit-learn.org/stable/modules/cross_validation.html): particiones y evaluación.
- [scikit-learn, errores comunes](https://scikit-learn.org/stable/common_pitfalls.html): fuga de información y ajuste correcto.
- [NIST/SEMATECH Engineering Statistics Handbook](https://www.nist.gov/programs-projects/nistsematech-engineering-statistics-handbook): referencia general para métodos estadísticos.

La selección final debe revisarse con el director si se busca una afirmación inferencial fuerte o si el diseño tiene dependencia compleja.

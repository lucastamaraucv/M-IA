# Notebooks del Modo Maestro

Un notebook Jupyter por cada sesion del **Modo Maestro** del Visual Debugger
(`python_visualizer_flask.py`), mas una carpeta de referencia extra sobre las
librerias que se usan en las sesiones. Cada notebook trae:

1. El codigo de ejemplo real (identico al de la sesion, o un ejemplo de
   referencia curado para `referencia/`).
2. Los metodos/funciones de Python que usa, con su explicacion.
3. Una **explicacion paso a paso automatica** (generada a partir del AST del
   codigo, ver `code_walkthrough.py`): que hace cada bloque — asignaciones,
   bucles, condicionales, funciones, clases, try/except — en el orden en que
   se ejecuta.
4. En las sesiones del Modo Maestro, ademas, un cierre "como reutilizar esto"
   con las funciones/clases/variables que quedan definidas tras ejecutar la celda.

Generados automaticamente — ver `sessions_data.py` (clase `Session`, carga
`sessions.json`), `method_docs.py` (diccionario de explicaciones),
`code_walkthrough.py` (explicador AST) y `generate_notebooks.py` (arma todo
en `notebooks/`). Para regenerar tras editar sesiones en la app:
`node _extract.js && python generate_notebooks.py`.

## 📚 Referencia extra: Python / NumPy / Pandas / Matplotlib / Seaborn

Empezá por [`00_verificar_entorno.ipynb`](referencia/00_verificar_entorno.ipynb): confirma
que tu Jupyter/Anaconda tenga todas las librerias que usan las sesiones
(estandar: `abc`, `collections`, `csv`, `functools`, `heapq`, `io`, `math`,
`string`, `sys` — siempre disponibles; terceros: `numpy`, `pandas`,
`matplotlib`, `seaborn` — vienen por defecto en Anaconda) y te dice el
comando exacto para instalar lo que falte.

Ademas de las sesiones, `referencia/` trae 5 notebooks independientes con
mas ejemplos curados (no ligados a una sesion puntual) de las librerias
base del temario, cada uno con enlace a su documentacion oficial:

- [Python — biblioteca estandar](referencia/python_stdlib.ipynb) — <https://docs.python.org/3/> — strings avanzado, listas/tuplas/dicts avanzado, itertools, functools, re, datetime, pathlib, json, dataclasses, context managers, typing.
- [NumPy](referencia/numpy.ipynb) — <https://numpy.org/> — creacion de arrays, dtypes, indexado/mascaras, reshape, broadcasting, vectorizacion vs bucles, agregaciones por eje, algebra lineal, ordenar/buscar, aleatoriedad reproducible.
- [Pandas](referencia/pandas.ipynb) — <https://pandas.pydata.org/> — loc/iloc, ordenar/rankear, groupby con agregaciones multiples, merge/concat, pivot_table/crosstab, datos faltantes, apply/map/.str, fechas, CSV en memoria, estadisticas descriptivas.
- [Matplotlib](referencia/matplotlib.ipynb) — <https://matplotlib.org/> — linea, subplots, barras, scatter, histograma, personalizacion/leyenda, interfaz orientada a objetos (fig/ax), anotaciones.
- [Seaborn](referencia/seaborn.ipynb) — <https://seaborn.pydata.org/> — temas, scatterplot con hue, histplot, boxplot/violinplot, heatmap de correlacion, barplot, pairplot, lineplot con banda de variabilidad.

Se generan con `generate_reference_notebooks.py`, a partir del contenido
escrito en `reference_data.py` (no se extraen de la app, son ejemplos
propios validados ejecutandolos con NumPy/Pandas/Matplotlib/Seaborn
instalados). Para regenerar: `python generate_reference_notebooks.py`.

## Sesiones del Modo Maestro

## S00 · Intro y tipos

- [S00 · Variables y tipos](notebooks/S00_intro_y_tipos/00_variables_y_tipos.ipynb)
- [S00 · Strings y slicing](notebooks/S00_intro_y_tipos/01_strings_y_slicing.ipynb)
- [S00 · Operadores](notebooks/S00_intro_y_tipos/02_operadores.ipynb)

## S01 · Colecciones

- [S01 · Lista, Tupla, Set, Dict](notebooks/S01_colecciones/03_lista_tupla_set_dict.ipynb)

## S02 · Control de flujo

- [S02 · if / elif / else](notebooks/S02_control_de_flujo/04_if_elif_else.ipynb)
- [S02 · while, for, enumerate](notebooks/S02_control_de_flujo/05_while_for_enumerate.ipynb)

## S03 · Comprehensions

- [S03 · List y Dict comprehension](notebooks/S03_comprehensions/06_list_y_dict_comprehension.ipynb)

## S04 · Excepciones

- [S04 · try / except / else / finally](notebooks/S04_excepciones/07_try_except_else_finally.ipynb)

## S05 · Funciones

- [S05 · Funciones con anotaciones](notebooks/S05_funciones/08_funciones_con_anotaciones.ipynb)
- [S05 · *args y **kwargs](notebooks/S05_funciones/09_args_y_kwargs.ipynb)
- [S05 · Lambda, recursion, closure](notebooks/S05_funciones/10_lambda_recursion_closure.ipynb)

## S06 · OOP

- [S06 · Clases y objetos](notebooks/S06_oop/11_clases_y_objetos.ipynb)
- [S06 · Herencia y polimorfismo](notebooks/S06_oop/12_herencia_y_polimorfismo.ipynb)
- [S06 · @property y @staticmethod](notebooks/S06_oop/13_property_y_staticmethod.ipynb)
- [S06 · Clases abstractas (ABC)](notebooks/S06_oop/14_clases_abstractas_abc.ipynb)

## S07 · Estructuras de datos

- [S07 · Stack, Queue, Heap](notebooks/S07_estructuras_de_datos/15_stack_queue_heap.ipynb)
- [S07 · Grafos y BFS](notebooks/S07_estructuras_de_datos/16_grafos_y_bfs.ipynb)

## S08 · Funcional

- [S08 · map / filter / reduce](notebooks/S08_funcional/17_map_filter_reduce.ipynb)

## S09 · Generadores

- [S09 · yield y next (generadores)](notebooks/S09_generadores/18_yield_y_next_generadores.ipynb)

## S10 · NumPy

- [S10 · NumPy Arrays basicos](notebooks/S10_numpy/19_numpy_arrays_basicos.ipynb)
- [S10 · NumPy Indexado y slicing](notebooks/S10_numpy/20_numpy_indexado_y_slicing.ipynb)
- [S10 · NumPy Broadcasting y stats](notebooks/S10_numpy/21_numpy_broadcasting_y_stats.ipynb)
- [S10 · NumPy Algebra lineal](notebooks/S10_numpy/22_numpy_algebra_lineal.ipynb)

## S11 · Pandas

- [S11 · Pandas Series](notebooks/S11_pandas/23_pandas_series.ipynb)
- [S11 · Pandas DataFrame](notebooks/S11_pandas/24_pandas_dataframe.ipynb)
- [S11 · Pandas groupby y apply](notebooks/S11_pandas/25_pandas_groupby_y_apply.ipynb)
- [S11 · Pandas merge](notebooks/S11_pandas/26_pandas_merge.ipynb)

## S05 · Archivos

- [S05 · Archivos con io.StringIO](notebooks/S05_archivos/27_archivos_con_io_stringio.ipynb)
- [S05 · CSV en memoria](notebooks/S05_archivos/28_csv_en_memoria.ipynb)

## S07 · TDD

- [S07 · Tests con assert](notebooks/S07_tdd/29_tests_con_assert.ipynb)

## S10 · +Pandas

- [S10 · Correlaciones](notebooks/S10_pandas/30_correlaciones.ipynb)
- [S10 · Nulos y limpieza](notebooks/S10_pandas/31_nulos_y_limpieza.ipynb)
- [S10 · Pivot table](notebooks/S10_pandas/32_pivot_table.ipynb)
- [S10 · Strings en Pandas](notebooks/S10_pandas/33_strings_en_pandas.ipynb)

## S11 · Visualizacion

- [S11 · Datos para graficos (NumPy)](notebooks/S11_visualizacion/34_datos_para_graficos_numpy.ipynb)

## S13 · Generadores avanzados

- [S13 · Generator expressions](notebooks/S13_generadores_avanzados/35_generator_expressions.ipynb)
- [S13 · Pipeline de generadores](notebooks/S13_generadores_avanzados/36_pipeline_de_generadores.ipynb)

## S14 · NLP

- [S14 · NLP sin NLTK](notebooks/S14_nlp/37_nlp_sin_nltk.ipynb)

## S15 · Machine Learning

- [S15 · KNN desde cero (ML)](notebooks/S15_machine_learning/38_knn_desde_cero_ml.ipynb)

## S16 · Imagenes

- [S16 · Imagenes con NumPy](notebooks/S16_imagenes/39_imagenes_con_numpy.ipynb)

## 🎓 Práctica 1 (examen final)

- [P1 · 01 FRange (iterativo)](notebooks/P1_practica_1_examen_final/40_01_frange_iterativo.ipynb)
- [P1 · 01 FRange (con range)](notebooks/P1_practica_1_examen_final/41_01_frange_con_range.ipynb)
- [P1 · 02 Ciudades en Florida](notebooks/P1_practica_1_examen_final/42_02_ciudades_en_florida.ipynb)
- [P1 · 03 RLE (iterativo)](notebooks/P1_practica_1_examen_final/43_03_rle_iterativo.ipynb)
- [P1 · 03 RLE (recursivo)](notebooks/P1_practica_1_examen_final/44_03_rle_recursivo.ipynb)

## 🎓 Práctica 2 (examen final)

- [P2 · 01 sort_by (generador)](notebooks/P2_practica_2_examen_final/45_01_sort_by_generador.ipynb)
- [P2 · 02 categorizar (np.where)](notebooks/P2_practica_2_examen_final/46_02_categorizar_np_where.ipynb)
- [P2 · 03 pivot_table](notebooks/P2_practica_2_examen_final/47_03_pivot_table.ipynb)

## 🎓 Práctica 3 (examen final)

- [P3 · 01 Pinguinos - Exploracion](notebooks/P3_practica_3_examen_final/48_01_pinguinos_exploracion.ipynb)
- [P3 · 02 Pinguinos - NumPy](notebooks/P3_practica_3_examen_final/49_02_pinguinos_numpy.ipynb)
- [P3 · 03 Pinguinos - Limpieza y nueva columna](notebooks/P3_practica_3_examen_final/50_03_pinguinos_limpieza_y_nueva_columna.ipynb)
- [P3 · 04 Titanic - Exploracion](notebooks/P3_practica_3_examen_final/51_04_titanic_exploracion.ipynb)
- [P3 · 05 Titanic - NumPy](notebooks/P3_practica_3_examen_final/52_05_titanic_numpy.ipynb)
- [P3 · 06 Titanic - Limpieza y nueva columna](notebooks/P3_practica_3_examen_final/53_06_titanic_limpieza_y_nueva_columna.ipynb)

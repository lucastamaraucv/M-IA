# La capacidad predictiva de las redes neuronales LSTM respecto del Bitcoin: diseño y optimización de una red neuronal LSTM para predecir las variaciones en el precio del Bitcoin en el corto plazo

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 6, 24 a 27, 49 y 54 a 66 de 75; no leídas las páginas de revisión general de machine learning en finanzas ni el tratamiento de los datos de las secciones 4.1 a 4.4.3)

| Campo | Valor |
|---|---|
| Título exacto | La capacidad predictiva de las redes neuronales LSTM respecto del Bitcoin. Diseño y optimización de una red neuronal LSTM para predecir las variaciones en el precio del Bitcoin en el corto plazo |
| Autor / Directora | Iñigo Sánchez Zurdo; directora: María Coronado Vaca |
| Tipo / Venue / Año | Trabajo de fin de grado, Facultad de Ciencias Económicas y Empresariales, Madrid, junio de 2022 (la universidad no aparece nombrada en las páginas leídas; **comprobar en el repositorio**) |
| Archivo local | `LA CAPACIDAD PREDICTIVA DE LAS REDES NEURONALES LSTM RESPECTO DEL BITCOIN - Sanchez, Zurdo, Inigo.pdf` |
| URL / DOI | SIN DOI en el documento |
| Métodos | Red LSTM con normalización por lotes y dropout (una celda base, optimizada por fases en unidades, dropout, tasa de aprendizaje, optimizador, tamaño de lote, tamaño de bloque, escalado y épocas); comparada con GRU y RNN simple y con tres modelos de referencia (variación nula, media ingenua y regresión lineal) |
| Datos | Cotización de Bitcoin minuto a minuto; objetivo: retorno logarítmico a 5 minutos vista a partir de los 60 minutos anteriores; datasets de 10, 20 y 30 variables (precio, volumen e indicadores técnicos) (p. 2 y p. 54) |

## Aporte clave

Es el único trabajo de la carpeta que **llega a un resultado negativo claro y bien explicado**: un LSTM cuidadosamente optimizado para predecir el **retorno** de Bitcoin a 5 minutos **no supera** a los referentes de "variación nula" (paseo aleatorio) ni de "media ingenua", porque en la práctica predice un valor casi constante cercano a cero (p. 2, p. 60 a 63). Está en español y usa la regresión del retorno, que es la formulación correcta, en vez del nivel del precio.

## Hallazgos cuantitativos (HECHO, con página)

- **Referentes** (p. 59): (1) variación nula, que predice retorno cero, equivalente a "el mejor pronóstico del precio futuro es el actual"; (2) media ingenua, que predice el retorno medio del entrenamiento; (3) regresión lineal.
- **Resultados en el conjunto de evaluación** (Tabla 13, p. 60), con el retorno logarítmico como objetivo:

| Modelo | ME | RMSE | MAE |
|---|---|---|---|
| Variación nula (20 y 30 variables) | −0,000031 | **0,002236** | **0,001479** |
| Media ingenua | −0,000013 | 0,002236 | 0,001478 |
| LSTM (20 variables) | −0,000033 | 0,002257 | 0,001500 |
| LSTM (30 variables) | −0,00376 | 0,002414 | 0,001671 |
| GRU (20 variables) | 0,001595 | 0,002791 | 0,002125 |
| GRU (30 variables) | −0,000505 | 0,002372 | 0,001640 |
| Regresión lineal (20 variables) | −0,00642 | 0,061574 | 0,002133 |
| RNN simple (20 variables) | 0,002479 | 0,003546 | 0,002820 |

- **El LSTM con 20 variables queda por encima (peor) que los dos referentes ingenuos** en las tres métricas; el RMSE es 0,002257 frente a 0,002236 (p. 60).
- **Mecanismo del fallo:** las predicciones del LSTM se concentran en un rango muy estrecho cercano a cero, muy por debajo del rango de los retornos reales; por eso su error es el de un modelo constante (p. 60 y p. 61). La GRU muestra el mismo problema con algo más de amplitud.
- **Optimización por fases** (p. 49 a 53): tamaño de bloque óptimo de 60 observaciones (pérdida 0,001474 frente a 0,001922 con 30 y 0,002595 con 120); escalado MinMax(−1,1) como el mejor (0,001688, frente a 0,004921 con RobustScaler); 128 unidades, dropout 0,2, tasa de aprendizaje 0,01, Adam, lote de 64 y 20 épocas (Tabla 12, p. 53).
- **Escalado sin fuga:** el escalado se ajusta solo con el conjunto de entrenamiento; la autora cita a Chan (2021) y el "look-ahead bias" (p. 50).
- **Limitación de datos:** se usó alrededor del **2 % de las observaciones disponibles** por falta de capacidad computacional, y la optimización se hizo reduciendo los conjuntos al 20 % de su tamaño (p. 43 y p. 58).
- **Conclusión de la autora** (p. 58): no puede afirmarse capacidad predictiva superior a la del paseo aleatorio ni a la media ingenua; los resultados "no suponen una negación del potencial de las redes neuronales, sino la reafirmación de que su optimización es sumamente complicada".

## Revisión de la literatura (HECHO, con página)

- La literatura en criptomonedas se concentra casi por completo en **clasificar la dirección**, no en regresar el retorno (p. 6).
- Albariqi y Winarko (2020) critican que se publiquen resultados positivos sin validación cruzada, con probable sobreajuste (p. 26); la precisión de las RNN en la literatura suele estar por debajo de 60 %.
- Chen y colaboradores (2019) concluyen que los modelos estadísticos superan a las redes en datos de baja frecuencia, y que las redes superan a los estadísticos con datos de alta frecuencia (p. 24).
- Trabajos citados como metodológicamente sólidos: Cocco, Tonelli y Marchesi (2021), Mudassir y colaboradores (2020), Albariqi y Winarko (2020): usan validación cruzada, retornos en lugar de precios y ajuste de hiperparámetros (p. 26).

## Limitaciones y críticas

- Declarado por la autora: restricción computacional como el principal escollo; la optimización por fases en lugar del proceso iterativo completo; faltan indicadores (bandas de Bollinger); el 2 % de los datos; la alta frecuencia podría no ser lo óptimo en un mercado tan volátil (p. 58 y p. 59).
- **[OPINIÓN]** El colapso a una predicción casi constante sugiere un problema de ajuste o de escala del objetivo más que una prueba de que el LSTM sea inútil: con una señal tan débil, minimizar el error cuadrático lleva a predecir la media. Es coherente con lo que describe la tesis de Domingo Colomer para una lectura con regularización excesiva (valores casi constantes); en este trabajo no se comprueba esa causa, por lo que queda como hipótesis.
- **[OPINIÓN]** No se evalúa la **dirección** ni se aplica una prueba estadística de la diferencia entre modelos; las diferencias de RMSE (0,002257 frente a 0,002236) son de 1 % y no se acompañan de intervalos.
- **[OPINIÓN]** Una sola partición y una sola ejecución; los resultados dependen de la semilla.
- **[OPINIÓN]** El nivel del trabajo es de grado, con una muestra reducida; úsese como ejemplo metodológico y no como evidencia definitiva a 5 minutos.

## Conexión con mi tesis (red E20)

- **Es el antecedente más parecido a mi hallazgo principal:** un modelo complejo bien afinado que **no supera** a la media o al paseo aleatorio en retornos de alta frecuencia. Respalda que "E20 empata con los referentes simples" es un resultado esperable y publicable.
- **Formulación correcta:** retorno (o magnitud) en vez de nivel del precio, referentes ingenuos explícitos y escalado ajustado solo con el entrenamiento: coincide con mi protocolo.
- **El colapso a la media:** explica por qué conviene evaluar la **dirección y el movimiento** además del error cuadrático, y por qué mi lectura fija C=3e-5 debe comprobarse contra una lectura constante.
- **Escala temporal:** a 5 minutos no hay señal con el LSTM; mi hallazgo es que la dirección es algo predecible entre 1 minuto y 2 horas con otras variables y objetivos; **hay que explicar esa diferencia** (variables, objetivo y periodo distintos) en vez de darla por contradictoria.
- **Referencias españolas útiles:** Albariqi y Winarko (2020), Cocco y otros (2021) y Mudassir y otros (2020) como estándares de metodología.
- **Límite para citarlo:** trabajo de grado, muestra del 2 % de los datos y una sola ejecución.

## Referencias que cita y conviene localizar (DOI según el documento; verificar)

Albariqi y Winarko (2020), "Prediction of Bitcoin Price Change using Neural Networks" (ICoSTA, 10.1109/icosta48221.2020.1570610936); Aygün y Kabaçi (2021), comparación de métodos estadísticos y de aprendizaje automático para retornos diarios de Bitcoin (10.31590/ejosat.822153); Cocco, Tonelli y Marchesi (2021), "Predictions of Bitcoin prices through machine learning based frameworks" (PeerJ Computer Science, 10.7717/peerj-cs.413); Chen, Li y Sun (2020), "Bitcoin price prediction using machine learning: an approach to sample dimension engineering" (10.1016/j.cam.2019.112395); Bailey y López de Prado (2021), "Finance is not excused" (10.2139/ssrn.3895330); Bergsli y colaboradores (2022), volatilidad de Bitcoin (10.1016/j.ribaf.2021.101540); Caporale y Zekokh (2019), GARCH con cambio de régimen en criptomonedas (10.1016/j.ribaf.2018.12.009); Dey y colaboradores (2021), RNN en distintas frecuencias (10.3390/a14080251); Mudassir y colaboradores (2020), predicción de Bitcoin con variables de alta dimensión (Neural Computing and Applications). **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico de los capítulos 3 a 6 (páginas 27 a 64 del PDF; numeración interna 22 a 59), que la ficha anterior no había leído en las secciones 4.1 a 4.4.3. La revisión general de aprendizaje automático en finanzas (capítulos 1 y 2) se resume en la ficha. Páginas = páginas del PDF.

## A1. Planteamiento (p. 27 y p. 28)

Objetivo: analizar la capacidad predictiva de redes LSTM sobre el Bitcoin, pero **como regresión de la variación del precio (retorno logarítmico)** y no como clasificación del signo; además, estudiar los indicadores técnicos como entradas y llevar el análisis a **datos de alta frecuencia (minuto a minuto, horizonte de 5 minutos)**. El alcance se limita por la capacidad de cómputo disponible.

## A2. Datos (p. 29 a 34)

- **Fuente:** Crypto Data Download (bolsa Bitstamp): BTCUSD, ETHUSD, LTCUSD y XRPUSD, cada minuto, con apertura, máximo, mínimo, cierre, volumen en dólares y número de monedas intercambiadas; periodo disponible del 16 de agosto de 2017 al 6 de junio de 2022 (inicio fijado por ETHUSD).
- **Muestra realmente usada: solo el mes de enero de 2022** (1 al 31 de enero), **44 640 observaciones**, por limitaciones de cómputo (todas las técnicas "no han podido ser aplicadas con datos superiores a 1 mes"; ≈ 2 % de los datos disponibles). Se eliminan **131 observaciones con volumen cero**, quedando **44 509**.
- **Variables adicionales (116 iniciales, Tabla 1):** apertura, máximo, mínimo, cierre, volumen en monedas y en dólares (a 1 minuto, para BTC, ETH, LTC y XRP); **razón de cotización respecto a BTC** (ETH, LTC, XRP); **media móvil exponencial (EMA) del cierre** y su razón con el cierre (Ct/EMAc) con ventanas de 5, 15, 30, 60, 120, 240, 360, 720 y 1 440 minutos (BTC y ETH); EMA del volumen en dólares y su razón; **MACD(12, 26, 9)** (BTC); **RSI** de 15, 30, 60, 120, 360, 720 y 1 440 minutos (BTC y ETH) y la razón RSI_BTC/RSI_ETH; **varianza realizada** de 15, 30 y 60 minutos (solo BTC, por la propagación de volatilidad de Yi y otros, 2018, y HAR de Bergsli y otros, 2022); y el objetivo.
- **Objetivo:** el **retorno logarítmico de BTC a 5 minutos vista** a partir de los bloques de los minutos anteriores (se elige 5 y no 1 minuto para dejar tiempo de ejecución de una futura estrategia).
- **Fórmula del RSI con volumen** (Morosan, 2011): RSI = 50·(1 + 1/(1 + RS_v) − 1/(1 + RS_r)), con RS_v la fuerza relativa del volumen y RS_r la del precio (no se aclara si se usa la versión estándar o ésta en los cálculos).
- **Transformaciones (Tabla 2):** logaritmo de los retornos para precios, volúmenes y razones de cotización; variación porcentual para las EMA; **sin transformación** para Ct/EMAc, Vol/EMAv, MACD, RSI y la varianza realizada (que genera errores de cálculo con logaritmos y valores extremos).

## A3. Selección de variables (p. 39 a 44)

1. **Correlación de Pearson con el objetivo menor que 0,001** en valor absoluto: se eliminan **27 variables** (Tabla 3: por ejemplo Open_XRP_LogRet −0,0009; BTC/ETH_Ratio_720m −0,0009; ETH_30m_VolEMA 0,0008; MACD_26_12_9 0,0000), quedando 87.
2. **Prueba F univariante** (α = 0,05): se eliminan **24 más**, dejando **63** variables de las 115 iniciales.
3. **Eliminación recursiva de variables (RFE)** con estimador de regresión lineal: elige **8 variables** (ranking 1: BTC_15m_EMA/Close, Close_LTC_LogRet, BTC_15m_EMA_pctchange, BTC_240m_EMA_pctchange, BTC_LTC_ratio_LogRet, Close_BTC_LogRet, BTC_60m_EMA_pctchange y BTC_120m_EMA_pctchange); se considera insuficiente y se construyen conjuntos con las **20 y 30 variables de mejor ranking** (Tabla 4); el de 50 variables no se pudo ejecutar (cómputo). (La ficha anterior mencionaba conjuntos de 10, 20 y 30 variables; el de 10 se cita en el texto de resultados.)
- Observación: el umbral de 0,001 es tan bajo que solo elimina variables con correlación prácticamente nula; el texto no reporta la correlación máxima que sí se conserva.

## A4. Diseño de la validación (p. 44 a 48)

- **Partición:** 80 % entrenamiento (**35 607** observaciones) y 20 % evaluación (**8 902**); el orden temporal se conserva en la partición principal (se construyen primero los **bloques de predicción**: ventana de p minutos como entrada y el objetivo f = 5 minutos después; los bloques se solapan, con paso de 1 minuto).
- **Validación cruzada de 5 pliegues** sobre el entrenamiento: validación de **7 121** observaciones (16 % del total) y entrenamiento de **28 486**. **La reordenación (barajado) de las observaciones se hace dentro de la validación cruzada** ("no se ha incorporado en la separación de entrenamiento y evaluación… sino en la validación cruzada"), es decir, **se barajan bloques que se solapan en 59 de 60 minutos**; la autora reconoce la crítica de López de Prado (2018, 2021) sobre la validación cruzada en finanzas y la técnica "purgada" y la descarta con el argumento de que el solapamiento ocurre en menos del 1 % de las observaciones entre validación y evaluación (el solapamiento **dentro** del entrenamiento y la validación sí es casi total y no se trata).
- **Arquitectura base:** **una sola capa LSTM** con dropout y normalización por lotes y una capa densa de una unidad con activación lineal (no se prueba ReLU porque no puede producir valores negativos).
- **Optimización de hiperparámetros por fases** (por cómputo): se reducen los conjuntos de entrenamiento y validación **al 20 % de su tamaño**; el espacio completo de 9 721 combinaciones × 5 pliegues × 10 épocas = 486 050 iteraciones no se pudo ejecutar; se opta por **5 fases** con un solo parámetro o dos a la vez, eligiendo el valor de menor pérdida media (MSE) de validación cruzada (Tabla 5, valores probados: unidades 64, 128, 256; dropout 0,01, 0,1, 0,2; tasa de aprendizaje 0,001, 0,01, 0,1; optimizador Adam, SGD, RMS; lote 32, 64, 128, 256; tamaño de bloque 10, 15, 30, 60, 120, 240; escalado MinMax(0,1), MinMax(−1,1), Estándar, Robusto, Cuantil).
- **Tablas de pérdida media de validación (MSE):**
  - Fase 1: unidades 64 → 0,002048; **128 → 0,001794**; 256 → 0,002701; dropout 0,01 → 0,002828; 0,1 → 0,001871; **0,2 → 0,001843**; tasa 0,001 → 0,002348; **0,01 → 0,002024**; 0,1 → 0,002171 (se elige 0,01 aunque 0,1 y 0,01 son casi iguales; la elección de 0,2 de dropout con 0,1 casi igual se justifica "para minimizar el sobreajuste").
  - Fase 2: optimizador SGD 0,005378, RMS 0,004854, **Adam 0,001969**; lote 32 0,003096, 64 0,003839, 128 0,003725, 256 0,005609 (con Adam: 32 → 0,002790; **64 → 0,001507**; 128 → 0,001614; 256 → 0,001966; **se elige 64** porque 32 es el peor con Adam).
  - Fase 3 (bloque): 10 → 0,002801; 15 → 0,001960; 30 → 0,001922; **60 → 0,001474**; 120 → 0,002595; 240 → 0,003220.
  - Fase 4 (escalado, Tabla 10): MinMax(0,1) 0,002170; **MinMax(−1,1) 0,001688**; Estándar 0,003640; Robusto 0,004921; Cuantil 0,003212. El escalado se ajusta solo con el entrenamiento (para evitar el sesgo de anticipación, Chan, 2021; Jiang, 2020 sobre normalizar por ventanas).
  - Fase 5 (épocas): una sola ejecución de **50 épocas** (Tabla 11); la pérdida de validación mínima (5×10⁻⁶) aparece en la época 50 pero se observa una cercana en la época 19 y un pico anómalo en las épocas 23 a 25 (hasta 3,85×10⁻⁴); se elige **20 épocas**.
- **Valores finales (Tabla 12):** **128 unidades, dropout 0,2, tasa de aprendizaje 0,01, Adam, lote 64, bloque de 60 minutos, MinMax(−1,1), 20 épocas.**
- La propia autora advierte que la sensibilidad a los parámetros (que cualquier otro valor degrade el rendimiento) es indicio de sobreajuste y de sesgo de espionaje de datos (Chan, 2021).

## A5. Referentes y resultados (p. 59 a 62)

- **Referentes:** (1) variación nula (retorno cero; random walk); (2) **media ingenua** (retorno medio del entrenamiento, −1,9×10⁻⁵; Greaves y Au, 2015); (3) regresión lineal. (El texto dice 4 modelos base y describe tres.)
- **Métricas** sobre el **retorno logarítmico**: error medio (ME), RMSE y error absoluto medio (MAE); el cálculo sobre retornos hace válida la comparación (a diferencia de métricas sobre precios en logaritmo, que Mudassir y otros, 2020, señalan como engañosas).
- **Tabla 13 completa** (conjunto de evaluación; entre paréntesis el número de variables):

| Arquitectura | ME | RMSE | MAE |
|---|---|---|---|
| Variación nula (20 y 30) | −0,000031 | 0,002236 | 0,001479 |
| Media ingenua (20 y 30) | −0,000013 | 0,002236 | 0,001478 |
| Regresión lineal (20) | −0,00642 | 0,061574 | 0,002133 |
| Regresión lineal (30) | −0,006545 | 0,614392 | 0,008012 |
| LSTM (20) | −0,000033 | 0,002257 | 0,001500 |
| LSTM (30) | −0,00376 | 0,002414 | 0,001671 |
| GRU (20) | 0,001595 | 0,002791 | 0,002125 |
| GRU (30) | −0,000505 | 0,002372 | 0,001640 |
| RNN simple (20) | 0,002479 | 0,003546 | 0,002820 |
| RNN simple (30) | 0,029242 | 0,031784 | 0,031220 |

- **Lectura de los números:** el RMSE de la variación nula (0,002236) equivale a la desviación típica de los retornos a 5 minutos de la muestra de evaluación (MSE = 5,0×10⁻⁶). La relación LSTM(20)/ingenuo = 0,002257/0,002236 = 1,009 (el LSTM es 0,9 % peor). La regresión lineal tiene RMSE de 0,0616 y 0,614 (de 27 a 275 veces el del ingenuo) por predicciones extremas (variables colineales).
- **Diagnóstico gráfico (Gráfico 2):** las predicciones de LSTM y GRU se concentran en un rango muy estrecho cerca de 0, mucho menor que el de los retornos reales, por lo que "en la práctica está prediciendo prácticamente un mismo valor de manera continua", igual que los referentes.
- **Resultado:** el LSTM (20 variables) es mejor que las otras redes pero **peor que la variación nula y la media ingenua**; con 20 variables mejora a 30; la regresión lineal y la RNN simple no son adecuadas.

## A6. Conclusiones y recomendaciones de la autora (p. 63 y p. 64)

No puede afirmarse capacidad predictiva superior a la del paseo aleatorio ni a la media ingenua; posibles causas: datos de alta frecuencia en un mercado volátil, limitación de cómputo (2 % de los datos); recomienda más datos, optimización completa (no por fases), más indicadores (bandas de Bollinger) y selección multivariante de variables sin reducción univariante previa.

## A7. Lectura crítica para la tesis (se suma a la ficha)

1. **Es el resultado negativo más limpio de la carpeta** y respalda la regla del proyecto de comparar siempre contra el retorno cero; coincide con el resultado de E20 de que a horizontes cortos con retornos hay poco que ganar.
2. **Limitaciones que debilitan la conclusión:** un solo mes (enero de 2022, régimen bajista), una sola capa LSTM con 128 unidades, sin ventana móvil, validación cruzada barajada con bloques solapados (que puede sesgar la selección de hiperparámetros), selección de variables con correlación lineal, optimización con el 20 % de los datos y **ausencia de pruebas de significación (Diebold y Mariano)**: con 8 902 puntos y una diferencia relativa de 0,9 % no se puede decir que el LSTM sea "peor", solo que no mejora.
3. **Métrica no direccional:** no se calcula la exactitud de dirección ni el AUC; un LSTM con salida casi constante podría tener alguna señal de dirección no capturada por RMSE (la memoria del proyecto indica AUC .54–.55 en 1–2 horas con otros métodos).
4. **Tabla 11:** pérdida de entrenamiento de 0,0498 en la época 1 y de 10⁻⁵ después; el entrenamiento llega a niveles inferiores al del predictor constante (5×10⁻⁶ ≈ 2,2×10⁻³ de RMSE), consistente con datos escalados por MinMax(−1,1) cuya varianza es menor (el MSE de entrenamiento está en la escala del objetivo escalado, no en retornos); **no es comparable directamente con la Tabla 13** (los valores no se reescalan en la tabla de épocas), de modo que la equivalencia con el predictor constante debe verificarse con el código.

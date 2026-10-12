# Classical and quantum reservoir computing: development and applications in machine learning

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 16, 37 a 41, 54 a 65, 70, 99 a 114 y 255 a 258 de 295; **no leídos** los capítulos 4 y 5 sobre ecuación de Schrödinger y reservorios cuánticos, ni los apéndices)

| Campo | Valor |
|---|---|
| Título exacto | Classical and quantum reservoir computing: development and applications in machine learning |
| Autora | Laia Domingo Colomer (Máster en Fundamental Principles of Data Science) |
| Directores | Florentino Borondo Rodríguez y Javier Borondo Benito |
| Tipo / Venue / Año | Tesis doctoral, Universidad Politécnica de Madrid, Escuela Técnica Superior de Ingeniería Agronómica, Alimentaria y de Biosistemas, Grupo de Sistemas Complejos, 2023; versión en arXiv:2310.07455v1 [quant-ph], 11 de octubre de 2023 |
| Archivo local | `2310.07455v1.pdf` |
| URL / DOI | arXiv:2310.07455 (sin DOI de revista en el documento) |
| Métodos | Computación de reservorio (red de estado de eco) con variantes: ensamble, descomposición tendencia-estacionalidad-residuo, "next generation" y auto-reservorio; regresión de cresta; comparación con LSTM y SARIMA; además redes neuronales y reservorios cuánticos |
| Datos del capítulo relevante | Precios semanales de calabacín, berenjena y tomate en el sureste de España, marzo de 2013 a marzo de 2022; 16 variables regresoras de producción y comercio |

## Aporte clave

Para esta tesis interesa sobre todo el **capítulo 3**: aplica la computación de reservorio a series temporales cortas, volátiles y dependientes de factores externos, y muestra que un reservorio con **descomposición de la serie** supera a SARIMA y a una red LSTM (p. 99 a 112 y p. 256). Además propone una métrica, la **exactitud de dirección del mercado (Market Direction Accuracy, MDA)**, para no premiar a modelos que simplemente repiten el valor anterior.

## Conocimiento extraído (HECHO, con página del PDF)

**Teoría de reservorios (capítulo 2.3)**
- Un reservorio tiene entrada, estados internos y salida; solo la matriz de salida se entrena y se resuelve con regresión lineal (p. 54 a 56). Ecuación de actualización con tanh (ecuación 2.10, p. 56).
- Propiedad de eco: los estados quedan determinados por el historial de entradas y salidas, y no dependen del estado inicial. Se ilustra con un ejemplo de ondas senoidales (p. 57 a 59).
- Condiciones suficientes: si el mayor valor singular de W es menor que 1 hay estados de eco; si el radio espectral es mayor que 1 no los hay para entradas que incluyen el cero. **Son demasiado restrictivas**: existen redes con estados de eco aun con valores singulares mayores que 1 (p. 59 y p. 60).
- El radio espectral controla la memoria: radios altos dan memoria más larga (p. 60 y p. 61).
- Reservorios grandes tienden a dar mejores resultados pero con más coste y **más riesgo de sobreajuste** (p. 61).
- Hay que descartar los primeros t_min pasos como transitorio (p. 62).
- **Tasa de fuga α:** da más memoria de pasado lejano (p. 63 y p. 64).
- **Regresión de cresta con parámetro γ:** si γ es demasiado grande el modelo predice valores casi constantes; si es muy pequeño aumenta el sobreajuste (p. 64). Es la misma lógica que observé con la fuerza de regularización de la lectura de E20.
- Otras mejoras: ruido en la salida de entrenamiento, entrada constante y lectura cuadrática (p. 64 y p. 65).
- **Comparación con redes recurrentes:** el reservorio tiene muchos menos parámetros entrenables que una red recurrente (p. 70).

**Predicción de precios agrícolas (capítulo 3)**
- **Problema:** conjuntos pequeños. Entrenamiento hasta diciembre de 2019 (356 puntos), validación en 2020 (53) y prueba desde enero de 2021 (62). Escala lineal a [−1, 1]. La validación elige los hiperparámetros y la prueba evalúa (p. 102 y p. 103).
- **Cinco variantes de reservorio comparadas con LSTM (128 neuronas, 5 000 épocas) y SARIMA(0,0,1)(1,0,1,45)** (p. 103 a 106):
  - S-RC: reservorio estándar.
  - E-RC: **ensamble** de muchos reservorios con las mismas características y promedio de sus predicciones, para depender menos de la realización aleatoria cuando hay pocos datos.
  - D-RC: descomposición en tendencia, estacionalidad y residuo, y un ensamble para cada componente; la suma da la predicción. Se comprobó la estacionariedad del residuo con la prueba de Dickey y Fuller aumentada (valores p entre 10⁻¹¹ y 10⁻¹⁴).
  - NG-RC: "next generation", sin matrices aleatorias, solo retardos y productos de retardos.
  - ARNN-RC: auto-reservorio sobre las variables regresoras.
- **Resultados en la prueba para el calabacín** (Tabla 3.2, p. 108): error absoluto medio de 0,089 con D-RC, frente a 0,154 con LSTM y 0,160 con SARIMA; MDA de 77,4 % con D-RC, frente a 37,7 % con LSTM y 45,3 % con SARIMA. Para berenjena y tomate el D-RC también es el mejor (MDA 69,8 % y 70,4 %; tablas 3.3 y 3.4, p. 108 y p. 109).
- **Tendencia general:** el D-RC es el único que baja de 0,10 de error en las tres series; E-RC y S-RC quedan entre 0,11 y 0,13; el NG-RC rinde como los referentes (p. 109 y p. 110). El ensamble es mucho más robusto frente a la elección de las matrices aleatorias (p. 109).
- **La MDA** (p. 110 y p. 111): clasifica el cambio semanal como subida, bajada o constante con un umbral de ±0,05 €/kg; un modelo al azar acierta cerca de 33 %. **El texto advierte de un error común:** en series muy autocorrelacionadas, repetir el valor anterior da un error pequeño aunque el modelo no anticipe ningún cambio, y métricas como el error absoluto medio, el R² o el error relativo no lo detectan (p. 101 y p. 110).
- **Interpretación del período de validación (2020):** el error absoluto fue peor por el choque de la pandemia, pero la MDA se mantuvo; el reservorio sigue la tendencia aunque no prediga niveles extremos nunca vistos (p. 111).
- **Intervalos de confianza:** propone estimarlos modelando la distribución del error del D-RC por separado según si el modelo predice subida, bajada o constante; el error es mucho menor en el conjunto "constante" y los conjuntos de subida y bajada están sesgados, porque el modelo subestima los cambios grandes (p. 113 y p. 114).
- **Conclusiones de la autora** (p. 256 y p. 257): hay que evaluar la dirección además del error; el reservorio con descomposición supera a LSTM y SARIMA; los modelos multivariantes mejoran a los univariantes.

## Limitaciones y críticas

- Declarado por la autora: faltan modelos precisos de intervalos de confianza (se dejan para trabajo futuro) (p. 256).
- **[OPINIÓN]** El conjunto de prueba tiene solo 62 puntos semanales y no se hace una prueba estadística de la diferencia entre modelos; MDA 77 % frente a 45 % con 62 puntos y un solo periodo de prueba es una diferencia grande pero sin intervalo.
- **[OPINIÓN]** Son precios de verduras, con estacionalidad fuerte; la autora afirma que las conclusiones se extienden a series con propiedades parecidas (p. 112), pero no lo prueba con Bitcoin. La estacionalidad es lo que explota la descomposición; en Bitcoin diario no hay estacionalidad comparable.
- **[OPINIÓN]** El LSTM no usa las variables externas, por lo que la comparación con el reservorio no es de igual a igual en información (el propio texto lo dice: "no considera factores externos", p. 102).
- No se leyeron los capítulos cuánticos; no se puede afirmar nada sobre ellos.

## Conexión con mi tesis (red E20)

- **Coincide con el hallazgo de que repetir el valor anterior engaña:** la advertencia sobre la autocorrelación y la métrica MDA justifican comparar E20 con referentes de persistencia y de media móvil, y no solo con error cuadrático.
- **Ensamble de reservorios:** el E-RC reduce la dependencia de la realización aleatoria; apoya reportar E20 sobre varias semillas de red (en mi fase 2 usé 8 semillas) y sugiere un ensamble de semillas como mejora barata.
- **Regularización de la lectura:** el efecto de γ (demasiado grande, predice constantes; demasiado pequeño, sobreajusta) es el mecanismo que expliqué para C=3e-5 frente a 1e-3 en E20.
- **Memoria y tasa de fuga:** da la base para E21 (más memoria con constantes de tiempo largas), aunque en BTC real E21 no superó a la media móvil.
- **Descomposición de la serie:** idea candidata para BTC (separar tendencia, ciclos y residuo antes de alimentar al reservorio). **[OPINIÓN]** No está probada en Bitcoin; habría que preregistrarla como hipótesis.
- **Límite para citarlo:** series agrícolas semanales, no financieras.

## Referencias que cita y conviene localizar

Jaeger (2001), echo state networks; Maass, Natschläger y Markram (2002), liquid state machines; Gauthier y colaboradores (2021), next generation reservoir computing; Ma y colaboradores (2014) y Chen y colaboradores (2020), auto-reservorio (ARNN-RC); Pathak y colaboradores (2017, 2018), predicción de sistemas caóticos con reservorios y lectura cuadrática; Hoerl y Kennard (2012), regresión de cresta; Gneiting y Katzfuss (2014), predicción probabilística; Dickey y Fuller (1979); Domingo y colaboradores (2023c), el artículo de precios agrícolas en el que se basa el capítulo 3. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (ecuaciones, datos, tablas y resumen de los capítulos cuánticos)

Contenido técnico de la **teoría de reservorios (cap. 2.3, p. 54 a 70 del PDF)**, el **capítulo 3 completo (predicción de series; p. 99 a 114 y hasta la p. 115 con intervalos de confianza y análisis multivariante)**, la **sección 5.3 (reservorio cuántico para series temporales)** y las **conclusiones (p. 255 a 260)**. Los capítulos de teoría de redes neuronales y de mecánica cuántica (2.1, 2.2 y 2.4), el capítulo 4 (ecuación de Schrödinger) y las secciones 5.1, 5.2 y 5.4 (diseño óptimo, ruido y fármacos) son de física y química cuánticas: **se resumen con sus conclusiones (A6) y no se reproducen sus derivaciones ni tablas**; los apéndices no se han leído. Páginas = páginas del PDF (PDF = numeración interna + 28).

## A1. Reservorio de eco: formulación de la tesis (cap. 2.3)

- **Arquitectura:** entrada u⃗ ∈ R^K, estados internos x⃗ ∈ R^N y salida y⃗ ∈ R^L; matrices **W_in (N×K), W (N×N, el reservorio), W_back (N×L, realimentación) fijas** y **W_out** entrenable (solo conectada a los estados internos en la tesis).
- **Dinámica:** x⃗(t) = f( W_in·u⃗(t) + W·x⃗(t − 1) + W_back·y⃗(t − 1) )  (2.10), con f = tanh; salida y⃗(t) = f_out[ W_out·x⃗(t) ]  (2.11), con f_out = identidad.
- **Estados de eco** (Definición 1): x⃗(t) = E(…, u⃗(t − 1), u⃗(t), …, y⃗(t − 1), y⃗(t))  (2.12); propiedades de **olvido del estado** y de **olvido de la entrada y de la salida** (equivalentes a la definición); ejemplo con u(t) = sin(t/5) e y_teach = ½·sin⁷(t/5) (2.13 y 2.14), con inicializaciones distintas (ceros, unos, uniforme U(−0,5; 0,5)) cuyas trayectorias convergen.
- **Condiciones suficientes:** (1) si el mayor valor singular de W es σ_max < 1 hay estados de eco para todo u, y, x ∈ [−1, 1]^N; (2) si el radio espectral |λ_max| > 1 no hay estados de eco con entrada que contenga 0 y A = [−1, 1]^N. **Son demasiado restrictivas** (hay redes con estados de eco con valores singulares > 1 cuando la entrada y la salida no son 0 en ningún paso); el radio espectral controla la **memoria**; si |λ_max| ≫ 1 puede no haber estados de eco.
- **Entrenamiento (4 pasos):** (1) generar W, W_in y W_back al azar (**W dispersa e inhomogénea**, entradas distintas de cero en {a, −a} con igual probabilidad y a elegido para el radio espectral deseado; W_in y W_back densas); reservorios grandes dan mejores resultados con **más riesgo de sobreajuste** y coste; (2) actualizar los estados **con forzado del maestro** (teacher forcing): x⃗(t) = f(W_in·u⃗(t) + W·x⃗(t − 1) + W_back·y⃗_teach(t − 1))  (2.18); (3) **descartar un transitorio de t_min estados**; (4) hallar W_out minimizando MSE = (1/(T − t_min))·Σ_{t=t_min}^{T} [ f_out⁻¹(y⃗_teach(t)) − W_out·x⃗(t) ]²  (2.19) por regresión lineal. **Predicción:** el reservorio evoluciona de forma autónoma realimentando su propia salida.
- **Mejoras:** **tasa de fuga α ∈ (0, 1]:** x̃ = f(…), x = (1 − α)·x(t − 1) + α·x̃  (2.20 y 2.21) (la tesis indica que "α cercano a 1 conserva más información del pasado lejano", lo contrario de la convención habitual de la tasa de fuga; verificar); **regresión de cresta** MSE_r = MSE + γ·‖W_out‖²  (2.22) (γ grande predice casi constantes; γ pequeño reproduce 2.19 y sobreajusta); **ruido en el objetivo** y⃗_teach → y⃗_teach + ν⃗(t), ν ∼ U(−b, b)  (2.23); **entrada constante** u⃗ = c⃗ cuando no hay variables explicativas; **modelo cuadrático** y⃗ = W_out·(x⃗; x⃗²)  (2.24) (Pathak y otros, 2017 y 2018).
- **Ejemplos (p. 66 a 70):** serie periódica con N = 200, 5 % de conectividad, radio espectral 0,3 (falla por inestabilidad), 1,3 (óptimo en prueba) y con α = 0,8, ruido U(−0,1; 0,1) y γ = 0,01 (predicciones cercanas); **homogeneidad y densidad (Tabla 2.1, MSE de prueba): inhomogéneo y disperso 0,0032; inhomogéneo y denso 0,13; homogéneo y disperso 0,017; homogéneo y denso 0,060** (la dispersión es crucial; la inhomogeneidad algo menos). Ecuación del calor yₜ = ½·y_zz con y(z, 0) = sin z (solución sin z·e^{−t}); N = 400, 2 % de conectividad, radio 0,9, t_step = 500, t_min = 200; el MSE baja de 0,13 a 1×10⁻⁶ con ruido de 0,001, γ = 10⁻¹² y entrada constante.
- **Reservorio frente a RNN:** el reservorio tiene muchos menos parámetros entrenables (solo un modelo lineal) y necesita menos datos.

## A2. Capítulo 3: predicción de precios agrícolas (p. 99 a 114)

- **Datos:** precios en origen en España (subastas) de **calabacín, berenjena y tomate**, euros por kilogramo, **agregados semanalmente** (media semanal), de **marzo de 2013 a marzo de 2022**; entrenamiento hasta diciembre de 2019 (**356 puntos**), validación 2020 (**53**), prueba desde enero de 2021 (**62**); escala lineal a [−1, 1]; **16 variables regresoras** de volúmenes de producción y comercio internacional (nueve en el reservorio cuántico). El periodo incluye el confinamiento de la pandemia.
- **Modelos:** S-RC (reservorio estándar); **E-RC** (ensamble de N_e reservorios con los mismos hiperparámetros y promedio de las predicciones, para reducir la dependencia de la realización aleatoria cuando hay pocos datos); **D-RC** (descomposición **aditiva** en tendencia, estacionalidad y residuo; un E-RC por componente; la predicción es la suma; la prueba de Dickey y Fuller aumentada del residuo da valores p de 3×10⁻¹¹ (calabacín), 2×10⁻¹⁴ (berenjena) y 3×10⁻¹⁴ (tomate)); **NG-RC** (Gauthier y otros, 2021; sin matrices aleatorias: retardos k y productos de retardos; óptimo k = 3 y γ = 0,56; con serie unidimensional solo términos y(t)·y(t − k)); **ARNN-RC** (Chen y otros, 2020; auto-reservorio que mapea las variables regresoras futuras a la serie; no tiene predicción en entrenamiento).
- **Hiperparámetros óptimos (Tabla 3.1; α, N, γ, ρ(W), densidad D(W), N_e):** S-RC 0,81, 120, 2,6, 0,52, 0,012, –; E-RC 0,98, 80, 0,51, 1,4, 0,011, 240; D-RC tendencia 0,58, 60, 0,011, 1,1, 0,016, 80; D-RC estacionalidad 0,74, 20, 0,011, 0,32, 0,023, 100; D-RC residuo 0,91, 60, 7,24, 0,85, 0,022, 120; ARNN-RC –, 30, –, 0,50, 0,03, –; t_dismiss = 10, f = tanh, f_out = identidad. **Referentes:** LSTM de 128 neuronas con 5 000 épocas y SARIMA(0,0,1)(1,0,1)₄₅.
- **Métrica MDA (Market Direction Accuracy):** el cambio semanal se clasifica en +1 (subida si > +0,05 €/kg), −1 (bajada) o 0 (constante); un modelo al azar acierta ≈ 33 %; la tesis explica que un modelo que repite el precio anterior tiene bajo error absoluto y R², por lo que hace falta una métrica robusta a la autocorrelación.
- **Tablas 3.2, 3.3 y 3.4 (error absoluto medio / MDA; entrenamiento, validación y prueba):**

| Calabacín | MAE ent. | MAE val. | **MAE prueba** | MDA ent. | MDA val. | **MDA prueba** |
|---|---|---|---|---|---|---|
| LSTM | 0,217 | 0,199 | 0,154 | 0,414 | 0,455 | 0,377 |
| SARIMA | 0,124 | 0,213 | 0,160 | 0,505 | 0,523 | 0,453 |
| S-RC | 0,123 | 0,214 | 0,141 | 0,586 | 0,545 | 0,604 |
| E-RC | 0,128 | 0,166 | 0,123 | 0,617 | 0,705 | 0,604 |
| **D-RC** | 0,135 | 0,132 | **0,089** | 0,563 | 0,795 | **0,774** |
| NG-RC | 0,167 | 0,182 | 0,150 | 0,476 | 0,605 | 0,463 |
| ARNN-RC | – | 0,197 | 0,122 | – | 0,659 | 0,529 |

| Berenjena | MAE val. | **MAE prueba** | MDA val. | **MDA prueba** |
|---|---|---|---|---|
| LSTM | 0,194 | 0,153 | 0,364 | 0,372 |
| SARIMA | 0,214 | 0,151 | 0,500 | 0,509 |
| S-RC | 0,171 | 0,129 | 0,705 | 0,623 |
| E-RC | 0,157 | 0,117 | 0,636 | 0,660 |
| **D-RC** | 0,141 | **0,090** | 0,659 | **0,698** |
| NG-RC | 0,180 | 0,182 | 0,535 | 0,481 |
| ARNN-RC | 0,185 | 0,121 | 0,545 | 0,549 |

| Tomate | MAE val. | **MAE prueba** | MDA val. | **MDA prueba** |
|---|---|---|---|---|
| LSTM | 0,127 | 0,177 | 0,500 | 0,333 |
| SARIMA | 0,124 | 0,138 | 0,545 | 0,389 |
| S-RC | 0,106 | 0,114 | 0,636 | 0,574 |
| E-RC | 0,105 | 0,123 | 0,727 | 0,574 |
| **D-RC** | 0,094 | **0,093** | 0,659 | **0,704** |
| NG-RC | 0,128 | 0,162 | 0,488 | 0,364 |
| ARNN-RC | 0,126 | 0,131 | 0,481 | 0,545 |

  (El MAE de entrenamiento de berenjena y tomate es de 0,086 a 0,185, con el D-RC en 0,120 y 0,091; la MDA de entrenamiento del D-RC es 0,563, 0,654 y 0,614.)
- **Interpretación de la autora:** el D-RC es el único con MAE < 0,10 en las tres series; E-RC y S-RC entre 0,11 y 0,13 (el ensamble es mucho más robusto a la elección de las matrices); el NG-RC rinde como los referentes (tomate: 0,16, 78 % por encima del D-RC); en calabacín el D-RC acierta el cambio en **77,4 % frente a 45,3 % (SARIMA) y 37,7 % (LSTM)**, 1,7 y 2,1 veces; el error de validación (2020) es peor por la pandemia pero la MDA se mantiene.

## A3. Intervalos de confianza y análisis multivariante (p. 112 a 116)

- **Intervalos con la distribución del error del D-RC:** el error de entrenamiento ε(t) = y_teach(t) − y(t) se separa en tres conjuntos según el cambio relativo **predicho**: **Aumento** (≥ +10 %), **Disminución** (≤ −10 %) y **Constante** (−10 % a +10 %) (ecuación 3.1); el error es mucho menor en "Constante" y sesgado en los otros dos (el modelo subestima los cambios grandes). Se ajusta una distribución **normal inversa gaussiana (NIG)** a cada conjunto (parámetros: Constante a = 0,12, b = −0,048, x₀ = 0,0069, σ = 0,051; Aumento a = 1,36, b = 0,22, x₀ = −0,083, σ = 0,20; Disminución a = 1,66, b = −0,25, x₀ = 0,056, σ no impreso en la extracción); intervalos al 90, 80, 70 y 60 %; **ancho medio 0,46 €/kg al 90 % y 0,20 €/kg al 60 %** (con gaussiana, 0,25 al 60 %). Limitación: no usa las variables regresoras. Propuesta futura: lectura de red neuronal de tres capas con pérdida orientada a la calidad del intervalo (Hu y otros, 2020, potencia eólica).
- **Multivariante:** siete variedades de pimiento (California rojo, amarillo y verde; italiano verde y rojo; lamuyo rojo y verde), precios semanales de 2013 a 2021: los D-RC multivariantes superan a los individuales (conclusión 4 de la tesis; las cifras no se reprodujeron aquí).

## A4. Reservorio cuántico para series temporales (sección 5.3, p. 221 a 229)

- **Tarea:** predecir el calabacín semanal con la misma partición; escala [0, 1]; nueve regresoras opcionales; **7 qubits** (óptimo entre 2 y 8, Figura 5.15); entrada secuencial: ρ(t) = |y(t)⟩⟨y(t)| ⊗ Tr_n(ρ(t − Δt)) (traza parcial sobre el primer qubit; el estado se vuelve mixto); evolución unitaria U hasta t + Δt; **características** x̂(t) = (⟨X₁⟩, ⟨Z₁⟩, …, ⟨X_N⟩, ⟨Z_N⟩) con N_v = 2 pasos intermedios (dimensión 2N × N_v = **28**); lectura con **regresión de cresta** (γ = 10⁻¹⁰ sin variables externas y γ = 0,1 con ellas); **ocho familias de circuitos** (G1, G2, G3, MG, D2, D3, Dn y el modelo de Ising) con **100 simulaciones** por familia; criterio de elección: **mayorización** (Vallejos y otros, 2021).
- **Resultados (Figuras 5.12 a 5.16):** G1 y G2 (grupo de Clifford, menos complejas) empeoran al añadir compuertas y con ≈ 100 compuertas la MDA baja a ≈ 38 % (azar) y el MAE iguala al de predecir la media; **G3 mejora con las compuertas y converge a MAE = 0,13 y MDA = 0,5 hacia 150 compuertas** (sin variables externas); MG óptimo con 40 compuertas pero difícil de implementar; el Ising requiere ≈ 9 000 compuertas G3 (30–70 veces más que el óptimo); con variables externas la diferencia G1–G3 baja de 0,23 a 0,003 €/kg en MAE y de 13 % a 3 % en MDA (las variables externas aportan la información clave) y G3 óptimo con 60 a 200 compuertas. Conclusión: la mayorización es buen indicador de rendimiento en pronóstico, **sobre todo sin variables externas**.
- **Observación:** el MDA óptimo del reservorio cuántico (0,5 sin variables externas) queda lejos del 77 % del D-RC clásico; no se compara con LSTM ni SARIMA en esta sección.

## A5. Resumen de los capítulos cuánticos (según las conclusiones, p. 255 a 260)

Cap. 4: una red totalmente conectada (1D) y una red convolucional (2D) resuelven la ecuación de Schrödinger independiente del tiempo con potenciales polinomiales aleatorios y generalizan a osciladores de Morse; con función de pérdida a medida se obtienen estados de alta energía del oscilador de Morse acoplado 2D; un **reservorio de valores complejos** (activación compleja y regresión de cresta compleja, aprendizaje de varios pasos) propaga funciones de onda en el tiempo y, con la transformada de Fourier, recupera energías propias y funciones propias de cuatro sistemas (oscilador armónico 1D y 2D, Morse 1D y polinomial 1D): **4–6 veces más rápido** que el integrador numérico; para el Morse acoplado 2D errores en energías < 1×10⁻³ y en funciones < 1×10⁻⁴ y **7–9 veces más rápido**; para el oscilador cuártico acoplado (caos cuántico) estados propios **8–15 veces** y cicatrices ("scars") **9–15 veces** más rápido. Cap. 5: siete familias de circuitos cuánticos (G1, G2, G3, MG, D2, D3, Dn) con energías de excitación de LiH y H₂O: las más complejas según la mayorización rinden más; G3 óptimo convergiendo hacia ≈ 200 compuertas (8 qubits) y 250 (10 qubits); ruido cuántico: con fidelidad final > 0,96 el ruido de **amortiguación de amplitud mejora** el resultado y los de despolarización y de amortiguación de fase siempre lo empeoran (priorizar corregir el de despolarización); red híbrida cuántico-clásica para afinidad de unión de fármacos (la primera capa convolucional sustituida por un reservorio cuántico G3 que se estabiliza con ≈ 300 compuertas, con **20 % menos de parámetros** y entrenamiento 20–40 % más rápido; mitigación de errores con p < 0,01 y 300 compuertas).

## A6. Lectura crítica para la tesis

1. **Útil para la metodología, no como evidencia en Bitcoin:** la métrica **MDA** y el aviso sobre repetir el valor anterior respaldan el uso de referentes de persistencia y de métricas de dirección; el **ensamble de reservorios** respalda reportar varias semillas o promediarlas; el resultado del NG-RC (≈ referentes) coincide con que un modelo lineal con retardos es un buen control.
2. **Riesgos del D-RC que la tesis no discute:** (a) la **descomposición en tendencia, estacionalidad y residuo** puede calcularse con toda la serie (incluido el periodo de prueba), lo que filtraría información futura; el texto no dice si se hace solo con el entrenamiento (verificar en el artículo original); (b) la **MDA de validación (0,795) supera a la de entrenamiento (0,563)** y los hiperparámetros se eligen en validación con solo 53 puntos; (c) la **prueba tiene 62 puntos**, sin intervalo de confianza para la MDA (con n = 62 el error estándar es ≈ 6 puntos) ni prueba de Diebold y Mariano; (d) los **precios agrícolas tienen estacionalidad fuerte** (el D-RC la explota), algo que no existe en Bitcoin; (e) el LSTM no usa las variables externas, de modo que no es una comparación de igual información; (f) el objetivo discretiza los cambios con un umbral de ±0,05 €/kg y no se compara contra la regla "predecir siempre constante".
3. **El reservorio cuántico simulado** reduce su MDA al azar con más compuertas en las familias poco complejas; no mejora al reservorio clásico en esta tarea.

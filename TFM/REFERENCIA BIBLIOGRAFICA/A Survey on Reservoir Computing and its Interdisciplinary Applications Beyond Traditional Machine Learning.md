# A Survey on Reservoir Computing and its Interdisciplinary Applications Beyond Traditional Machine Learning

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 7, 11 a 15, 27 a 28, 30 a 31 y 33 a 34 de 51; el resto son catálogos de aplicaciones físicas, químicas y de neurociencia)

| Campo | Valor |
|---|---|
| Título exacto | A Survey on Reservoir Computing and its Interdisciplinary Applications Beyond Traditional Machine Learning |
| Autores | Heng Zhang y Danilo Vasconcellos Vargas (Departamento de Ciencia e Ingeniería de la Información, Universidad de Kyushu, Japón) |
| Tipo / Venue / Año | Artículo de revisión. Publicado en IEEE Access (2023), DOI 10.1109/ACCESS.2023.3299296; preprint arXiv:2307.15092v1 (27 de julio de 2023) |
| Archivo local | `2307.15092v1.pdf` |
| Métodos | Revisión narrativa de computación de reservorio: redes de estado de eco (ESN), máquinas de estado líquido (LSM), técnicas de entrenamiento, reservorios físicos, aplicaciones y conexión con el cerebro |

## Aporte clave

Revisión unificada de la computación de reservorio (reservoir computing, RC): una red recurrente de neuronas conectadas al azar cuyas conexiones **no se entrenan**, y una capa de lectura simple que sí se entrena. La revisión explica la historia (Dominey, Jaeger, Maass, Verstraeten), las dos familias principales (ESN no espigantes y LSM espigantes), las técnicas de entrenamiento, los reservorios físicos y los problemas abiertos de diseño (p. 1 a 7 y p. 33).

## Conocimiento extraído (HECHO, con página)

**Definición y ventajas**
- RC transforma una entrada de baja dimensión en un espacio de alta dimensión con una red recurrente fija; una lectura lineal produce la respuesta. Ventajas citadas: entrenamiento rápido, implementación sencilla, bajo coste y sin problemas de gradiente que desaparece o explota (p. 1 y p. 2).
- Las cuatro propiedades que un reservorio debe cumplir: alta dimensión, no linealidad, propiedad de separación y memoria que se desvanece (fading memory, equivalente a la propiedad de eco) (p. 31).

**ESN frente a LSM**
- Las ESN usan neuronas **no espigantes** de tiempo discreto con fuga; las LSM usan neuronas espigantes de integración y disparo y son más plausibles biológicamente y más adecuadas para chips neuromórficos (p. 4 a 6).
- Ecuaciones de la ESN con tasa de fuga α: actualización tanh(W_in·u + W·x) y mezcla (1 − α)·x_anterior + α·actualización (ecuaciones 1 y 2, p. 4).
- Las LSM requieren la propiedad de separación y la de aproximación (p. 6).

**Lectura (readout)**
- La lectura clásica es regresión de cresta (ridge) con factor de regularización β; una vez recogidos los estados, β se puede ajustar sin volver a ejecutar la red (ecuación 7, p. 7). La revisión añade que la regresión de cresta suele bastar si el reservorio aporta dinámica no lineal rica.
- Otras técnicas de entrenamiento: mínimos cuadrados recursivos, aprendizaje FORCE, gradiente en línea, algoritmos evolutivos, y plasticidad biológica (Hebb, plasticidad dependiente del tiempo de los disparos STDP, plasticidad intrínseca) (Tabla 1, p. 7).

**Propiedad de eco y radio espectral**
- Un radio espectral menor que 1 se usa mucho para garantizar la propiedad de eco, pero Yildiz y colaboradores (2012) demostraron que **no es ni necesario ni suficiente**; el supuesto "borde del caos" es en realidad el borde de la propiedad de eco (p. 5).

**Limitaciones de la ESN simple**
- Los pesos fijos al azar pueden limitar el rendimiento. **El rendimiento se satura al aumentar el tamaño del reservorio**: solo agrandarlo no mejora (p. 6). Esto motivó reservorios múltiples y ESN profundas.
- **ESN profunda (DeepESN, 2016):** apila reservorios para obtener varias escalas de tiempo; las capas más altas capturan frecuencias más bajas y las perturbaciones duran más en ellas (ecuaciones 15 a 17, p. 12). Se explica que un reservorio único maneja mal varias escalas de tiempo a la vez.
- Lectura no lineal polinómica y topología de mundo pequeño (small-world) como variantes (p. 13).

**Plasticidad**
- La STDP en LSM puede mejorar la propiedad de separación con datos reales de voz, y se desarrollaron versiones que reducen la memoria necesaria (p. 11).
- La plasticidad intrínseca ajusta la excitabilidad de las neuronas del reservorio, sobre todo para preentrenar y optimizar (p. 11).

**Finanzas (sección 5.9)**
- Predicción bursátil a corto plazo con ESN, usando el exponente de Hurst para elegir una subserie persistente con la mayor predecibilidad para entrenar (referencia [281] de la revisión) (p. 27).
- Tres estructuras de RC para precio de acciones, incluida la de mundo pequeño (referencia [250]) (p. 27).
- Modelado de sistemas financieros con ESN (referencia [251]) (p. 27). La revisión **no incluye resultados cuantitativos ni menciona Bitcoin** (la palabra no aparece en el texto).

**Problemas abiertos**
- No hay guías completas para diseñar reservorios; lo disponible se extrae de estudios experimentales de perfiles de escala de tiempo y espectros de frecuencia (Jaeger, citado en p. 33). Se menciona el meta-aprendizaje de hiperparámetros del reservorio (learning-to-learn) con BPTT (p. 33).
- Falta de herramientas: citan EchoTorch (primer paquete de Python para ESN, 2018), ReservoirComputing.jl, TensorFlow Addons con capa ESN y otros (p. 34).

## Limitaciones y críticas

- **[OPINIÓN]** Es una revisión amplia y multidisciplinaria; la parte financiera es muy breve y sin cifras. No sirve como evidencia empírica sobre predicción de Bitcoin, solo como marco conceptual y fuente de referencias.
- **[OPINIÓN]** Al ser narrativa, no declara criterios de inclusión de los estudios ni evalúa el sesgo de publicación.

## Conexión con mi tesis (red E20)

- **Marco conceptual de E20:** E20 es un reservorio de 1000 neuronas espigantes (familia LSM) con lectura lineal; esta revisión da el vocabulario y las propiedades (separación, fading memory) para describirla en el marco teórico.
- **Saturación con el tamaño:** coincide con mis resultados de que más neuronas o más conexiones no mejoran (apagar la recurrencia no empeoró en BTC real).
- **Radio espectral no determina nada:** respalda mi cautela de no atribuir el rendimiento a un ajuste del radio espectral, y de medir la recurrencia directamente (cociente corriente recurrente a entrada).
- **Escalas de tiempo múltiples:** la ESN profunda y la crítica al reservorio único para varias escalas son el antecedente teórico de E21 (constantes de tiempo multiescala).
- **Lectura ajustable sin reejecutar la red:** respalda mi procedimiento de volcar los estados y probar distintas lecturas (C=1e-3 frente a 3e-5) sobre los mismos estados.
- **Límite para citarlo:** no aporta evidencia financiera propia.

## Referencias que cita y conviene localizar

Jaeger (2001) y Jaeger (2012, sobre el supuesto borde del caos); Maass, Natschläger y Markram (2002); Verstraeten y otros (2007); Lukoševičius y Jaeger (2009), revisión de reservorios; Yildiz, Jaeger y Kiebel (2012), condiciones de la propiedad de eco; Gallicchio y Micheli (2017), DeepESN; Sussillo y Abbott (2009), FORCE; Dominey (1995); la serie sobre predicción bursátil con ESN y exponente de Hurst citada como [281]. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (modelos, ecuaciones, métodos de entrenamiento y catálogo de aplicaciones)

Contenido técnico de las secciones 1 a 7 (páginas 1 a 33 del PDF; las páginas 34 a 51 son referencias). Es una **revisión narrativa**, sin experimentos propios: los "datos" son los estudios que reseña. Páginas = páginas del PDF.

## A1. Historia y definición (p. 1 a 4)

- **RNN y sus problemas:** las redes recurrentes (RNN) tienen memoria pero sufren gradientes que desaparecen o explotan (BPTT, aprendizaje recurrente en tiempo real RTRL, LSTM de 1997). **Hitos:** prototipo corticoestriatal de Dominey (1995); aprendizaje recurrente de Atiya–Parlos (APRL, 2000; separa pesos de salida de ajuste rápido y pesos ocultos de ajuste lento) y retropropagación-descorrelación (BPDC, versión en línea); **ESN** (Jaeger) y **LSM** (Maass), a principios de los años 2000, unificadas como **computación de reservorio** (Verstraeten y otros).
- **Definición:** reservorio = red recurrente de neuronas conectadas al azar con pesos que **no se entrenan**; una capa de lectura (readout) simple, entrenada con regresión lineal, genera la respuesta; ventajas: entrenamiento rápido, sencillez, bajo coste y sin gradiente que explote; desventajas: el rendimiento depende de la inicialización aleatoria y de los hiperparámetros.

## A2. Red de estado de eco (ESN) (p. 4 y p. 5)

- Actualización: x̃(n) = tanh( W_in·u(n) + W·x(n − 1) )  (1); x(n) = (1 − α)·x(n − 1) + α·x̃(n)  (2), con α la **tasa de fuga**; lectura y(n) = W_out·x(n)  (3); con sesgo y entrada directa: u(n) → [1; u(n)] y x(n) → [1; u(n); x(n)]. Dimensiones: u ∈ R^{N_u}, x ∈ R^{N_x}, W_in ∈ R^{N_x×N_u}, W ∈ R^{N_x×N_x}.
- **Algoritmo 1:** (1) generar W_in y W al azar (uniforme U(−1, 1) habitual); (2) ejecutar con la señal de entrada y recoger los estados; (3) calcular la salida; (4) minimizar el MSE entre y(n) y la meta con regresión; (5) predecir con datos nuevos.
- **Propiedad de eco (ESP):** convergencia asintótica de los estados; el **radio espectral < 1** se usa mucho, pero Yildiz y otros (2012) demostraron que **no es ni necesario ni suficiente** ("no hay un beneficio general en escalar el radio espectral hacia el borde del caos"); se proponen nuevas condiciones suficientes; con entrada de escala adecuada el rango válido es mayor. El "borde del caos" es en realidad **el borde de la propiedad de eco** (Jaeger). Capacidad de memoria a corto plazo: resultados analíticos de Jaeger y Verstraeten.

## A3. Máquina de estado líquido (LSM) (p. 5 y p. 6)

- Reservorio ("líquido") 3D y local de neuronas de integración y disparo (IF) estimuladas por trenes de picos; x^M(t) = L^M·u(t)  (4) (filtro líquido); y(t) = f^M(x^M(t))  (5) (lectura sin memoria). Precondiciones: **propiedad de separación** (estados internos distintos para entradas distintas) y **propiedad de aproximación** (la lectura produce la meta); juntas equivalen a la memoria que se desvanece de la ESN.
- **Comparación:** la LSM es más plausible biológicamente y más adecuada para chips neuromórficos; la ESN admite más variantes. Limitaciones de la ESN: pesos fijos aleatorios y **saturación del rendimiento al aumentar el tamaño del reservorio**, lo que motiva reservorios múltiples (capas, paralelos) y optimización evolutiva o por gradiente.

## A4. Entrenamiento (sección 3; Tabla 1, p. 6 a 11)

- **Lectura clásica:** Y = W_out·X ≈ Y_target  (6); **regresión de cresta**: W_out = Y_target·Xᵀ·(X·Xᵀ + β·I)⁻¹  (7), con β el factor de regularización (se ajusta sin volver a ejecutar la red).
- **En línea:** mínimos cuadrados (LMS, O(N), inestable con gran dispersión de autovalores) y mínimos cuadrados recursivos (RLS, O(N²), convergencia de segundo orden). **Aprendizaje FORCE** (referencia 35): z(t) = wᵀ·r(t)  (8); error previo e⁻(t) = wᵀ(t − Δt)·r(t) − f(t)  (9); w(t) = w(t − Δt) − e⁻(t)·P(t)·r(t)  (10); P(t) = P(t − Δt) − P(t − Δt)·r(t)·rᵀ(t)·P(t − Δt)/(1 + rᵀ(t)·P(t − Δt)·r(t))  (11); P(0) = I/α  (12); error posterior e⁺(t) = e⁻(t)(1 − rᵀ(t)·P(t)·r(t))  (13); termina cuando e⁺/e⁻ ≈ 1  (14). FORCE funciona mejor con reservorios caóticos antes del entrenamiento y mantiene el error pequeño siempre; variantes: FORCE extendido, full-FORCE (menos neuronas, mejor con ruido y aplicable a SNN), Two-Step FORCE, Transfer-FORCE y R-FORCE (multidimensional); paquete `tension` (TensorFlow/Keras).
- **Gradiente en línea:** versión estable de Jaeger y colaboradores que optimiza escala de entrada, radio espectral, tasa de fuga y regularización; BPDC; BPTT; ACTRNN.
- **Evolutivo:** algoritmos genéticos, optimización por enjambre de partículas (PSO), optimizador de enjambre competitivo (CSO), colonia de abejas y **Evolino** (inspirado en LSTM).
- **Biológicamente plausible:** Hebb y anti-Hebb (no redujeron la dispersión de autovalores; el reservorio con Hebb "prefiere entradas fáciles de predecir"), **STDP** (mejora la separación en voz real; versiones con menos memoria para hardware) y **plasticidad intrínseca (IP)** (ajusta la excitabilidad de las neuronas; preentrenamiento y optimización global; esquema local en 2019).

## A5. Tendencias recientes (sección 4; p. 11 a 20)

- **Pruebas de referencia:** reconocimiento de dígitos hablados, formas de onda, dígitos escritos, **series NARMA**, ecualización de canal, XOR temporal y capacidad de memoria.
- **ESN profunda (DeepESN, 2016):** capas apiladas: x̃⁽ⁱ⁾(n) = tanh( W_fwd⁽ⁱ⁾·x⁽ⁱ⁻¹⁾(n) + W_rec⁽ⁱ⁾·x⁽ⁱ⁾(n − 1) )  (15); x⁽ⁱ⁾(n) = (1 − α⁽ⁱ⁾)·x⁽ⁱ⁾(n − 1) + α⁽ⁱ⁾·x̃⁽ⁱ⁾(n)  (16), con x⁽⁰⁾ = u; estado total ⟨x⁽¹⁾, …, x⁽ᴺ⁾⟩  (17). Resultados: escalas de tiempo ordenadas por la jerarquía; las capas altas representan frecuencias más bajas y las perturbaciones duran más (la diferencia se atenúa si la entrada llega a todas las capas); ESN profundas con remuestreo de secuencia (2022) y filtro de Hodrick–Prescott (2023).
- **ESN difusa profunda, autocodificador de ESN multicapa** (PSO en dos niveles: arquitectura y pesos), **CSO** para diagnóstico de fallas de impresoras 3D (26 patrones).
- **ESN no lineal:** x_NESN = a₀ + a₁x + a₂x² + … + aₙxⁿ  (18) (menos estados y más complejidad); **topología de mundo pequeño** (p ≈ 0,1; SW-ESN con entrada y salida separadas, mayor rango de ESP).
- **LSM:** STDP en línea (NEST), optimización de conectividad y número de neuronas (algoritmos evolutivos, estrategia de adaptación de covarianza para conectividad, distribución de pesos y constante de tiempo de la membrana) y búsqueda de arquitectura (MNIST, MNIST con ruido y FSDD).
- **Sistemas dinámicos:** reservorio de nodo único con retardo (ecuación diferencial con retardo dx/dt = F(t, x(t), x(t − τ))  (19); nodos virtuales θ = τ/N), **autómatas celulares**, **osciladores acoplados**  dx_i/dt = F(x_i) + G(x_1, …, x_N)  (20) (mecánicos, de ADN, redes de reacciones químicas, fase, relajación con VO₂, nano-osciladores de espín).
- **Reservorio físico (Tabla 2):** electrónico (circuitos analógicos, FPGA, memristores), fotónico (nodos ópticos, bucle de retardo, cavidad pasiva coherente), espintrónico (osciladores de par de espín, ondas de espín, skyrmiones, nanoimanes dipolares), mecánico (masa-resorte-amortiguador, brazo de pulpo, robots de tensegridad y generadores de patrón central) y **cuántico** (dinámica analógica bajo Hamiltoniano dependiente del tiempo, resonancia magnética nuclear, circuitos con compuertas; cualquier sistema caótico cuántico sirve).
- **RC de nueva generación (NG-RC):** con activación lineal y lectura no lineal, el RC es matemáticamente una **autorregresión vectorial no lineal (NVAR)**; el modelo NG-RC (referencia 208) prescinde de matrices aleatorias y de casi todos los metaparámetros, con menos datos y menos cómputo en Lorenz y otras pruebas.

## A6. Aplicaciones (sección 5; Tabla 3, p. 20 a 28)

Electrocardiograma (ESN adaptable por paciente con MIT-BIH; ESN para actividad anómala en dispositivos médicos; transistores orgánicos electroquímicos), electromiografía (LSM en hardware neuromórfico; plasticidad CRITICAL), magnetocardiografía (RC espintrónico físico), biomédicas diversas, **robótica** (masa-resorte, pulpo, brazo neumático, gateo de origami, aprendizaje de forrajeo con FORCE sobre un cultivo neuronal vivo), **drones** (ESN para distribuciones de peticiones de usuarios; ESN profunda con aprendizaje por refuerzo para trayectorias; control de alas batientes con RC físico), sensores inalámbricos (reconocimiento de actividad en vida asistida), **diagnóstico de fallas** (impresoras 3D; pilas de combustible PEMFC: predicción de vida útil restante con ESN y variantes), reconocimiento de imágenes (Tabla 4: competitivo en MNIST pero rendimiento mucho menor en CIFAR-10), agrupamiento de series (primer algoritmo dinámico con ESN; agrupamiento con reservorio profundo en 2020), segmentación de secuencias (dos reservorios que se supervisan mutuamente), aprendizaje de similitud (mejor que redes siamesas con pocos datos), detección de ataques en redes eléctricas (99 % de detección con reservorio de nodo único más MLP), identificación de emisores, comunicaciones ópticas (ecualización), tráfico de red, detección de símbolos MIMO-OFDM, quimiosensores (concentración de gases), pronóstico de **viento** (velocidad, dirección y potencia probabilística con ESN invariante a deformación temporal), procesamiento de **audio y habla** (LSM con dígitos aislados, regla hebbiana en línea con modelo de oído de Lyon, ESN con máquinas de kernel para árabe, nano-osciladores con TI-46) y **finanzas** (p. 27):
  - **Predicción bursátil:** un ensayo temprano de predicción de precio a corto plazo con ESN que usa el **exponente de Hurst** para elegir la subserie persistente más predecible de entrenamiento (Lin y otros, 2009; referencia 281 de la revisión); y un estudio de tres estructuras de RC (incluida la de mundo pequeño; referencia 250).
  - **Modelado de sistemas financieros** con ESN (referencia 251). **No se reportan cifras y no se menciona Bitcoin.**

## A7. Conexión con el cerebro (sección 6; p. 28 a 32)

- **Modelo corticoestriatal de Dominey:** corteza prefrontal recurrente (reservorio) más aprendizaje por recompensa en las conexiones al caudado (lectura); **selectividad mixta** (referencia 24 de la revisión, 2013): neuronas con respuestas superposición no lineal de varios aspectos, que elevan la dimensionalidad (colapsa en los ensayos con error) y hacen separable la salida con lectura lineal; observada en la corteza prefrontal, el subículo y el tálamo de un pez eléctrico; en un reservorio entrenado en una tarea de explorar-explotar la distribución de neuronas es similar a la de neuronas del cíngulo anterior dorsal de primates (referencia 288, 2016).
- **Oscilaciones neuronales y sincronía** (circuitos de alimentación hacia adelante frente a ensambles neuronales; **problema de vinculación** de ensambles superpuestos; Gray y Singer: sincronía de precisión de milisegundos; propagación de la sincronía; bandas de 0,05 a 500 Hz).

## A8. Perspectivas y problemas abiertos (sección 7; p. 32 y p. 33)

El reservorio aleatorio probablemente no es óptimo y la lectura lineal limita; la corteza no es aleatoria (estructura por evolución y desarrollo); **sin guías de diseño** ("las ideas disponibles se extraen de estudios experimentales de perfiles de escala de tiempo y espectros de frecuencia", Jaeger): propuesta de **aprendizaje a aprender (L2L)** de los hiperparámetros del reservorio con BPTT (referencia 308); falta de herramientas unificadas (guía práctica de Lukoševičius, caja de herramientas Oger 2012, easyesn, simulador NEST, Nengo, EchoTorch 2018, DeepESN en Matlab 2019, capa ESN en TensorFlow Addons 2020, `tension` 2022, ReservoirComputing.jl); reservorios físicos difíciles de diseñar y ajustar; direcciones: teoría, aplicaciones industriales (control predictivo no lineal, gemelos digitales) e integración con redes convolucionales y de grafos, y nuevas arquitecturas físicas (FPGA de bajo consumo, redes de Schrödinger, autómatas celulares con regla CA90).

## A9. Lectura crítica para la tesis

1. **Para el marco teórico de E20:** ecuaciones (1) a (3), el algoritmo 1, la regresión de cresta (7) y la discusión de que el **radio espectral < 1 no es necesario ni suficiente** (importante si E20 fija el radio) y de que el rendimiento **se satura con el tamaño del reservorio** (refuerza la prueba de 1 000 neuronas); la **DeepESN** y la heterogeneidad de escalas de tiempo respaldan el brazo SNN_ALPHA_MULTI (varias constantes de tiempo); la equivalencia **RC lineal + lectura no lineal = NVAR** y NG-RC dan un **referente sin parte aleatoria** que debería incluirse en la comparación (regresión con retardos).
2. **No hay evidencia financiera cuantitativa** ni sobre Bitcoin; la parte de finanzas son tres referencias sin resultados.
3. Al ser una revisión narrativa, no declara criterios de inclusión ni evalúa sesgo de publicación; las comparaciones entre reservorios físicos son de tareas de laboratorio (NARMA, XOR, dígitos).

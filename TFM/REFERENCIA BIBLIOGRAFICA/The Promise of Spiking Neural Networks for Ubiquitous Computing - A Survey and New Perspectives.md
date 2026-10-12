# The Promise of Spiking Neural Networks for Ubiquitous Computing: A Survey and New Perspectives

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 2, 7 a 13, 16 a 17, 19 a 22, 34, 37 y 38 de 50; la parte de reconocimiento de actividad, corazón, audio y emociones se leyó solo en resumen)

| Campo | Valor |
|---|---|
| Título exacto | The Promise of Spiking Neural Networks for Ubiquitous Computing: A Survey and New Perspectives |
| Autores | Hemanth Sabbella, Archit Mukherjee, Thivya Kandappu, Sounak Dey, Arpan Pal, Archan Misra y Dong Ma (Singapore Management University y TCS Research) |
| Tipo / Venue / Año | Artículo de revisión, arXiv:2506.01737v1 [cs.NE], 2 de junio de 2025 (formato ACM, 50 páginas) |
| Archivo local | `2506.01737v1.pdf` |
| URL / DOI | arXiv:2506.01737 (el DOI del PDF es un marcador de posición, no válido) |
| Métodos | Revisión sistemática de 76 estudios con redes neuronales espigantes (SNN) sobre series temporales de sensores, agrupados en seis dominios; además repaso de modelos de neurona, codificaciones, entrenamiento, bibliotecas de software y hardware neuromórfico |

## Aporte clave

Introduce de forma ordenada los componentes de una SNN (modelos de neurona, codificación de señales en espigas y métodos de entrenamiento) y revisa 76 trabajos con series temporales. Los dominios son actividad humana, latidos cardíacos, audio, emociones, gestos y tacto (p. 1 y p. 17). **No hay un dominio financiero**: lo único financiero es una referencia en la bibliografía (Mateńczuk y otros, 2021, "Financial time series forecasting: Comparison of traditional and spiking neural networks", p. 46). Es una buena fuente de **marco teórico de SNN**, no de evidencia financiera.

## Conocimiento extraído (HECHO, con página)

**Modelos de neurona (p. 7 a 9)**
- Las neuronas espigantes se comunican con espigas discretas y tienen una variable de estado (potencial de membrana) que evoluciona en el tiempo; eso les da memoria, a diferencia de las neuronas artificiales sin estado.
- **Integración y disparo con fuga (LIF):** integra la entrada, el potencial decae hacia el reposo con constante de tiempo τ_m, y dispara y se reinicia al superar el umbral (ecuación 1, p. 7). Es el modelo más usado.
- Variantes: integración y disparo sin fuga (IF), LIF recurrente (rLIF, con realimentación de las espigas, ecuación 3) y modelo de respuesta de espigas (SRM). Se mencionan Hodgkin-Huxley, Izhikevich, LIF adaptativo, exponencial y de resonancia (p. 8 y p. 9).
- La revisión **no describe neuronas de dos compartimentos (dendrita y soma) como TS-LIF**.

**Codificación de la señal en espigas (p. 9 a 12)**
- Por tasa (la intensidad define la probabilidad o frecuencia de espigas); temporal (incluida la gaussiana con campos receptivos); delta (espiga cuando el cambio supera un umbral; útil con movimientos y cambios bruscos); cruce de niveles; y codificación directa con una primera capa de neuronas LIF. La directa es la más usada por conservar la dinámica temporal y ser compatible con hardware neuromórfico (p. 11 y p. 12).
- Algunos trabajos citados encuentran mejor rendimiento con la codificación temporal gaussiana que con la de tasa (p. 10).

**Entrenamiento (p. 12 y p. 13)**
- **Problema de la neurona muerta:** la función de espiga no es diferenciable (la derivada es cero salvo en el umbral), así que puede no haber gradiente. Se usa un **gradiente sustituto** suave en el paso hacia atrás (ecuaciones 5 y 6, p. 12).
- **STDP** (plasticidad dependiente del tiempo de las espigas): fortalece la sinapsis si la presináptica dispara antes que la postsináptica y la debilita si ocurre al revés; se citan variantes (anti-Hebbiana, probabilística, modulada por recompensa) (ecuación 7, p. 13).
- Otras vías mencionadas: retropropagación en el tiempo, conversión de una red artificial a espigante y aprendizaje no supervisado.

**Reservorios espigantes (p. 20 a 22)**
- Los reservorios espigantes (rSNN) aparecen en detección de anomalías cardíacas con 91,3 % y 92 % de acierto en dos conjuntos distintos (p. 20), y en reconocimiento de voz con 83,2 % en el conjunto Spiking Speech Commands y 50,9 % en Spiking Heidelberg Digits (Cramer y otros) (p. 22).
- **Heterogeneidad de constantes de tiempo de la membrana:** Perez-Nieves y otros (2021) la introducen y alcanzan 81,7 % y 56,1 % en esos mismos conjuntos (p. 22). Es un antecedente directo de dar a cada neurona un ritmo de memoria distinto.

**Bibliotecas de software (p. 34)**
- snnTorch, SpikingJelly (compatible con modelos grandes como Spiking ResNet), Nengo (reglas de aprendizaje PES, RLS y BCM), **Norse** (extiende PyTorch con LIF, Izhikevich, STDP y SuperSpike), y Lava para el chip Loihi (p. 34).

**Hardware neuromórfico (p. 37)**
- DYNAP-SE2 (4 096 neuronas), Xylo (1 000 neuronas LIF y 278 000 sinapsis), Innatera T1 (500 neuronas) y Loihi 2 para investigación general (p. 37).

**Eficiencia**
- Ejemplo experimental de los autores: la detección de caídas con SNN en chip neuromórfico consume **71 veces** menos energía que una red artificial en un microcontrolador (p. 2).

**Direcciones futuras (p. 38)**
- Procesamiento en flujo continuo, sin ventanas deslizantes, para aprovechar la memoria de la membrana; hay dos retos: etiquetar puntos individuales y ajustar el tamaño de la memoria a cada tarea (p. 38).

## Limitaciones y críticas

- **[OPINIÓN]** Todos los trabajos revisados son clasificaciones de sensores (actividad, ECG, voz). No cubre regresión, pronóstico financiero ni series no estacionarias.
- **[OPINIÓN]** Es una revisión: no contrasta estadísticamente los resultados citados y mezcla conjuntos de datos distintos, por lo que los porcentajes no son comparables entre estudios (el propio texto lo reconoce al hablar de resultados "dependientes de la arquitectura y no comparables", p. 20).
- **[OPINIÓN]** El énfasis en eficiencia energética no es relevante para mi tesis, donde lo que importa es la precisión predictiva.

## Conexión con mi tesis (red E20)

- **Marco teórico de la red:** da la definición de LIF, de la codificación, del problema de la neurona muerta y del STDP que E20 usa. Sirve para el capítulo de marco teórico, junto con el artículo original TS-LIF.
- **Heterogeneidad de constantes de tiempo:** respalda E21 (constantes de tiempo log-uniformes entre 1 y 60 días) como idea con antecedentes publicados (Perez-Nieves y otros, 2021). Mis resultados con BTC real muestran que mejora a E20 en +0,01 de AUC pero no supera a la media móvil.
- **Codificación de la entrada:** E20 usa una entrada con signo y un canal de volatilidad con tanh; la revisión muestra el abanico de alternativas (tasa, delta, cruce de niveles) y que la elección no es neutra.
- **Frameworks:** el proyecto sigue el patrón de diseño de Norse; la revisión confirma que es un marco reconocido para SNN en Python.
- **Límite para citarlo:** no hay evidencia financiera.

## Referencias que cita y conviene localizar

Eshraghian y colaboradores (2023), "Training spiking neural networks using lessons from deep learning" (Proceedings of the IEEE); Perez-Nieves, Leung, Dragotti y Goodman (2021), "Neural heterogeneity promotes robust learning" (Nature Communications); Cramer y colaboradores (2020), conjuntos Spiking Heidelberg Digits y Spiking Speech Commands; Mateńczuk y colaboradores (2021), "Financial time series forecasting: Comparison of traditional and spiking neural networks" (Procedia Computer Science, 192); Ma y colaboradores (2025), "Spiking Neural Networks for Temporal Processing: Status Quo and Future Prospects" (arXiv:2502.09449); Dey y colaboradores (2022), clasificación de series temporales con reservorio espigante; Pehle y Pedersen (2021), Norse. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (modelos, ecuaciones, tablas de estudios y herramientas)

Contenido íntegro de las secciones 1 a 7 (páginas 1 a 39 del PDF; las páginas 40 a 50 son referencias), incluida la parte de dominios de aplicación que la ficha anterior solo había leído en resumen. Páginas = páginas del PDF. **Ninguno de los 76 estudios es financiero**; se documenta por completitud y como marco teórico de redes con picos.

## A1. Metodología de la revisión (p. 4 y p. 5)

- Búsqueda en Google Scholar de consultas con tres componentes (nombre de la aplicación, "Spiking Neural Networks" y modalidad de sensor); editoriales: IEEE (80 trabajos), Elsevier (19), Springer (16), Frontiers (8), MDPI (5), ACM (5), IOP (4) y otras (29): **166 artículos**.
- Filtro en dos pasos: relevancia (implementaciones de bajo consumo y tiempo real, revistas de alto impacto o muy citadas) y encadenamiento hacia atrás con el "principio de cuatro ojos" (al menos dos revisores por artículo): **76 estudios** = 9 de actividad humana, 13 de actividad cardíaca, **22 de audio**, 7 de emociones, 12 de gestos y 13 de tacto.
- Comparación con otras revisiones de SNN (Tabla 1): casi todas se centran en imágenes (Pfeiffer 2018, Bouvier 2019, Tavanaei 2019, Nunes 2022, Eshraghian 2023, etc.); esta es la primera con énfasis en series temporales de sensores.

## A2. Fundamentos: neuronas, codificación y entrenamiento (p. 6 a 15)

**Neuronas (ecuaciones 1 a 4):**
- **LIF:** τ_m·dV(t)/dt = −V(t) + R·I(t)  (1); integra la entrada, decae hacia el reposo con constante τ_m, dispara si V > V_th y se reinicia a V_reset; V en voltios, R resistencia de membrana, I corriente de entrada.
- **IF (sin fuga):** dV/dt = I(t)  (2).
- **LIF recurrente (rLIF):** τ_m·dV_i/dt = −V_i + Σ_{j} w_ij·Σ_{t_j^f} κ(t − t_j^f) + I_i(t)  (3), con κ el núcleo de respuesta sináptica; recurrencia uno a uno o de todos a todos; más coste y más tiempo de entrenamiento.
- **Modelo de respuesta de espigas (SRM):** V(t) = Σ_i Σ_{t_i^f} η(t − t_i^f) + Σ_j w_j Σ_{t_j^{in}} κ(t − t_j^{in})  (4), con η el núcleo refractario y κ el sináptico; generaliza al LIF y al IF, a costa de más cálculo.
- Otros: Hodgkin–Huxley, Izhikevich, LIF adaptativo (ALIF), exponencial, resonancia y disparo. **No se trata el modelo de dos compartimentos (dendrita y soma) de TS-LIF.**

**Codificación (p. 9 a 12):** (a) **por tasa** (probabilidad de pico proporcional al valor normalizado, distribuciones uniforme, normal, beta o Poisson; Banerjee y otros muestran que añadir ruido gaussiano aumenta la información del tren); (b) **temporal** (tiempo hasta el primer pico, inverso al valor; y gaussiana con campos receptivos, con mejor desempeño que la de tasa en varios trabajos); (c) **delta** (pico positivo o negativo si el cambio entre dos valores supera un umbral; multiumbral con n trenes, p. ej. 0,1, 0,2, 0,4 y 0,5); (d) **cruce de niveles** (niveles uniformes fijos, p. ej. 0,3, 0,6 y 0,9); (e) **directa** (la primera capa de neuronas LIF o IF convierte los valores analógicos en picos; la más usada).

**Entrenamiento (p. 12 a 15):**
- **Neurona muerta:** S = δ(V − V_th)  (5) y ∂S/∂V = ∞ si V = V_th y 0 en otro caso  (6); se usa un **gradiente sustituto** suave en el paso hacia atrás.
- **STDP:** Δw = A₋·e^{Δt/τ₋} si Δt < 0 y A₊·e^{−Δt/τ₊} si Δt > 0  (7), con Δt = t_pre − t_post (del orden de 10 ms; las constantes de la fórmula impresa difieren de la convención de otras fuentes); variantes: anti-Hebbiana, STDP en espejo, probabilística y modulada por recompensa (R-STDP).
- **SpikeProp** (Bohte y otros, 2002): sustituye ∂S/∂U por ∂t/∂U (tiempos de pico); limitado a un pico por neurona.
- **BPTT:** ∂L/∂W = Σ_t Σ_{s≤t} ∂L[t]/∂W[s]·∂W[s]/∂W  (8).
- **SLAYER** (Shrestha y otros): extiende BPTT con asignación de error en el tiempo; aprende retardos axonales y pesos a la vez.
- **STBP** (Wu y otros): ∂L/∂W[n] = Σ_t Σ_{s≤t} ∂L[t]/∂u[s,n]·∂u[s,n]/∂I[s,n]·∂I[s,n]/∂W[n]  (9).
- **STDP supervisado (SSTDP):** ∂L[n]/∂W[n] = ∂L[n]/∂t[n]·∂t[n]/∂W[n]  (10).
- **Conversión de red artificial a red con picos:** evita la neurona muerta pero es con pérdida de exactitud y sin dinámica temporal; se afina después.

## A3. Resultados por dominio (p. 16 a 33)

**Actividad humana (Tabla 2).** Dos trabajos sobre el conjunto RecGym (12 ejercicios, IMU más capacitancia corporal): Bian y otros, red de 256-64-12 neuronas con BPTT; codificación **delta multiumbral** la más robusta (87,5 %; en otro trabajo 91,7 % con tasa, 89,1 % temporal, 89,6 % binaria y 89,8 % delta multiumbral); en el chip Loihi con el menor producto energía-retardo. Actividades diarias: Li y otros (conversión): UCI-HAR 98,86 %, UniMiB SHAR 94,04 %, HHAR 97,52 % con **94 %** menos energía; Suriani y otros (tasa y STDP supervisado) WISDM 99,5 %; Fra y otros WISDM 94,51 % (93,47 % con CNN convertida); Wi-Fi 84,8 % frente a 88,57 % de una GRU con más de 70 % de ahorro de memoria; datos de profundidad MSR3D 75 % y 83,6 %; radar de micro-Doppler 85 %.

**Actividad cardíaca (Tabla 3).** Clasificación y detección de anomalías en el electrocardiograma: PhysioNet/CinC 2017 (84,4 % con conversión de CNN; 85,8 % con atención; 92 % con SNN de reservorio y STDP más regresión logística), MIT-BIH arritmia (93,8 %, 94,5 %, 91,3 % con SNN de reservorio sobre el chip DYNAP-SE y 722,1 µW; 95,34 % y 98,22 % con muestreo por cruce de niveles y STBP en ASIC con 0,75 µJ por inferencia; 98,29 % con 0,031 µJ; 97,9 % con STDP y R-STDP con 1,78 µJ por latido frente a 35 mJ de la mejor red artificial), fibrilación auricular MIT-BIH con 17 clases 95,6 % (delta y reservorio supervisado), 94,1 % con ConvLSTM 2D con picos (4,68 µJ frente a 450 µJ de la red artificial) y 79 % de detección de anomalías con 64 mW (0,7 % de la potencia de una CNN equivalente). Conclusión: delta funciona mejor con reservorios y cruce de niveles con MLP; en conversión, IF supera a la tasa.

**Audio (Tabla 4; 22 estudios).** Detección de palabras clave: Aloha 93,8 % (Loihi, 110 veces menos energía que GPU: 0,27 mJ frente a 29,8 mJ), 95,31 % con 6,6 µJ por inferencia en Xylo, WaveSense 99,5 % (Aloha), 99,8 % (Hey Snips) y 87,6 % (Speech Commands); conjuntos espigantes **SHD y SSC** (Cramer y otros, 2020): reservorio con 83,2 % y 50,9 %; **Perez-Nieves y otros (2021), heterogeneidad de constantes de tiempo de la membrana: 81,7 % y 56,1 %**. Reconocimiento del habla: 89,9 % (cóclea más CNN en FPGA), 97,5 % en TIDIGITS y 93,8 % en TIMIT, 98,4 % en FSDD (búsqueda bayesiana de parámetros), 94 % y 99,6 % en RWCP con Tempotron, 97,6 % en TIDIGITS, error de fonemas 18,7 % en TIMIT y de palabras 36,9 % (FAME) y 9,4 % (Librispeech). Clasificación de ambientes: 98,0 % con 542 µW en Xylo; 93 % con 692 µW y 57,6 µJ en DCASE 2020; 6,8 nJ en un procesador Zynq. Detección de actividad de voz: tasa de error total media (HTER) 2,72 % a 8,2 %; 0,9 µW con HTER 5,8 %, 12,6 % y 22,3 % en ruido bajo, medio y alto.

**Emociones (Tabla 5; electroencefalograma).** NeuCube (reservorio 3D con STDP): 74–86 % en DEAP y 96,67 % en SEED (Luo y otros); 83,5 % binaria y 94,83 % en 4 clases en DREAMER; FractalSNN: 80,92 % (DREAMER), 73,20 % (DEAP), 68,33 % (SEED) y 42,23 % (MPED); conversión de CNN con 91,43 % en SEED y 13,8 % de la energía; EESCN con aceleraciones de 1,9–3,3 veces sobre la anterior y 6,4–7,9 veces sobre NeuCube. Problemas: generalización entre sujetos y pocos conjuntos de datos.

**Gestos (Tabla 6).** sEMG con Myo y NinaPro (DYNAP-SE y Loihi: 5,7 ms y 41 mW), SpGesture (atención de Jaccard con picos), ultrasonido (92 %, 4,4 veces menos cómputo), control robótico (latencia < 4 ms y < 6 mW), neuronas motoras (≈ 95 %), lenguaje de signos (96 % sCNN con SLAYER y 1,1 mJ; 89,4 % sMLP con 37 µJ), radar neuromórfico (94,58 %, error de localización 0,98 m, < 300 µW).

**Tacto (Tabla 7).** Texturas 94,6 % (Biotac) y 92,2 % (RoboSkin) con SLAYER; detección de contacto y deslizamiento F1 > 0,999 (Loihi 32,66 nJ por inferencia frente a 5,169 µJ en CPU); 88,3 % en 6 tipos de contacto con STDP supervisado frente a 71,4 % de PCA y k-NN; formas 100 % hasta 11 objetos; objetos y recipientes con redes de grafos con picos (89,44 % y 64,4 % en EvTouch; 93,75 % y 73,33 % tras optimizar; 96 %, 90 % y 100 % en el estado del arte), fusión visual-táctil (81 % y 100 %; 1 900 veces menos potencia que una GPU).

## A4. Herramientas (p. 33 a 37)

- **Software (Tabla 8):** BindsNET (2018; simulación sobre PyTorch; LIF, IF, Izhikevich; STDP y R-STDP), Brian2 (2013), GeNN (2014), NEST (2007; redes de millones de neuronas), **snnTorch** (2021; LIF y de segundo orden; `spikegen`), **SpikingJelly** (2019; conversión a Lava para Loihi 2), Nengo (2015; NengoLoihi y NengoSpiNNaker), **Norse** (2020; extiende PyTorch; LIF, Izhikevich, STDP y SuperSpike), Lava/Lava-DL (2021; Loihi 2), Sinabs (2019; chips Speck y DYNAP-CNN de SynSense) y Rockpool (2019; Xylo y DYNAP-SE2; solo LIF). Recomendaciones: simulación (BindsNET, snnTorch) para investigar; entorno propio de la plataforma para desplegar.
- **Hardware (Tabla 10):** Akida (BrainChip), **Loihi 2** (Intel; 1 millón de neuronas y 120 millones de sinapsis; solo investigación), DYNAP-CNN (1 millón de neuronas), Speck (328 mil neuronas, visión), **DYNAP-SE2** (4 096 neuronas y 65 mil sinapsis; recurrente), **Xylo** (1 000 neuronas LIF y 278 mil sinapsis; ≈ 550 µW en audio y < 300 µW en IMU) y T1 de Innatera (500 neuronas y 60 mil sinapsis; < 1 mW).

## A5. Direcciones futuras (p. 37 a 39)

Procesamiento en flujo continuo sin ventanas deslizantes (retos: etiquetar puntos individuales y ajustar el tamaño de la memoria); SNN multimodales; **capacidad de respuesta** en los primeros pasos (ALIF y funciones de pérdida ponderadas en el tiempo); codificaciones híbridas (delta más tasa) y por entropía con front-ends analógicos; adaptación de modelos en el despliegue (dominio, prueba y aprendizaje continuo; la memoria de la membrana dificulta modelar el desplazamiento de distribución); compresión de SNN para dispositivos; falta de un estándar de conversión analógico-picos.

## A6. Lectura crítica para la tesis

1. **No hay evidencia financiera:** todos los resultados son de clasificación de sensores con conjuntos de laboratorio; los porcentajes no son comparables entre tareas ni demuestran capacidad de pronóstico.
2. **Eficiencia energética no es el objetivo de E20.** Lo útil para el marco teórico: ecuaciones del LIF, codificaciones (la **delta** y la **directa** se parecen a la entrada con signo y la lectura del proyecto), el problema de la neurona muerta y el gradiente sustituto (E20 usa lectura lineal sobre el reservorio, sin gradiente a través de picos), la STDP, la **heterogeneidad de constantes de tiempo** (Perez-Nieves y otros: base para el brazo SNN_ALPHA_MULTI) y el consejo de procesar sin ventanas (contrastar con la forma en que E20 propaga el estado de la membrana entre días; a verificar en el código).
3. La fórmula de STDP impresa tiene convención de signos distinta de la de otras fuentes (artículo de Ezinwoke y Rhodes); verificar antes de citarla.

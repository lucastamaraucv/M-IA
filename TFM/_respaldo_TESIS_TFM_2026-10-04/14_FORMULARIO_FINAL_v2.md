# Formulario TFM (5–8 octubre 2026): versión v2 lista para copiar

**Estudiante:** Lucas Ivan Tamara Trejo · **Profesora:** Maruja Ortega F. (09MIAR) · **Modalidad elegida en este borrador:** propuesta propia, individual.
**Reglas de la profesora (ya cubiertas abajo):** un solo formulario; campos: título, contexto y motivación (breve), objetivos (breve), metodologías de IA (breve), dataset; tutor (si ya contactaste); integrantes o justificación si es individual. Plazo: 5/10/2026 14:00 a 8/10/2026 23:59 (España); en Perú, 07:00 del 5/10 a 16:59 del 8/10.
**Cambios frente al borrador 12:** título más preciso, textos recortados al formato "breve", antecedentes añadidos (15 artículos de `REFERENCIA BIBLIOGRAFICA`), justificación individual redactada y lista de verificación.

---

## 1. Título del proyecto propuesto

Patrón de los títulos asignados por la VIU (`Asignaciones_11_10_23.pdf`, ~40 títulos): frases nominales cortas de 6 a 16 palabras, sin dos puntos ni detalles de validación: *[Acción] de [objeto] mediante / utilizando [técnica] en / para [dominio]*. Ejemplos financieros: «Predicción de Rendimiento de Cartera Utilizando Deep Learning en Mercados Financieros»; «Detección de Fraude en Transacciones Financieras utilizando Técnicas de Inteligencia Artificial»; «Análisis de Sentimiento en Redes Sociales y su Impacto en los Mercados Financieros». Los detalles (cronológica, referentes, TS-LIF exacto) van en objetivos y metodología, no en el título.

**Principal (copiar este):**
> Predicción de la Dirección de Bitcoin utilizando una Red Neuronal Espigante de Segmentos Temporales y Aprendizaje Automático

**Alternativas:**
> Red Neuronal Espigante de Segmentos Temporales para la Predicción de Series Temporales de Bitcoin

> Predicción de la Dirección de Bitcoin utilizando una Red Neuronal Espigante de Segmentos Temporales y Aprendizaje Automático

> Comparación de Redes Neuronales Espigantes y Aprendizaje Automático para la Predicción de Bitcoin en Mercados de Criptomonedas

Nota: las dos primeras adaptan el título del artículo original de la neurona (*TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting*) al estilo de la VIU. Sirve porque E20 usa esa neurona, pero tu red es un reservorio y el trabajo es una comparación, así que la primera promete algo más cercano a «proponer una red» que a «evaluarla».

## 2. Contexto y motivación (texto breve)

Los modelos de aprendizaje automático para predecir Bitcoin suelen reportar aciertos altos que desaparecen al compararlos con el precio de ayer, al evitar fugas de información temporal o al usar un bloque de prueba cronológico (Baquero, 2026; Sánchez Zurdo, 2022; Berger y Koubová, 2024). Las redes de reservorio y las redes con pulsos son alternativas ligeras y bioinspiradas, pero su uso en criptomonedas es escaso y rara vez cumple esos estándares (Sharma et al., 2025; Ezinwoke y Rhodes, 2025; Zhang y Vargas, 2023). Este trabajo parte de E20, un reservorio propio de 1 000 neuronas espigantes de dos compartimentos (TS-LIF) ya desarrollado y auditado, y mide con un protocolo preregistrado si aporta información adicional sobre BTC real.

## 3. Objetivos (texto breve)

**General.** Determinar, con un protocolo preregistrado y reproducible, si un reservorio espigante TS-LIF aporta información predictiva sobre el movimiento y la dirección de Bitcoin más allá de referentes simples y de modelos de aprendizaje automático con la misma información.

**Específicos.**
1. Evaluar E20 con datos reales de BTC (diario y de 1 h a 2 h) frente a persistencia, media móvil exponencial de |r| y HAR, con un bloque final intocable.
2. Compararlo con regresión logística, bosques aleatorios, gradient boosting, perceptrón multicapa, TCN y LSTM, con la misma validación cronológica, métricas oficiales (AUC, acierto, Brier, calibración), intervalos por bloques, prueba de Diebold–Mariano y número de configuraciones declarado.
3. Validar el protocolo con series sintéticas tipo BTC de señal conocida (0 a 100 %): el 0 % no debe dar señal y los niveles altos deben detectarse.
4. Identificar qué componente de E20 aporta o no (recurrencia, memoria multiescala, lectura) mediante ablaciones y un reservorio no espigante de control.

## 4. Posibles metodologías de IA (texto breve)

Modelo principal: reservorio espigante TS-LIF con lectura logística o ridge. Controles: red de estado de eco no espigante y modelo lineal con retardos (equivalente a un reservorio de nueva generación). Referentes de ML: regresión logística, Random Forest, gradient boosting, MLP, TCN y LSTM. Evaluación: validación con ventana móvil y bloque final intocable; AUC, acierto, Brier y calibración; contrastes pareados con bootstrap por bloques, corrección de Holm y tamaño de efecto preregistrado; se declara la potencia estadística. Trazabilidad: código versionado, semillas y declaración de uso de IA según la guía de la VIU.

## 5. Descripción del dataset

Datos reales (principales): serie diaria BTC/USD 2016-04-24 a 2026-04-25 (archivo fijo y versionado); velas de Binance de 1 minuto a 1 día (API pública, almacenadas en PostgreSQL); índice de volatilidad implícita DVOL de Deribit y variables de calendario; toda variable se construye solo con información anterior al instante de predicción. Datos sintéticos (control): series tipo BTC con caos determinista, momentum, cambios de régimen y GARCH, con señal conocida; se publican generador y semillas. Licencias: se citará la fuente y solo se publicará código y datos derivados permitidos.

## 6. Tutor y modalidad

**Tutor (campo del formulario):** si no has contactado a nadie, escribe: *"No he contactado tutor. Agradecería asignación afín a series temporales con aprendizaje automático o redes neuronales."* Las líneas del listado más afines: #49 (W. J. Rodríguez Graterol), #135 (F. G. Vera Briones) y #55 (J. Cigales Canga). Si contactas a uno antes del 8/10, escribe su nombre.

**Integrantes:** Lucas Ivan Tamara Trejo (individual).

**Justificación de TFM individual (la del estudiante; copiar este):**
> Prefiero realizar el Trabajo de Fin de Máster de forma individual debido a la alta limitación de tiempo derivada de la combinación de mis responsabilidades laborales y el ritmo de estudio del máster. Desarrollarlo de manera individual me otorga la autonomía y flexibilidad necesarias para organizar mis horarios de investigación y desarrollo de código de forma independiente, adaptándome con mayor eficiencia a mi disponibilidad actual sin depender de la coordinación de tiempos con otros compañeros.

## 7. Antecedentes que sustentan la propuesta (para memoria y para responder a la profesora)

Agrupados por papel; todos están fichados en `REFERENCIA BIBLIOGRAFICA` con su anexo técnico. Comprobar autores, año y DOI en cada ficha antes de citar.

| Grupo | Artículos | Qué aportan |
|---|---|---|
| Reservorio o pulsos en finanzas y BTC | Sharma et al. (2025), *Echo State Networks for Bitcoin Time Series Prediction*; *Reservoir Computing in Alpha Forecasting of Foreign Exchange Market*; *Quantum Reservoir Computing for Realized Volatility Forecasting*; Ezinwoke y Rhodes (2025), *Predicting Price Movements in High-Frequency Financial Data with SNN*; Walugembe et al. (2026), *Bio-Inspired Spiking Recurrent Networks…*; Kenny (2020), TU Dublin | Hay precedentes, pero evalúan nivel de precio, una sola partición o seleccionan el mejor modelo sobre la prueba: el hueco que cubre este trabajo |
| Evaluación y referentes | Baquero (2026), *Bitcoin Price Prediction: Peer-Reviewed Evidence…*; *HARd to Beat*; Berger y Koubová (2024); Sánchez Zurdo (2022); Akyildirim et al. (2021); *The Efficient Market Hypothesis for Bitcoin in the Context of Neural Networks* | Estándares: referente ingenuo, ventana móvil, Diebold–Mariano, varios regímenes, incluir el cero; resultados negativos y predictibilidad solo a corto plazo |
| Marco teórico | Zhang y Vargas (2023), revisión de reservorios; Domingo Colomer (2023), tesis UPM; Sabbella et al. (2025), revisión de redes con pulsos | Ecuaciones de ESN y LIF, métrica de dirección (MDA), ensamble, radio espectral, heterogeneidad de constantes de tiempo |
| Contraste (cómo no evaluar) | Estudios de nivel de precio sin referente ingenuo (Recta 2023; EAFIT 2023; gestión de capital) | Justifican el protocolo estricto |

Resultados previos propios (de `PLAN_E20_MEJORA_IMPORTANTE_v1.md`): con la misma información E20 empata con el mejor ML a 1 h; la dirección de BTC solo es predecible entre 1 min y 2 h (AUC .54–.55); con lectura fija C=3e-5 E20 iguala a una media móvil de |r|. El trabajo no promete que E20 gane: un "empata, y esto aprendemos de cada componente" es un resultado válido.

## 8. Lista de verificación antes de enviar (tú envías; yo no)

- [ ] Elegir A (propuesta propia, este documento) o B (5 opciones del listado, ver `12`): **solo un formulario**.
- [ ] Confirmar individual y la justificación (debe ser cierta).
- [ ] Tutor: nombre, o la frase de "no he contactado tutor"; si es externo, CV breve en Comentarios.
- [ ] Revisar que cada campo respete el límite de caracteres del formulario (la versión corta del título está para eso).
- [ ] Declaración de uso de IA según la guía VIU: este texto fue redactado con asistencia de IA; verifícalo y declara su uso.
- [ ] Enviar entre el 5/10 14:00 (España) y el 8/10 23:59.

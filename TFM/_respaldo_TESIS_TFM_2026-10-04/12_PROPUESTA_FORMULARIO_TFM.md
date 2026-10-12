# Formulario de TFM (5–8 octubre 2026): borrador para proponer un proyecto propio con la red E20

**Fuente institucional:** `SESIONES/INDICACIONES 1.txt` (Maruja Ortega F., profesora 09MIAR). Etiqueta: `INSTITUCIONAL`.
**Estado:** borrador. `PENDIENTE_DE_CONFIRMAR`: tutor, modalidad (individual o grupo), permisos de datos y que la universidad acepte un proyecto propio basado en investigación previa.

## 1. Lo que exige el texto de la profesora (resumen verificable)

| Dato | Contenido del .txt |
|---|---|
| Apertura de formularios | **5/10/2026 a las 14:00** (hora de España peninsular), en «Documentación para el Trabajo de Fin de Título / Recursos y Materiales». En Lima: **07:00 del 5/10** (España CEST = UTC+2, Lima = UTC−5; diferencia de 7 h). |
| Plazo de envío | del 5 al **8 de octubre de 2026 hasta las 23:59 (España)**. En Lima: **16:59 del 8/10**. |
| Cuántos formularios | **UNO solo**: o selección del listado, o propuesta propia. No se aceptan dos. |
| Si seleccionas del listado | 5 opciones por orden de preferencia. |
| Si propones un proyecto propio | título; contexto y motivación (texto breve); objetivos (texto breve); posibles metodologías de IA (texto breve); descripción del dataset. |
| Tutor | indicar si ya contactaste uno (VIU o externo; si es externo, breve CV en Comentarios; puede proponerse un cotutor VIU). |
| Grupo | nombres de los integrantes (**recomendado 2, máximo 4**) o, si es **individual, completar la justificación**. |
| Asignación | se publica en la misma sección, según el calendario de la Guía Docente. |
| Contacto | mortega@professor.universidadviu.com |

Punto crítico: como solo cabe un formulario, hay que decidir **antes del 8/10** entre la opción A (propuesta propia con E20) y la opción B (selección del listado). Ver sección 5.

## 2. OPCIÓN A: textos listos para copiar al formulario (propuesta propia)

### Título del proyecto propuesto

**Reservorio espigante TS-LIF frente a modelos de aprendizaje automático en la predicción de Bitcoin con datos reales bajo validación cronológica, con series sintéticas de señal conocida como control**

*(alternativa más corta: «¿Aporta información un reservorio de neuronas espigantes en la predicción de Bitcoin? Comparación con modelos de ML con datos reales»)*

**Decisión del estudiante (2026-10-02): la tesis debe usar datos reales de BTC.** Por eso BTC real es el eje (O1–O2) y las series sintéticas solo sirven de control para validar el protocolo.

### Contexto y motivación (texto breve)

Los modelos de aprendizaje automático (ML) y profundo se usan con frecuencia para predecir mercados financieros, pero sus resultados suelen estar inflados por fugas de información temporal y por comparaciones desiguales. Las redes neuronales espigantes (SNN) son una familia bioinspirada con interés teórico y de bajo consumo, pero se evalúan poco en finanzas con protocolos rigurosos. Este trabajo parte de una red propia de 1 000 neuronas espigantes de dos compartimentos (TS-LIF), llamada E20, desarrollada y auditada durante 2026. Las pruebas preliminares indican que, en condiciones iguales de información, E20 **empata** con los mejores modelos de ML en lugar de superarlos; el trabajo busca medir con exactitud cuándo, cuánto y por qué.

### Objetivos (texto breve)

**Objetivo general:** determinar, con un protocolo preregistrado y reproducible, si un reservorio espigante TS-LIF aporta información predictiva adicional frente a modelos clásicos de ML y a referentes simples.

**Objetivos específicos:**
1. **O1.** Evaluar con **datos reales de Bitcoin** (diario y de 1 h a 2 h, donde el proyecto ya midió algo de señal) si E20 predice la dirección y el movimiento mejor que referentes simples (persistencia, medias móviles de |r|, HAR), con un bloque final intocable fijado de antemano.
2. **O2.** Comparar E20 con modelos de ML (regresión logística, bosques aleatorios, gradient boosting, perceptrón multicapa, TCN y LSTM) con la misma información y la misma validación cronológica sobre BTC real, con métricas oficiales (AUC, acierto, Brier y calibración) e intervalos de confianza por bloques.
3. **O3.** Validar el protocolo con un banco **sintético** de series tipo BTC y señal conocida (0, 10, 30, 40, 60, 80, 90 y 100 %): control positivo (debe detectarse la señal) y control negativo (0 % no debe producir señal).
4. **O4.** Identificar qué componente de E20 aporta o no (recurrencia, memoria multiescala, lectura) mediante ablaciones y un control no espigante, y documentar costes y límites.

### Posibles metodologías de IA (texto breve)

- **Modelo principal:** reservorio espigante TS-LIF (neuronas de dos compartimentos, memoria multiescala y plasticidad STDP/iSTDP) con lector logístico o ridge.
- **Controles:** red de estado de eco (ESN) no espigante con la misma entrada y lectura; modelos con retardos y volatilidad rodante.
- **Referentes de ML:** regresión logística, Random Forest, gradient boosting, MLP, TCN y LSTM, con selección de modelo solo por validación interna.
- **Evaluación:** validación cronológica con bloque final intocable; métricas AUC, acierto, Brier y curva de calibración; diferencias pareadas por realización con bootstrap por bloques y corrección de Holm; tamaño de efecto preregistrado. Se declara la potencia estadística disponible.
- **Trazabilidad:** código versionado, semillas, bitácora de cada ejecución y declaración de uso de IA conforme a la guía VIU.

### Descripción del dataset

1. **BTC real (datos principales):** (a) serie diaria BTC/USD 2016-04-24 a 2026-04-25 (archivo fijo y versionado en el proyecto); (b) velas de Binance de 1 minuto a 1 día obtenidas de la API pública y almacenadas en PostgreSQL; (c) índice de volatilidad implícita DVOL de Deribit a 1 h y variables de calendario. Todas las variables se construyen solo con información disponible antes del instante de predicción.
2. **Datos sintéticos (control, propios y reproducibles):** series tipo BTC generadas con caos determinista (mapa logístico), momentum, cambio de régimen y GARCH persistente, con nivel de señal controlado y verdad conocida (oráculo). Se publica el generador y las semillas.
3. **Estado de licencias y permisos:** `PENDIENTE_DE_CONFIRMAR` (condiciones de uso de cada fuente antes de redistribuir datos; se citará la fuente y se publicará solo código y datos derivados permitidos).

### Tutor, grupo y justificación

- **Tutor:** `PENDIENTE_DE_CONFIRMAR`. Si aún no has contactado a nadie, escribe «No he contactado tutor». Las líneas del listado más cercanas a este trabajo son #49 (W. J. Rodríguez Graterol, series temporales multivariadas con ML/DL), #135 (F. G. Vera Briones, redes neuronales para predicción de datos) y #55 (J. Cigales Canga, cambio de distribución).
- **Integrantes:** `PENDIENTE_DE_CONFIRMAR`. Recomendado 2, máximo 4.
- **Si es individual, borrador de justificación** (a confirmar por ti, porque debe ser cierto): «El trabajo continúa una línea de investigación individual de varios meses sobre una red espigante propia, con código, datos y protocolo ya desarrollados por el estudiante. Su ejecución y verificación dependen de ese material de partida, por lo que el estudiante solicita realizarlo de forma individual». Verificable con el historial de git del proyecto.

## 3. Resultados previos que respaldan la propuesta (todos de archivos del proyecto)

| Hecho | Evidencia | Estado |
|---|---|---|
| Con la misma información, E20 **empata** con el mejor ML a 1 h (.703 frente a .699, IC95 [−.001, +.012]). | `PLAN_E20_MEJORA_IMPORTANTE_v1.md`, auditoría 118 agentes (P5) | exploratorio, 1 bloque |
| La dirección de BTC es predecible solo en 1 min–2 h (AUC .54–.55); a 4 h o más no. | memoria del proyecto, 13 escalas con nulos barajado e IAAFT | verificado en el proyecto |
| Lectura fija C=3e-5: baja la varianza entre realizaciones ≈ 2 veces y el AUC de E20 sube de .5734 a .6066 (GARCH sintético, 10 realizaciones nuevas). | `logs_ind/e20_pd/mi_fase01_resultado.txt` (commit 68e8c63) | medido el 2026-10-02 |
| Con esa lectura, E20 iguala a una media móvil simple de \|r\| (.6066 frente a .6080). | misma fuente | medido el 2026-10-02 |
| La red no logra una mejora importante todavía; los estados de E20 no añaden información sobre los retardos. | `PLAN_E20_PUNTOS_DEBILES_v1.md` | exploratorio |

**Enfoque honesto para la memoria:** una conclusión de «E20 ≈ ML, y esto es lo que se aprende de cada componente» es un resultado científicamente válido. La propuesta **no promete** que E20 gane.

## 4. Literatura ya recopilada que sirve de base (en `TS-LIF 1000 NEURONAS/teorias_resumenes/`)

TS-LIF (ICLR 2025) y TS-SNN; DH-LIF; *Efficient and Effective Time-Series Forecasting with Spiking Neural Networks*; *Financial Time Series Prediction using Spiking Neural Networks*; *High-Frequency Trading and Financial Time-Series Prediction with SNNs* (Gao, Luk, Weston, 2021); e-prop (*A solution to the learning dilemma for recurrent networks of spiking neurons*); *Heterosynaptic Plasticity Prevents Runaway Synaptic Dynamics*; *Collective stability of networks of winner-take-all circuits*; *Closed-form Continuous-time Neural Networks*; *A Time Series is Worth 64 Words* (PatchTST); *Hawkes processes in finance* (Bacry y Muzy, 2015); *Chaos in Bitcoin Cryptocurrency Metrics*; *Are Bitcoin Bubbles Predictable? LPPLS* (Wheatley y Sornette, 2018); el índice `00_INDICE.md` ordena 69 resúmenes por problema. Las referencias deben comprobarse con DOI antes de citarlas en la memoria.

## 5. OPCIÓN B (alternativa): selección de 5 propuestas del listado

Si prefieres la vía segura de tutor asignado, el orden de la hoja `Selección BTC` del Excel (prioridad 1 a 5) es: **#49** (Rodríguez Graterol), **#55** (Cigales Canga), **#132** y **#135** (Vera Briones, grupo máx. 3) y **#31** (Barraza, stablecoins). Con esa opción **E20 no se aprobaría automáticamente**: habría que acordarlo con el tutor, y #49/#135 son los que mejor admiten una red propia como método principal.

| Criterio | A: propuesta propia | B: del listado |
|---|---|---|
| Uso de E20 como centro | Sí, es la propuesta | Solo si el tutor lo acepta |
| Tutor | Debes conseguirlo o la universidad lo asigna | Ya está definido |
| Riesgo | Rechazo o reasignación de tema | Tema distinto al que quieres |
| Recomendación | **Mi recomendación, por tu objetivo declarado**, siempre que contactes antes a un tutor afín (#49 o #135) | Respaldo |

Decisión pendiente del estudiante. Solo se puede enviar uno de los dos.

## 6. Pendientes antes de enviar

1. Decidir A o B (un solo formulario).
2. Individual o grupo (y nombres) y, si es individual, la justificación definitiva.
3. Tutor: contactarlo antes del 8/10 si es posible; si es externo, preparar un CV breve.
4. Confirmar con la profesora si un proyecto basado en investigación previa propia es aceptable y cómo declararlo.
5. Revisar licencias de datos (Binance, Deribit, CryptoCompare) y no redistribuir datos restringidos.
6. Preparar la declaración de uso de IA (modelo de la página 4 de `P11_G01 Guia uso IA`); este borrador fue redactado con asistencia de IA y tú debes verificarlo y firmarlo.
7. El formulario lo envías **tú** en el Campus Virtual; yo no lo envío.

## 7. Contrato de salida

- **Hecho:** lectura de `INDICACIONES 1.txt` y del contexto de la tesis; borrador de los campos del formulario; comparación A/B.
- **Evidencia:** este archivo; `SESIONES/INDICACIONES 1.txt`; `Seleccion_TFM_BTC_y_catalogo_tutores.xlsx`; commit 68e8c63 del proyecto E20.
- **Pendiente:** decisión A/B, tutor, grupo, licencias, confirmación con la profesora.
- **Siguiente acción:** el estudiante elige A o B y confirma tutor y modalidad; después se ajusta el texto y se registra la decisión en `11_ESTADO_Y_DECISIONES.md`.

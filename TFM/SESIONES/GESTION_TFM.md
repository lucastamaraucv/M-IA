# Gestión del TFM: formulario, requisitos VIU, estado, pendientes y defensa

**Estudiante:** Lucas Ivan Tamara Trejo · **Actualizado:** 2026-10-04 · La tesis está en `TFM/TESIS TFM/MEMORIA_TFM.md` (con sus figuras en `TESIS TFM/figuras/`). Este archivo reúne todo lo administrativo para que la carpeta de la tesis contenga solo la tesis. Copia de los 24 archivos de planificación anteriores: `TFM/_respaldo_TESIS_TFM_2026-10-04/`.

---

# PARTE I. Formulario de propuesta (5–8 de octubre de 2026)

**Lo envías tú** en el Campus Virtual; ninguna IA lo envía.

## 0. Reglas del formulario (fuente: `SESIONES/INDICACIONES 1.txt` y Guía didáctica 2026-27)

| Dato | Valor |
|---|---|
| Plazo | **5/10/2026 14:00 → 8/10/2026 23:59 (España)** = **07:00 del 5/10 → 16:59 del 8/10 (Lima)** |
| Dónde | Campus Virtual → «Documentación para el Trabajo de Fin de Título / Recursos y Materiales» |
| Cuántos | **Uno solo**: selección del listado (5 opciones por preferencia) **o** propuesta propia |
| Propuesta propia | título; contexto y motivación (breve); objetivos (breve); metodologías de IA (breve); descripción del dataset |
| Tutor | indicar si ya se contactó (VIU o externo; si es externo, CV breve en Comentarios) |
| Grupo | recomendado 2, máximo 4; **la guía 2026-27 dice que los TFM son grupales salvo casos especiales debidamente justificados** → la justificación individual es importante |
| Trabajo previo | la guía exige declarar en el resumen si el TFM **se basa en trabajos previos del alumno** (aquí: MDHS-SNN, E20 y TIA-LIF, desarrollados en 2026) |

## 1. Título del proyecto

**Principal (elegido por el estudiante):**
> Predicción de la Dirección de Bitcoin utilizando una Red Neuronal Espigante de Segmentos Temporales y Aprendizaje Automático

Alternativas si el formulario limita caracteres o se prefiere nombrar el reservorio:
> Predicción de la Dirección de Bitcoin mediante un Reservorio de Neuronas Espigantes y Modelos de Aprendizaje Automático

> Comparación de Redes Neuronales Espigantes y Aprendizaje Automático para la Predicción de Bitcoin en Mercados de Criptomonedas

Reglas observadas en los ~40 títulos asignados por la VIU (`SESIONES/Asignaciones_11_10_23(1).pdf`): frase nominal de 6 a 16 palabras; sin siglas, sin dos puntos, sin cifras; no promete que el modelo gane; los detalles (validación, referentes) van en objetivos. La guía exige que el título final **no difiera** del asignado.

## 2. Contexto y motivación (texto breve, copiar)

Muchos modelos de aprendizaje automático para predecir Bitcoin pierden su ventaja al compararlos con referentes simples o al usar validación cronológica estricta. Las redes neuronales espigantes son una alternativa bioinspirada y de bajo coste, pero casi no se han evaluado con ese rigor en criptomonedas. El trabajo parte de una línea de investigación propia desarrollada en 2026: un reservorio de 1 000 neuronas espigantes de dos compartimentos (neurona TS-LIF, ICLR 2025) llamado E20, cuya mejor versión (E20-ALB) lee sus estados con un bosque aleatorio. Se propone medir con un protocolo preregistrado si esta red aporta información sobre la dirección de Bitcoin que no capten los modelos convencionales con la misma información.

## 3. Objetivos (texto breve, copiar)

**General.** Determinar, con un protocolo preregistrado y reproducible, si una red de reservorio con neuronas TS-LIF aporta información predictiva sobre la dirección de Bitcoin más allá de referentes simples y de modelos de aprendizaje automático que reciben la misma información.

**Específicos.**
1. Validar el protocolo con series sintéticas de señal conocida (control positivo y negativo).
2. Identificar qué componentes de la red aportan valor mediante ablación (recurrencia, memoria multiescala, lectura).
3. Comparar la red con regresión logística, bosque aleatorio, gradient boosting, perceptrón multicapa, LSTM y una variante con atención, con validación cronológica, AUC e intervalos por bootstrap de bloques.
4. Determinar en qué escalas temporales la dirección de Bitcoin es predecible y si el resultado se replica en otros activos (Ether, oro tokenizado).
5. Confirmar el resultado una sola vez en activos nunca utilizados, con una prueba de equivalencia.

## 4. Posibles metodologías de IA (texto breve, copiar)

Red neuronal espigante de reservorio (neuronas TS-LIF de dos compartimentos) con lectura de bosque aleatorio o regresión logística; variante con atención entrenada por retropropagación como contraste. Referentes de aprendizaje automático con las mismas entradas: regresión logística, bosque aleatorio, gradient boosting, perceptrón multicapa y LSTM. Evaluación: partición cronológica con bloque final intocable, AUC de dirección, acierto selectivo, intervalos por bootstrap de bloques emparejado, placebos, análisis de potencia, prueba de equivalencia y preregistro de cada hipótesis. Código versionado, semillas fijas y declaración de uso de IA según la guía de la VIU.

## 5. Descripción del dataset (copiar)

Datos reales y públicos: velas de Binance de 1 minuto a 1 día para Bitcoin (2018–2026), Ether y oro tokenizado (PAXG), almacenadas en PostgreSQL con manifiestos sha256; serie diaria BTC/USD 2016–2026 en un archivo fijo versionado; series diarias de mercados tradicionales de FRED (NASDAQ, bono a 10 años, Brent, EURUSD, dólar). Variables: retornos, volatilidad, 62 indicadores técnicos causales y calendario, todas construidas solo con información anterior al instante de predicción. Datos sintéticos propios con señal de intensidad conocida (reglas de régimen, momentum, caos y cambio de volatilidad), con generador y semillas publicados. Para la prueba final se reservan Solana, BNB y XRP a 2 horas.

## 6. Tutor, integrantes y justificación

**Tutor:** *«No he contactado tutor. Agradecería una asignación afín a series temporales con aprendizaje automático o redes neuronales.»* Líneas del listado más afines: #49 (W. J. Rodríguez Graterol, series temporales multivariadas), #135 (F. G. Vera Briones, redes neuronales para predicción), #55 (J. Cigales Canga, cambio de distribución). Si contactas a uno antes del 8/10, escribe su nombre.

**Integrantes:** Lucas Ivan Tamara Trejo (individual).

**Justificación de TFM individual (la del estudiante; debe ser cierta):**
> Prefiero realizar el Trabajo de Fin de Máster de forma individual debido a la alta limitación de tiempo derivada de la combinación de mis responsabilidades laborales y el ritmo de estudio del máster. Desarrollarlo de manera individual me otorga la autonomía y flexibilidad necesarias para organizar mis horarios de investigación y desarrollo de código de forma independiente, adaptándome con mayor eficiencia a mi disponibilidad actual sin depender de la coordinación de tiempos con otros compañeros. Además, el trabajo continúa una línea de investigación propia sobre una red neuronal espigante, con código, datos y protocolo ya desarrollados por mí, cuyo historial está versionado.

*(La última frase es opcional: refuerza el «caso especial» que pide la guía 2026-27.)*

**Opción B (alternativa, solo si no se envía la propuesta propia):** 5 propuestas del listado por orden: #49, #55, #132, #135, #31. Con esa vía E20 no queda aprobada automáticamente; habría que acordarlo con el tutor.

## 7. Resultados previos que respaldan la propuesta (para el correo o el tutor)

| Hecho | Cifra |
|---|---|
| E20-ALB, mejor modelo del banco sintético | AUC medio 0,741 frente a RF 0,731; supera a RF con 10 entradas en 5 de 9 bancos |
| E20-ALB frente a TIA-LIF (atención) en sintéticos | mejor en 4 de 4 bancos (3 de 4 con 25 épocas) |
| BTC a 2 h (11 225 barras de prueba) | todos los modelos razonables AUC 0,53–0,54; E20-ALB 0,536 empata con GBM y logística; supera a RF +0,0065 [+0,0013; +0,0121] |
| Escala temporal | dirección de BTC predecible solo entre 1 min y 2 h |
| Fuga corregida | el 87–94 % histórico de TIA-LIF era fuga t+1; sin ella ≈ clase mayoritaria |

Detalle completo en `TESIS TFM/MEMORIA_TFM.md`. **No se promete que la red gane**: un empate bien medido es un resultado válido y así se presentará.

## 8. Antecedentes (fichados en `TFM/REFERENCIA BIBLIOGRAFICA`)

| Grupo | Trabajos | Qué aportan |
|---|---|---|
| Reservorio o redes espigantes en finanzas | Sharma et al. 2025 (ESN para BTC); He 2023 (reservorio en divisas); Li et al. 2025 (reservorio cuántico, volatilidad); Ezinwoke y Rhodes 2025; Walugembe et al. 2026; Kenny 2020 | Precedentes con nivel de precio o selección sobre el test: el hueco que cubre este TFM |
| Evaluación y referentes | Baquero 2026; Audrino y Chassot 2024 (HAR); Berger y Koubová 2024; Sánchez Zurdo 2022; Akyildirim et al. 2021; Kraehenbuehl y Osterrieder 2022 | Referente ingenuo, validación cronológica, resultados negativos honestos |
| Marco teórico | Feng et al. 2025 (TS-LIF); Zhang y Vargas 2023; Domingo Colomer 2023; Sabbella et al. 2025 | Ecuaciones de la neurona, reservorios, redes espigantes |
| Contraste (cómo no evaluar) | López-García 2023; Hernández y Forero 2023; Gabana Molina 2022 | Nivel de precio sin referente ingenuo |

## 9. Correo a la profesora (opcional; lo envías tú)

**Para:** mortega@professor.universidadviu.com
**Asunto:** TFM 09MIAR – propuesta de proyecto propio (individual) – Lucas Ivan Tamara Trejo

> Buenas tardes, profesora Ortega:
>
> Le envío mi propuesta de proyecto propio para el TFM, que enviaré también por el formulario dentro del plazo (5 al 8 de octubre).
>
> **Título:** Predicción de la Dirección de Bitcoin utilizando una Red Neuronal Espigante de Segmentos Temporales y Aprendizaje Automático.
>
> **Resumen:** el trabajo evalúa con un protocolo preregistrado si una red neuronal espigante de reservorio, basada en la neurona TS-LIF (ICLR 2025), aporta información sobre la dirección de Bitcoin más allá de modelos de aprendizaje automático con la misma información. Parte de una línea de investigación propia desarrollada en 2026, que declararé explícitamente en la memoria. Los resultados preliminares indican que la red empata con los mejores modelos en datos reales y los supera en datos sintéticos con estructura conocida; un empate bien medido también sería una conclusión válida.
>
> **Modalidad:** individual, por la limitación de tiempo que me imponen mis responsabilidades laborales y porque el trabajo continúa una línea propia ya versionada.
>
> **Tutor:** todavía no he contactado a ningún tutor; agradecería una asignación afín a series temporales con aprendizaje automático o redes neuronales.
>
> Le agradecería confirmar si es aceptable un proyecto propio basado en investigación previa del estudiante y cómo debo declararlo.
>
> Un saludo,
> Lucas Ivan Tamara Trejo

## 10. Lista de verificación antes de enviar

- [ ] Elegir propuesta propia (este documento) u opción B: **un solo formulario**.
- [ ] Confirmar modalidad individual y que la justificación es cierta.
- [ ] Tutor: nombre o la frase «no he contactado tutor».
- [ ] Revisar el límite de caracteres de cada campo.
- [ ] Declarar el uso de IA según la guía VIU (estos textos se redactaron con asistencia de IA).
- [ ] Enviar entre el 5/10 07:00 y el 8/10 16:59 (hora de Lima).

---

# PARTE II. Requisitos, estado, pendientes y defensa

## 2. Estado y decisiones

| ID | Fecha | Decisión / hecho | Estado |
|---|---|---|---|
| D-001 | 2026-10-01 | Estructura basada en dos TFM de ejemplo del mismo máster, adaptada a la guía. | Hecho |
| D-006 | 2026-10-02 | Leídas las indicaciones del formulario (5–8/10/2026, un solo formulario). | INSTITUCIONAL |
| D-007 | 2026-10-02 | Propuesta propia con datos reales de BTC (decisión del estudiante); título elegido: «Predicción de la Dirección de Bitcoin utilizando una Red Neuronal Espigante de Segmentos Temporales y Aprendizaje Automático». | Decidido por el estudiante; pendiente de aprobación VIU |
| D-008 | 2026-10-04 | **Red principal de la tesis: E20-ALB** (E20 sin recurrencia + lectura de bosque aleatorio sobre 3 001 estados). Motivo: mejor modelo del banco sintético (0,741) y superior a TIA-LIF; en BTC 2 h empata con ML (0,536). TIA-LIF y E20 oficial quedan como comparación. | Decidido por el estudiante |
| D-009 | 2026-10-04 | Leída la **Guía didáctica TFM 09MIAR 2026-27** (`SESIONES/`): sustituye a la guía pública V03 como referencia (sección 3). | INSTITUCIONAL |
| D-011 | 2026-10-04 | Prueba N87 con datos de BTC (periodos 2021-08 → 2024-03, no usados para elegir nada): no hay una única mejor E20; E20-ALB mayor AUC de E20 en 2021–2024 (0,570, media por bloque), E20-A0C mejor en 2024–2026 (0,546) pero su mejora no se confirma; ML con indicadores ligeramente por encima; la predictibilidad decae. La tesis trata ALB como principal y A0C como variante con indicadores (sección 6.3.3, Tabla 13, Figura 9). | Hecho |
| D-010 | 2026-10-04 | Memoria escrita con la estructura del TFM real de ejemplo (`estructura de trabajo.../TFM-VIU-main/doc/memoria.pdf`): `TESIS TFM/MEMORIA_TFM.md` + `TESIS TFM/figuras/` (11 figuras generadas desde los resultados). La carpeta de la tesis contiene solo la tesis; lo administrativo está en este archivo. | Hecho |

| Dato | Valor | Estado |
|---|---|---|
| Tema y título | ver D-007 | pendiente de aprobación |
| Modalidad | individual (justificación en el formulario) | pendiente de aprobación (la guía dice «grupales salvo casos especiales justificados») |
| Director/a | sin asignar | PENDIENTE |
| Calendario de HITO1, HITO2, HITO3 y depósito | no publicado aún | PENDIENTE (Campus Virtual) |
| Plantilla oficial (Word/LaTeX) | en el Aula | PENDIENTE de descargar |
| Rúbrica detallada | la guía describe los criterios (sección 3.3) | PARCIAL |

## 3. Requisitos de la Guía didáctica 2026-27 (`SESIONES/Guía didáctica TFM 09MIAR_04_A_2026-27.pdf`)

### 3.1. Contenido mínimo de la memoria (en castellano)
Título, autor, tutor, fecha (mes y año), nombre del Máster y logo VIU · **Resumen y Abstract de 200–300 palabras cada uno, indicando explícitamente si se basa en trabajos previos del alumno** · Índice paginado · Objetivos · Estado del arte de la tecnología empleada · Desarrollo del proyecto · Resultados · Valoración y discusión de los resultados · Conclusiones y desarrollos futuros · Referencias bibliográficas · Anexos (incluida la **Declaración de uso de sistemas de IA**).

### 3.2. Formato
A4 · plantilla del Aula (Word o LaTeX) · **Arial o Helvética 11 pt, interlineado 1,5, márgenes de 3 cm** · **40–80 páginas** (nunca menos de 40) sin contar portada, índices, anexos ni bibliografía · cada capítulo empieza en página nueva · figuras y tablas numeradas, con pie, cerca de donde se citan · **normas APA** con correspondencia exacta cita ↔ referencia y orden alfabético · **tercera persona impersonal** · plagio > 30 % (Turnitin) = no se puede defender.

### 3.3. Evaluación
| Componente | Peso | Qué se valora |
|---|---|---|
| Informe del tutor | 30 % | independencia, cumplimiento de objetivos, razonamiento, gestión del tiempo, redacción, puntualidad de los hitos |
| Memoria (tribunal) | 55 % | contenido 60 % (diseño, contribuciones originales, rigor al aplicar y evaluar técnicas, calidad del elemento práctico, acabado); formato 30 % (estructura, redacción, tablas y gráficos, numeración, ortografía, APA); originalidad 10 % |
| Presentación oral (tribunal) | 15 % | exposición y ajuste al tiempo, diapositivas, precisión de las respuestas |

Mínimo 5/10 en cada parte para ponderar. Escala: 9–10 sobresaliente, 7–8,9 notable, 5–6,9 aprobado.

### 3.4. Proceso
1. Formulario de tema (5–8/10/2026) → asignación de tema y director → Compromiso de Tutorización firmado.
2. **Tres borradores (HITOS)** en Word por la actividad del Campus y al tutor; entrega obligatoria.
3. Informe de autorización del director (Apto/No apto). **Tras el informe no se puede modificar la memoria** (si cambia, NO APTO).
4. Depósito: ejemplar PDF, código desarrollado (o nota explicativa), Anexo I (solicitud de defensa), Anexo II (informe del director), expediente académico. Nombre del archivo según el Aula (patrón de la guía: `TFM_APELLIDO1-APELLIDO2.pdf`).
5. Defensa por videoconferencia: diapositivas en PDF el **día anterior** (recomendado ≤ 15); **20 minutos** de exposición + **15 minutos** de preguntas; primera diapositiva con título, autor, tutor, universidad, máster y convocatoria; DNI o pasaporte a mano.

## 4. Pendientes priorizados

**Antes del 8/10/2026 (16:59 Lima):**
1. Enviar el formulario (PARTE I de este archivo).

**Antes del HITO1:**
2. Descargar la plantilla del Aula y el calendario de hitos; anotar fechas en la sección 2.
3. Pasar la memoria a la plantilla y llegar a ≥ 40 páginas (añadir figuras 1–3 y ampliar estado del arte con los resultados del prompt de la sección 8).

**Para cerrar la memoria:**
4. **Prueba final congelada** (Anexo C de la memoria): preregistrar con commit y etiqueta y ejecutar una sola vez en SOL, BNB y XRP a 2 h.
5. Rivales MLP, LSTM y TCN a 2 h con el protocolo final.
6. Verificar todas las referencias marcadas con † (autores, año, DOI).
7. Completar la Declaración de uso de IA (Anexo E) con los usos reales.
8. Confirmación hacia adelante con datos nuevos de BTC (desde octubre de 2026), si el calendario lo permite.

## 5. Reglas para cualquier IA que trabaje aquí (resumen de los antiguos `AGENTS` y `00`)

1. **No inventar** resultados, cifras, valores p, referencias, aprobaciones, fechas ni permisos. Toda cifra de la memoria debe rastrearse a la bitácora del proyecto (`e20-puntos-debiles-v1/plans/PLAN_NOCHE_E20_REAL_v1.md` y adendas). Si falta evidencia, escribir PENDIENTE.
2. Etiquetar lo que no sea un hecho: `INSTITUCIONAL` (guía o Aula), `EJEMPLO` (otro TFM), `RECOMENDACIÓN`, `PENDIENTE_DE_CONFIRMAR`.
3. **No usar el test final** para elegir modelo, variables, umbral ni narrativa; cualquier desviación del protocolo se declara.
4. Elegir la estadística según la unidad independiente: con series temporales, bootstrap por bloques emparejado; no tratar ventanas o pliegues solapados como independientes; informar tamaño del efecto e incertidumbre, no solo valores p.
5. **No crear archivos nuevos en `TESIS TFM`** sin que el estudiante lo pida: allí solo van `MEMORIA_TFM.md` y `figuras/`; registrar cada decisión en la sección 2 de este archivo.
6. Al terminar, informar en cuatro líneas: Hecho · Evidencia · Pendiente · Siguiente acción.

## 6. Lista de control de la memoria (resumen de los antiguos `02`, `04`, `04B`, `05` y `10`)

| Capítulo | Se acepta cuando… |
|---|---|
| Resumen / Abstract | 200–300 palabras; problema, objetivo, método, datos, hallazgo con cifra y conclusión; declara el trabajo previo; nada que no esté en Resultados |
| Introducción | alguien ajeno entiende qué se estudia, por qué es un problema de IA, qué queda fuera y cómo se evalúa |
| Objetivos | cada objetivo tiene método, evidencia y conclusión (matriz O→M→E→R→C) |
| Estado del arte | compara trabajos por datos, protocolo y métricas; termina en el vacío que cubre el TFM; toda afirmación con cita |
| Marco teórico | solo conceptos que se usan después; símbolos definidos |
| Desarrollo | otro investigador puede reconstruir datos, particiones, parámetros, semillas y análisis; dice qué es propio y qué es librería o trabajo previo |
| Resultados | sin números ilustrativos; tamaño de muestra, intervalos y resultados negativos incluidos; cada figura citada en el texto |
| Discusión | separa observación de interpretación; explicaciones alternativas; significación ≠ utilidad práctica |
| Conclusiones | responden cada objetivo; no exceden los datos evaluados |
| Referencias y anexos | APA, sin referencias inventadas; anexos citados desde el texto; declaración de IA coherente con lo hecho |

## 7. Preguntas probables del tribunal (con la respuesta que respalda la memoria)

| Pregunta | Respuesta apoyada en evidencia |
|---|---|
| ¿Qué aporta respecto al artículo de TS-LIF? | Lleva la neurona a un reservorio y a un dominio de baja señal (dirección de BTC) con protocolo preregistrado; explica matemáticamente cuándo ayuda (comparador «rápido − lento», sección 7.1). |
| ¿E20-ALB supera a ML? | En sintéticos supera a RF con entradas estándar (5/9 bancos) y a TIA-LIF; en BTC empata con GBM y logística (0,536 frente a 0,537). El límite es de información. |
| ¿Probaron muchas variantes y eligieron la mejor? | Las hipótesis se preregistraron con commit y etiqueta; se declaran 22 hipótesis y 8 cumplidas; la prueba final se ejecuta una sola vez en activos no usados. |
| ¿Cómo evitaron la fuga de información? | Partición cronológica, escalados solo con entrenamiento, prueba de causalidad por truncamiento, placebos ≈ 0,50, alineación por etiquetas; además se detectó y corrigió una fuga real en TIA-LIF. |
| ¿Por qué un reservorio y no TS-LIF entrenado como en el paper? | Coste mínimo (solo la lectura) y la variante entrenada con atención (TIA-LIF) no fue mejor; la ablación muestra que el valor está en la representación multiescala. |
| ¿Sirve para operar? | No se afirma: AUC 0,54 ≈ 52–53 % de acierto; los costes no se modelaron; el acierto selectivo (+4 puntos) es exploratorio. |
| ¿Qué versión de TS-LIF usan? | La de las ecuaciones del artículo; el código oficial difiere (decaimientos libres, mezcla por canal, γ₁ fijo). |
| ¿Qué cambiarían con más tiempo? | Prueba de equivalencia en activos nuevos, datos de opciones, objetivo de volatilidad y hardware neuromórfico. |

## 8. Prompt de búsqueda bibliográfica para otra IA (versión 3; antes `13_PROMPT_BUSQUEDA_ANTECEDENTES`)

Copiar el bloque en una herramienta con búsqueda web y traer la respuesta para verificarla. **Toda referencia se comprueba abriendo el enlace antes de citarla.**

```text
ROL: asistente de revisión bibliográfica para un TFM del Máster en Inteligencia Artificial (VIU). Solo trabajos REALES y VERIFICABLES; si no puedes comprobar que existe, no lo incluyas.

PROYECTO: red neuronal espigante de reservorio con 1 000 neuronas TS-LIF de dos compartimentos (dendrita y soma; Feng et al., ICLR 2025), sin recurrencia, cuyos estados se leen con un bosque aleatorio (E20-ALB). Objetivo: predecir la DIRECCIÓN del siguiente retorno de Bitcoin con validación cronológica, comparando con regresión logística, bosque aleatorio, gradient boosting, MLP, LSTM y una variante con atención, con las mismas entradas.

RESULTADOS PROPIOS (busca trabajos que los confirmen o contradigan): la dirección de BTC solo es predecible entre 1 minuto y 2 horas (AUC máximo 0,547 a 2 h); a 2 h todos los modelos razonables obtienen AUC 0,53–0,54 y la red empata con gradient boosting; no hay señal diaria; en datos sintéticos con regla de régimen la red supera a un bosque aleatorio con entradas estándar, pero no a uno con características multiescala.

QUÉ BUSCAR (prioridad):
1. Tesis y TFM (español e inglés) sobre redes espigantes o reservorios en series financieras o criptomonedas; comparaciones de ML para la dirección de BTC con validación cronológica. Repositorios: RUA, O2-UOC, TDX, Dialnet, Zenodo, ProQuest, DART-Europe, arXiv, SSRN.
2. Artículos 2015–2026: neuronas espigantes multicompartimento o dendríticas para series temporales; reservorios y máquinas de estado líquido en finanzas; predictibilidad intradía de la dirección de BTC; fuga de información y sobreajuste en backtests; pruebas de equivalencia y bootstrap por bloques para comparar modelos; RESULTADOS NEGATIVOS de modelos complejos frente a referentes simples.
3. Revisiones sistemáticas 2022–2026 sobre redes espigantes en series temporales y ML en criptomonedas.

YA CONOCIDOS (no repetir): Feng et al. 2025 (TS-LIF); Lv et al. 2024; Sharma et al. 2025; Ezinwoke y Rhodes 2025; Walugembe et al. 2026; Baquero 2026; Berger y Koubová 2024; Akyildirim et al. 2021; Audrino y Chassot 2024; Zhang y Vargas 2023.

FORMATO: una tabla por bloque (máx. 15 filas): cita completa; DOI o enlace (obligatorio, si no "SIN DOI NI ENLACE"); tipo; método y datos; métrica y resultado exacto; cómo se evaluó (cronológica, referente simple, pruebas); relevancia y limitación en una frase; nivel de verificación ("LEÍDO completo", "LEÍDO resumen", "NO ABIERTO").
REGLAS: no inventes identificadores ni números ("NO ENCONTRADO" si falta); marca tus opiniones con [OPINIÓN]; al final: vacíos no cubiertos, 5 trabajos clave y 3 que contradicen el enfoque; fecha y consultas exactas usadas.
```

## 9. Fuentes

- **Guía didáctica TFM 09MIAR 2026-27** (`SESIONES/Guía didáctica TFM 09MIAR_04_A_2026-27.pdf`, 22 páginas): referencia institucional vigente.
- Guía pública 09MIAR V03 (https://www.universidadviu.com/sites/universidadviu.com/files/media_files/Gui%CC%81a%20Asignatura%20TFT_09MIAR_V03.pdf): versión anterior, solo de contexto.
- Guía de uso de IA para estudiantes VIU (`SESIONES/P11_G01 Guia uso IA_estudiantes_v02(1).pdf`): modelo de declaración en la página 4.
- Indicaciones del formulario (`SESIONES/INDICACIONES 1.txt`) y títulos asignados de ejemplo (`SESIONES/Asignaciones_11_10_23(1).pdf`).
- TFM de ejemplo: `estructura de trabajo de maestria en inteligencia artificial/TFM/pdf/TFM_DELVALLETORRES-IGNACIO.pdf` (2018–2019) y `.../TFM-VIU-main/TFM-VIU-main/doc/memoria.pdf` (2023–2024). Son ejemplos, no norma.
- Metodología: scikit-learn (errores comunes, validación cruzada, métricas, calibración); Demšar (2006, JMLR) para comparar clasificadores en varios conjuntos de datos.

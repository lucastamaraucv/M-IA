# Estado del proyecto y decisiones verificables

**Actualizado:** 1 de octubre de 2026. Este archivo registra lo que está confirmado, lo que es solo propuesta y qué falta. La otra IA debe actualizarlo al final de cada sesión; nunca debe convertir una hipótesis de trabajo en hecho confirmado.

## Hechos confirmados por archivos

| Hecho | Evidencia |
|---|---|
| Existen dos PDF de ejemplo del Máster Universitario en IA de VIU. | Rutas en [FUENTES.md](FUENTES.md). |
| La guía pública 09MIAR V03 describe un TFM de 12 ECTS, tres hitos y el proceso general de evaluación/defensa. | [Guía 09MIAR V03](https://www.universidadviu.com/sites/universidadviu.com/files/media_files/Gui%CC%81a%20Asignatura%20TFT_09MIAR_V03.pdf). |
| Existe una guía local VIU de uso de IA para estudiantes con modelo de declaración. | [PDF local](../P11_G01%20Guia%20uso%20IA_estudiantes_v02%281%29.pdf). |
| Existe un archivo con propuestas de tema sobre BTC. | `../Seleccion_TFM_BTC_y_catalogo_tutores.xlsx`, hoja `Títulos propuestos`; son propuestas, no asignación. |
| Se creó la carpeta `TESIS TFM` con estructura, metodología, plan y plantillas. | Archivos enlazados en [README.md](README.md). |

## Datos del TFM del estudiante

| Campo | Valor actual | Estado | Quién/qué puede confirmarlo |
|---|---|---|---|
| Tema y título | Sin confirmar; BTC es solo una opción. | PENDIENTE | Estudiante, propuesta aceptada y director. |
| Modalidad | Investigación o aplicado, sin elegir. | PENDIENTE | Estudiante/director. |
| Director | No identificado como asignación confirmada. | PENDIENTE | Campus/coordinación. |
| Convocatoria y calendario | No proporcionados. | PENDIENTE | Campus Virtual. |
| Plantilla y rúbrica vigentes | No proporcionadas. | PENDIENTE | Campus Virtual. |
| Datos, fuente y licencia | No confirmados. | PENDIENTE | Estudiante/fuente de datos/director. |
| Pregunta y objetivos | No confirmados. | PENDIENTE | Estudiante/director tras revisar viabilidad. |
| Referente, métrica y protocolo | No definidos. | PENDIENTE | Diseño metodológico posterior a tema/datos. |
| Resultados | Ningún experimento de la tesis del estudiante ejecutado aquí. | PENDIENTE | Registro de ejecución reproducible. |
| Hitos, memoria y defensa | Ninguna entrega del estudiante verificada aquí. | PENDIENTE | Comprobantes del aula y documentos finales. |

## Decisiones de estructura ya adoptadas en esta carpeta

| ID | Fecha | Decisión | Fundamento | Alcance / estado |
|---|---|---|---|---|
| D-001 | 2026-10-01 | Usar los dos TFM de IA como ejemplos principales de estructura. | Ambos son del mismo máster; sus índices difieren. | RECOMENDACIÓN documentada; adaptar a plantilla vigente. |
| D-002 | 2026-10-01 | Separar requisitos de la guía pública, ejemplos y recomendaciones. | Evita presentar decisiones de antiguos estudiantes como obligaciones. | Activo en `AGENTS.md`, `00` y `09`. |
| D-003 | 2026-10-01 | Mantener BTC en un archivo opcional. | El libro local contiene títulos propuestos, no aprobación de tema. | Pendiente de respuesta del estudiante. |
| D-004 | 2026-10-01 | No fijar una prueba estadística universal. | La técnica depende de unidad independiente, pregunta y partición. | Procedimiento en `04B`. |
| D-005 | 2026-10-01 | Añadir un protocolo de continuidad para otra IA y criterios de cierre por requisito/capítulo. | El usuario pidió que cada punto pudiera seguirse sin suposiciones. | `AGENTS.md`, `00`, `09`, `10` y este registro. |

## Próximo paso determinista

1. Solicitar o leer **tema confirmado y director**. Si el estudiante confirma BTC, adaptar `08_OPCION_BTC.md` y completar la ficha A de `05_PLANTILLAS.md`; si confirma otro tema, crear un archivo temático nuevo y conservar BTC como opción histórica.
2. Obtener **plantilla, rúbrica, instrucciones y calendario del Campus Virtual**. Registrar nombre, edición, versión, fecha y fuente; comparar contra VIU09 V03. Resolver diferencias antes de fijar formato/hitos.
3. Completar datos y viabilidad. Solo entonces cerrar objetivos y protocolo; elegir estadísticas con `04B`.
4. Actualizar [09_MATRIZ_REQUISITOS.md](09_MATRIZ_REQUISITOS.md) fila por fila con evidencia real.

## Registro de cambios futuro

Añade entradas con este formato, conservando las anteriores:

| Fecha | Requisito/decisión | Estado anterior → nuevo | Evidencia exacta | Acción y efecto | Verificado por |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

`VERIFICADO` requiere archivo, página, sección, celda o comprobante identificable y un criterio de aceptación satisfecho. `NO_APLICA` requiere justificación. Para hechos externos que cambian con el tiempo, anota la fecha de consulta.

## Verificación del paquete documental

El 1 de octubre de 2026 se comprobó que la carpeta contiene 17 archivos Markdown, que los 34 identificadores de la matriz son únicos y que los enlaces locales de Markdown resuelven a archivos existentes. Esta verificación **no** cambia el estado de los requisitos académicos del estudiante, que siguen pendientes de evidencia propia.

## Registro 2026-10-02 (sesión con E20)

| ID | Fecha | Decisión / hecho | Estado | Evidencia |
|---|---|---|---|---|
| D-006 | 2026-10-02 | Se leyó `INDICACIONES 1.txt` (idéntico en `SESIONES/` y en esta carpeta): formularios del 5 al 8/10/2026 (23:59 España); un solo formulario; propuesta propia exige título, contexto, objetivos, metodologías, dataset, tutor y grupo/justificación. | `INSTITUCIONAL` | `SESIONES/INDICACIONES 1.txt` |
| D-007 | 2026-10-02 | Borrador de propuesta propia basada en la red E20 y alternativa de 5 opciones del listado, en [12_PROPUESTA_FORMULARIO_TFM.md](12_PROPUESTA_FORMULARIO_TFM.md). Decisión A/B, tutor y modalidad pendientes del estudiante. | `PENDIENTE_DE_CONFIRMAR` | archivo 12 |

## 2026-10-02 — Formulario v2
- Creado `14_FORMULARIO_FINAL_v2.md`: título nuevo (reservorio TS-LIF, movimiento y dirección de BTC, evaluación cronológica con control sintético), textos breves, antecedentes (15 artículos de REFERENCIA BIBLIOGRAFICA), justificación individual para Lucas Ivan Tamara Trejo y lista de verificación.
- Pendiente del estudiante: decidir A/B, tutor, confirmar modalidad individual y enviar él mismo entre 5/10 14:00 y 8/10 23:59 (España).

# Protocolo operativo para continuar el TFM sin suposiciones

## 1. Vocabulario de autoridad y estado

| Etiqueta | Significado | Qué permite hacer |
|---|---|---|
| `INSTITUCIONAL` | Texto de la guía VIU o documento oficial de la convocatoria, con referencia exacta. | Aplicar su instrucción si corresponde a la edición del estudiante. |
| `EJEMPLO` | Rasgo observado en un TFM previo. | Considerarlo como posibilidad de estructura; nunca imponerlo. |
| `RECOMENDACIÓN` | Decisión metodológica propuesta y justificada. | Adoptarla solo tras comprobar pregunta, datos, recursos y director. |
| `PENDIENTE_DE_CONFIRMAR` | Falta fuente, versión, dato o decisión. | Preparar opciones y preguntas; no afirmar que está decidido. |

| Estado | Definición comprobable |
|---|---|
| `PENDIENTE` | No hay entrega o evidencia suficiente. |
| `EN_CURSO` | Hay trabajo iniciado con evidencia parcial identificada. |
| `VERIFICADO` | Se cumplen todos los criterios de aceptación y existe evidencia enlazada. |
| `NO_APLICA` | Se justificó por qué la condición de activación no se cumple. |
| `BLOQUEADO` | Un dato o documento externo imprescindible impide avanzar ese requisito concreto; se identificó quién debe aportarlo. |

`PENDIENTE` o `BLOQUEADO` de un requisito no paraliza tareas independientes. Una recomendación no se convierte en obligación por aparecer en este repositorio.

## 2. Orden de lectura y ejecución

1. **Contexto:** lee [README.md](README.md), [RESUMEN_PARA_CONTINUAR.md](RESUMEN_PARA_CONTINUAR.md) y [11_ESTADO_Y_DECISIONES.md](11_ESTADO_Y_DECISIONES.md).
2. **Normativa:** lee [01_REQUISITOS_VIU.md](01_REQUISITOS_VIU.md), [FUENTES.md](FUENTES.md) y cualquier documento nuevo de Campus Virtual. Registra versión, fecha y procedencia. No uses los PDF de tesis como norma.
3. **Definición:** completa la ficha A de [05_PLANTILLAS.md](05_PLANTILLAS.md) con respuestas del estudiante y evidencia. Si el tema no está confirmado, trabaja solo en elementos independientes del tema.
4. **Trazabilidad:** crea objetivos identificados `O1`, `O2`… y vincula cada uno con `M` (método), `E` (experimento/evidencia), `R` (resultado) y `C` (conclusión). La matriz B de [05_PLANTILLAS.md](05_PLANTILLAS.md) es el registro.
5. **Protocolo:** define datos, particiones, referente, métrica primaria, incertidumbre, límites y plan de análisis antes de ver el resultado final. Sigue [04_METODOLOGIA_Y_ESTADISTICA.md](04_METODOLOGIA_Y_ESTADISTICA.md) y [04B_DECISION_ESTADISTICA.md](04B_DECISION_ESTADISTICA.md).
6. **Ejecución:** guarda código, configuración, datos permitidos, predicciones, resultados y bitácora de cambios. Nunca rellenes una tabla de resultados con valores ilustrativos como si fueran reales.
7. **Redacción:** usa la plantilla oficial; adapta [02_ESTRUCTURA_MEMORIA.md](02_ESTRUCTURA_MEMORIA.md) y verifica cada apartado con [10_CRITERIOS_POR_CAPITULO.md](10_CRITERIOS_POR_CAPITULO.md).
8. **Hitos y cierre:** usa [03_PLAN_DE_TRABAJO.md](03_PLAN_DE_TRABAJO.md) y [06_ENTREGA_Y_DEFENSA.md](06_ENTREGA_Y_DEFENSA.md), pero sustituye fechas y formatos preliminares por instrucciones de la convocatoria.

## 3. Puertas de control

| Puerta | Se abre cuando… | Evidencia mínima | Trabajo que depende de ella |
|---|---|---|---|
| G0: tema | Tema y modalidad confirmados por estudiante y director/convocatoria. | Título/alcance acordados y fuente de confirmación. | Personalizar índice y literatura específica. |
| G1: reglas | Plantilla, rúbrica, calendario e instrucciones de edición disponibles. | Archivos/versiones y enlaces registrados. | Fijar formato, extensión, entregas y evaluación final. |
| G2: viabilidad | Datos, permisos, objetivo, referente y recursos identificados. | Ficha del proyecto y riesgo principal resuelto. | Comprometer un protocolo de experimento. |
| G3: protocolo | Métrica primaria, unidad independiente, particiones y plan de análisis escritos y revisados. | Protocolo con fecha/versión. | Entrenar y comparar como estudio definitivo. |
| G4: ejecución | Código y particiones reproducibles; resultados crudos guardados. | Registro de experimentos y archivos de salida. | Interpretar números en la memoria. |
| G5: interpretación | Objetivos conectados con resultados, incertidumbre y límites. | Matriz de trazabilidad completa y tablas verificadas. | Redactar conclusiones definitivas. |
| G6: memoria | Plantilla oficial, citas, tablas, uso de IA y revisión de contenido completos. | Versión revisada y comentarios del director resueltos. | Solicitar autorización de depósito. |
| G7: depósito | Autorización/documentos/fechas según aula. | Comprobantes y PDF final. | Defensa. |

Si una puerta no está abierta, se puede preparar material, explorar opciones o hacer pilotos claramente etiquetados. No se deben publicar como resultados definitivos ni declarar completada la etapa dependiente.

## 4. Registro de decisiones obligatorio

Cada decisión nueva debe tener: **ID**, fecha, pregunta, opciones consideradas, evidencia, criterio elegido, responsable de confirmación, efecto en capítulos/experimentos y estado. Regístrala en [11_ESTADO_Y_DECISIONES.md](11_ESTADO_Y_DECISIONES.md). Si se cambia una decisión, conserva la anterior como historial y explica el efecto sobre resultados ya calculados.

## 5. Respuesta cuando falta información

- **Falta tema:** no escoger BTC automáticamente; dejar una ficha lista y continuar reglas institucionales y estructura genérica.
- **Faltan documentos del aula:** usar la guía pública solo para planificar, marcar como provisionales la extensión, el formato, fechas y cualquier requisito específico.
- **Faltan datos o permisos:** no descargar ni procesar fuentes restringidas. Diseñar un protocolo candidato y una alternativa de datos públicos.
- **Falta suficiente muestra independiente:** priorizar descripción, intervalos justificados y límites; no inventar significación estadística.
- **Se contradicen fuentes:** identificar ambas con página/versión, aplicar la de la convocatoria vigente si es clara y elevar el conflicto al director/coordinación si no lo es.

## 6. Contrato de salida para cada trabajo de otra IA

Al entregar cualquier capítulo, análisis o edición, informa en cuatro líneas: `Hecho`, `Evidencia`, `Pendiente` y `Siguiente acción`. Actualiza la matriz de requisitos y el estado. No declares `VERIFICADO` un requisito solo porque redactaste un párrafo.

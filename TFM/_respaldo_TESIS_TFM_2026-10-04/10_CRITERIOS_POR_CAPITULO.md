# Criterios de aceptación de cada apartado de la memoria

Esta lista verifica el **contenido académico**. El orden, los nombres, formato y extensión deben adaptarse a la plantilla oficial. La otra IA puede fusionar capítulos, pero debe conservar sus funciones y marcar la ubicación final de cada una. Un apartado pasa a `VERIFICADO` solo si cumple sus condiciones y existe un borrador localizable.

## Preliminares: portada, índices y resumen

**Entrada:** plantilla de la edición, título confirmado, datos de autor/dirección/convocatoria, resultados finales para el resumen.

**Acción:** completar portada oficial; generar índices a partir de títulos reales; escribir el resumen al final de la investigación; agregar índices de figuras/tablas/algoritmos si lo exige la plantilla o el volumen lo justifica.

**Salida:** preliminares de la memoria, con número de página y títulos coherentes.

**Aceptación:** portada sin datos supuestos; índice navega a secciones reales; resumen expresa problema, objetivo, método, datos, hallazgo cuantificado y conclusión sin agregar resultados nuevos; palabras clave descriptivas. Abstract solo si corresponde a la convocatoria o al acuerdo con el director. **IDs:** VIU-03, MEM-01, MEM-02.

## 1. Introducción

**Entrada:** ficha del TFM, fuente del problema, objetivos acordados y alcance.

**Acción:** explicar el contexto suficiente para comprender el problema; delimitar población/sistema, tarea y horizonte; justificar relevancia; describir aporte previsto y mapa de capítulos.

**Salida:** problema formulado en términos verificables, con alcance explícito.

**Aceptación:** una persona ajena al proyecto puede identificar qué se estudiará, por qué es un problema de IA, a quién afecta, qué queda fuera y cómo se evaluará en términos generales. No hay promesas de rendimiento ni afirmaciones de novedad sin contraste bibliográfico. **IDs:** VIU-02, INV-01.

## 2. Estado del arte

**Entrada:** pregunta de investigación, términos de búsqueda, artículos y documentación primaria.

**Acción:** definir alcance de búsqueda; registrar dónde/cuándo se buscó si se pretende una revisión trazable; resumir métodos comparables por datos, protocolo, métricas y hallazgos; identificar limitaciones y el vacío que motiva el TFM.

**Salida:** texto comparativo y matriz de literatura. Una revisión sistemática solo se denomina así si se documenta el procedimiento correspondiente; en otro caso, llámala revisión narrativa o bibliográfica.

**Aceptación:** no es una sucesión de resúmenes aislados; cada comparación cita fuentes reales; las afirmaciones de «mejor» o «primero» tienen contexto; el último apartado conduce lógicamente a la propuesta. **IDs:** INV-02, VIU-14.

## 3. Marco teórico

**Entrada:** conceptos y fórmulas usados de verdad en método/resultados.

**Acción:** definir notación, supuestos y mecanismos técnicos necesarios, con fuentes. Separar conocimiento establecido de aportes del estudiante.

**Salida:** fundamentos suficientes para seguir metodología sin convertir el capítulo en un manual general de IA.

**Aceptación:** cada concepto presentado vuelve a usarse después; símbolos y términos son consistentes; fórmulas tienen variables y condiciones definidas. Si es breve, documenta su integración en el estado del arte. **IDs:** MEM-01, VIU-14.

## 4. Objetivos y preguntas

**Entrada:** problema delimitado, vacío bibliográfico y recursos disponibles.

**Acción:** redactar objetivo general y objetivos específicos con verbos observables: diseñar, implementar, comparar, evaluar, analizar. Para cada objetivo registrar método, experimento/evidencia y criterio de éxito; las hipótesis solo se agregan si son comprobables.

**Salida:** matriz `O→M→E→R→C` en [05_PLANTILLAS.md](05_PLANTILLAS.md).

**Aceptación:** no hay objetivos que dependan de datos inaccesibles; cada objetivo puede cerrarse con evidencia; los criterios no se reescriben después de ver el test final sin marcar desviación. **IDs:** INV-01, MEM-04.

## 5. Metodología y desarrollo

**Entrada:** protocolo previo, datos con permisos, referente, propuesta, recursos y decisiones estadísticas.

**Acción:** describir unidad independiente; fuente y selección de datos; exclusiones; preprocesamiento por partición; arquitectura/algoritmos; parámetros y espacio de búsqueda; baselines; particiones y control de fuga; métrica primaria/secundarias; incertidumbre, análisis estadístico aplicable, entorno y reproducibilidad. Explicar qué fue desarrollado por el estudiante frente a librerías o trabajo previo.

**Salida:** método suficientemente preciso para que otro investigador reproduzca las tablas centrales, sujeto a la disponibilidad legal de datos.

**Aceptación:** hay un diagrama o descripción inequívoca del flujo de datos; parámetros y semillas identificados; el test final no interviene en el ajuste; las mismas condiciones se aplican a comparadores; permisos y límites éticos constan. Si una prueba estadística se omite, se explica por qué. **IDs:** INV-03 a INV-09, VIU-16, MEM-03.

## 6. Resultados

**Entrada:** registros de ejecución, predicciones, tablas originales y protocolo.

**Acción:** presentar primero muestra y experimentos realizados; después métricas centrales frente al referente y variabilidad/incertidumbre; resultados secundarios, sensibilidad, errores o subgrupos según el objetivo. Indicar muestras/denominadores, unidades, dirección de cada métrica y costo cuando importa.

**Salida:** tablas y figuras que pueden rastrearse a una ejecución concreta.

**Aceptación:** ninguna tabla contiene números ilustrativos; diferencias se calculan correctamente; intervalos/pruebas usan la unidad correcta; resultados negativos se incluyen; toda figura es citada e interpretada en el texto. **IDs:** INV-10, INV-11, MEM-03, MEM-05.

## 7. Discusión

**Entrada:** objetivos, resultados, literatura y limitaciones conocidas.

**Acción:** explicar qué significan las diferencias observadas, qué mecanismos podrían explicarlas, si son consistentes con estudios previos y bajo qué condiciones podrían generalizarse. Separar observación de interpretación.

**Salida:** argumento crítico que no repite todas las tablas.

**Aceptación:** cada afirmación central apunta a un resultado y, cuando compara literatura, a una cita; distingue significación estadística de utilidad práctica; reconoce resultados inesperados y explicaciones alternativas. **IDs:** INV-12, MEM-04.

## 8. Conclusiones

**Entrada:** matriz de trazabilidad completada y discusión.

**Acción:** responder objetivo por objetivo; sintetizar aporte original y alcance. No introducir experimentos ni referencias nuevos para apoyar conclusiones.

**Salida:** cierre breve, concreto y respaldado.

**Aceptación:** ninguna conclusión excede población, datos o período evaluados; todos los objetivos tienen respuesta; una mejora modesta se informa como tal. **IDs:** MEM-04, INV-12.

## 9. Limitaciones y futuro

**Entrada:** incidencias experimentales, exclusiones, datos no disponibles, variabilidad y preguntas sin resolver.

**Acción:** clasificar límites en datos, método, cómputo, validez externa y ética cuando correspondan; explicar su efecto probable; proponer mejoras conectadas con esos límites.

**Salida:** lista priorizada de condiciones bajo las cuales el resultado podría cambiar y próximos experimentos concretos.

**Aceptación:** no se confunden tareas no realizadas con resultados; cada línea futura indica qué pregunta resolvería. **IDs:** INV-12, MEM-06.

## Referencias, anexos y declaración de uso de IA

**Entrada:** todas las citas, figuras, código de apoyo, registros de IA y normas del aula.

**Acción:** cotejar cita ↔ referencia; verificar DOI/URL, autor, año y título; incluir anexos solo cuando respaldan un argumento; preparar declaración de IA con usos reales y revisión humana.

**Salida:** bibliografía consistente, anexos referidos desde el cuerpo y declaración según la guía de la edición.

**Aceptación:** no hay referencias inventadas, citas rotas, marcadores `?`, capturas ilegibles ni anexos desconectados; no se divulgan datos sensibles; declaración coincide con el registro. **IDs:** VIU-14 a VIU-16, MEM-05, MEM-06.

## Regla final de liberación

Antes de marcar la memoria como lista: coteja todos los `MEM-*` de [09_MATRIZ_REQUISITOS.md](09_MATRIZ_REQUISITOS.md), los documentos de aula, la versión revisada por el director y la lista de [06_ENTREGA_Y_DEFENSA.md](06_ENTREGA_Y_DEFENSA.md). La otra IA puede identificar defectos y preparar correcciones, pero la autorización de depósito solo se registra cuando existe el documento correspondiente.

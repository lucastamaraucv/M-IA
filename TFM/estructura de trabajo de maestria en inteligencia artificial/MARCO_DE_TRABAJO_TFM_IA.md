# Marco de trabajo para desarrollar un TFM en Inteligencia Artificial

## Base y alcance

Este marco se deriva **solo de dos PDF del Máster Universitario en Inteligencia Artificial de la VIU**: un TFM del curso 2018–2019 sobre selección de atributos y otro del curso 2023–2024 sobre métodos semisupervisados. Es una propuesta de organización basada en ejemplos reales; **no acredita los requisitos oficiales actuales** del máster. La estructura final debe ajustarse a la guía y a las indicaciones del tutor vigentes para tu convocatoria.

## Estructura comparada de las dos tesis de IA

| Elemento | TFM 2018–2019 | TFM 2023–2024 | Lectura para tu tesis |
|---|---|---|---|
| Preliminares | Portada e índice general | Portada, agradecimientos, índice general e índices de figuras, tablas y algoritmos | Portada e índice general son constantes; los demás preliminares dependen del documento. |
| Resumen | Capítulo 1 | Antes del capítulo 1 | Inclúyelo; su posición y numeración pueden variar. |
| Introducción | No es capítulo independiente | Capítulo 1 | Conviene un capítulo que explique problema, motivación, enfoque y recorrido del texto. |
| Estado del arte | Capítulo 3, muy extenso | Capítulo 2, centrado en investigación previa | Revisar y comparar trabajos existentes es una pieza central. |
| Marco teórico | Integrado en el estado del arte | Capítulo 3 independiente | Sepáralo cuando las bases técnicas necesiten explicación extensa. |
| Objetivos | Capítulo 2 | Capítulo 4, con objetivo general y específicos | Declara objetivos verificables; su ubicación es flexible. |
| Métodos | Capítulo 4, «Materiales y métodos» | Capítulo 5, «Metodología y Desarrollo» | Describe datos, diseño, algoritmos, implementación y evaluación. |
| Resultados | Capítulo 5, por conjunto de datos y validación | Capítulo 6, por línea experimental | Ordena los resultados según los objetivos y experimentos reales. |
| Discusión | Capítulo 6 independiente | Apartado 6.3 del capítulo de resultados | Debe existir una interpretación crítica, sea capítulo o apartado. |
| Conclusiones | Capítulo 7 | Capítulo 7 | Cierra respondiendo a los objetivos y apoyándose en resultados. |
| Limitaciones y futuro | Dentro de la discusión final | Capítulo 8 independiente | Haz explícitos alcance, límites y trabajo futuro. |
| Referencias | Rótulo final «Anexo-Bibliografía» | Referencias bibliográficas separadas | Incluye referencias completas y comprobables. |
| Apéndices | No aparecen como apartados separados | Dos apéndices, para resultados adicionales y un visualizador | Reserva material extenso de apoyo para anexos si hace falta. |

La tesis de 2023–2024 **no incluye en su índice un abstract en inglés ni una lista de siglas**. Tampoco son rasgos exigibles por el mero hecho de aparecer en una tesis de otra carrera.

## Índice maestro recomendado para tu TFM

La siguiente plantilla combina los elementos de los dos PDF de IA. Los títulos son genéricos: sustitúyelos por los de tu problema, sin copiar las familias de métodos ni los experimentos de los ejemplos.

```text
Portada
Agradecimientos [opcional]
Índice general
Índice de figuras / tablas / algoritmos [si el volumen lo justifica]
Resumen

1. Introducción
   1.1. Contexto y problema concreto
   1.2. Motivación y relevancia
   1.3. Propuesta o enfoque general
   1.4. Alcance y organización del documento

2. Estado del arte
   2.1. Antecedentes directamente relacionados
   2.2. Métodos y resultados de trabajos previos
   2.3. Comparación crítica y vacío que aborda el TFM

3. Marco teórico [capítulo propio si la base técnica es extensa]
   3.1. Conceptos y definiciones necesarios
   3.2. Algoritmos, modelos o técnicas de base
   3.3. Supuestos y limitaciones teóricas relevantes

4. Objetivos
   4.1. Objetivo general
   4.2. Objetivos específicos
   4.3. Preguntas de investigación o hipótesis [si encajan con el estudio]

5. Metodología y desarrollo
   5.1. Diseño del estudio y alcance experimental
   5.2. Datos: origen, selección y características
   5.3. Preparación de datos
   5.4. Métodos de referencia y método propuesto
   5.5. Diseño e implementación del sistema o algoritmos
   5.6. Protocolo experimental y configuración
   5.7. Métricas y procedimiento de evaluación

6. Resultados
   6.1. Experimentos y resultados por objetivo o método
   6.2. Comparación con métodos de referencia
   6.3. Análisis de parámetros o de sensibilidad [si procede]
   6.4. Síntesis de hallazgos

7. Discusión
   7.1. Interpretación de los hallazgos
   7.2. Relación con el estado del arte y los objetivos
   7.3. Robustez, límites y explicaciones alternativas

8. Conclusiones
   8.1. Respuesta a cada objetivo o pregunta
   8.2. Aportaciones del trabajo

9. Limitaciones y perspectivas de futuro
   9.1. Límites de datos, métodos, tiempo o alcance
   9.2. Mejoras y trabajo futuro

Referencias bibliográficas
Apéndices [si hay resultados extensos, detalles técnicos o herramientas auxiliares]
```

**Variantes válidas observadas en los PDF:** el marco teórico puede integrarse en el estado del arte; objetivos pueden ir al comienzo; resultados y discusión pueden formar un único capítulo; limitaciones y futuro pueden integrarse en la discusión o las conclusiones. Mantén cada función académica reconocible aunque cambie su ubicación.

## Qué debe resolver cada parte

| Parte | Pregunta que responde | Evidencia o contenido esperable |
|---|---|---|
| Resumen | ¿Qué problema se abordó, cómo y con qué hallazgos? | Problema, objetivo, método, datos, resultados principales y conclusión breve. |
| Introducción | ¿Por qué merece hacerse este trabajo? | Problema delimitado, contexto, motivación, contribución prevista y mapa del documento. |
| Estado del arte | ¿Qué se ha intentado ya y qué falta? | Trabajos comparables, fortalezas, límites y justificación de la elección del enfoque. |
| Marco teórico | ¿Qué conceptos necesita el lector para comprender el método? | Definiciones, fundamentos, notación y supuestos pertinentes; evitar contenido general sin función. |
| Objetivos | ¿Qué resultados observables determinarán si el TFM cumple su propósito? | Un objetivo general y objetivos específicos que puedan rastrearse en métodos, resultados y conclusiones. |
| Metodología | ¿Cómo se obtuvo la evidencia? | Procedencia de datos, selección, preparación, algoritmos, configuración, protocolo, métricas y decisiones de implementación. |
| Resultados | ¿Qué ocurrió al aplicar el método? | Tablas, figuras y comparaciones directamente ligadas al protocolo; también resultados desfavorables. |
| Discusión | ¿Qué significan los resultados? | Interpretación frente a objetivos y literatura; condiciones bajo las que son válidos. |
| Conclusiones | ¿Qué se puede afirmar con la evidencia disponible? | Respuestas concretas por objetivo, aportaciones y alcance de las afirmaciones. |
| Limitaciones y futuro | ¿Qué queda fuera y qué se haría después? | Restricciones reales, efectos posibles en resultados y mejoras justificadas. |
| Apéndices | ¿Qué detalle respalda el cuerpo sin interrumpirlo? | Resultados adicionales, diseños, pseudocódigo o documentación complementaria. |

## Matices metodológicos observados que conviene planificar

1. **Trazabilidad de objetivos.** En el TFM de 2023–2024 los objetivos específicos enumeran revisión, implementación, selección de datos, experimentos y comparación; la discusión y las conclusiones vuelven a esos objetivos. Prepara una matriz simple: objetivo → método → experimento → resultado → conclusión.
2. **Datos y protocolo explícitos.** Una tesis usa dos conjuntos de datos y dos esquemas de validación; la otra selecciona 24 conjuntos de datos, explica sus proporciones de etiquetado y la validación cruzada. Justifica tus datos, particiones y repeticiones según tu problema.
3. **Comparación justa.** La tesis de 2023–2024 declara modelos de referencia y razona cómo fijar parámetros para comparar; también documenta cuando excluye un conjunto por coste de cómputo. Explica tus bases de comparación y cualquier excepción.
4. **Métricas antes de interpretar.** El TFM de 2018–2019 enumera métricas en métodos y después las usa en resultados. Define las métricas apropiadas para tu tarea y cómo calcularás cada una antes de presentar resultados.
5. **Resultados y discusión cumplen funciones distintas.** Primero presenta qué ocurrió; después interpreta por qué, si responde al objetivo y cómo se relaciona con trabajos previos. Los dos contenidos pueden estar en capítulos separados o en uno solo.
6. **Limitaciones honestas.** La tesis de 2023–2024 explica límites de tiempo, cómputo y alcance. Una conclusión sólida evita afirmar más de lo que permiten los datos y las condiciones probadas.
7. **Material complementario.** El TFM más reciente traslada resultados adicionales y documentación de una herramienta a apéndices. Usa ese espacio para detalles verificables que harían pesado el cuerpo principal.
8. **Referencias verificables.** En el PDF de 2023–2024 aparecen signos «?» donde deberían resolverse algunas citas. Al redactar tu tesis, comprueba que cada cita en el texto esté completa y figure en las referencias finales.

## Secuencia práctica de redacción

1. Delimita tema, problema, alcance y objetivos.
2. Reúne y compara la literatura; define el vacío que abordarás.
3. Diseña datos, método, referentes, métricas y protocolo antes de experimentar.
4. Implementa y registra decisiones, parámetros, versiones y resultados.
5. Escribe metodología y resultados a partir de registros verificables.
6. Redacta discusión, conclusiones y limitaciones vinculadas a cada objetivo.
7. Termina resumen, índices, referencias y anexos; revisa coherencia entre citas, figuras, tablas y texto.

## Fuentes PDF

- `TFM/pdf/TFM_DELVALLETORRES-IGNACIO.pdf` (curso 2018–2019; índice y capítulos principales).
- `TFM-VIU-main/TFM-VIU-main/doc/memoria.pdf` (curso 2023–2024; índice general, introducción, objetivos, metodología, resultados, conclusiones y limitaciones).

# Estructura de la memoria

Este índice usa como base dos TFM reales del **Máster Universitario en IA**: uno de 2018–2019, que separa estado del arte, resultados, discusión y conclusiones, y otro de 2023–2024, que además separa introducción, marco teórico, objetivos generales/específicos y limitaciones. Es una **estructura de trabajo** para adaptar a la plantilla VIU de tu convocatoria.

Para escribir o verificar cada capítulo, usa las entradas, salidas y criterios de [10_CRITERIOS_POR_CAPITULO.md](10_CRITERIOS_POR_CAPITULO.md). Registra en [11_ESTADO_Y_DECISIONES.md](11_ESTADO_Y_DECISIONES.md) cualquier fusión o cambio de capítulos exigido por la plantilla o acordado con el director.

## Índice maestro adaptable

```text
Portada oficial
Agradecimientos [opcionales]
Índice general
Índices de figuras, tablas y algoritmos [si procede]
Resumen y palabras clave
Abstract y keywords [solo si la plantilla o director lo solicita]

1. Introducción
   1.1. Contexto y problema delimitado
   1.2. Relevancia, motivación y justificación
   1.3. Enfoque y aportación prevista
   1.4. Alcance, límites iniciales y organización del texto

2. Estado del arte
   2.1. Estrategia de búsqueda y selección de literatura [si aporta valor]
   2.2. Trabajos y métodos comparables
   2.3. Comparación crítica y vacío que aborda el TFM

3. Marco teórico [integrable en 2 si es breve]
   3.1. Conceptos, notación y fundamentos esenciales
   3.2. Técnicas y modelos de base
   3.3. Supuestos y límites relevantes

4. Objetivos
   4.1. Objetivo general
   4.2. Objetivos específicos verificables
   4.3. Preguntas o hipótesis [si corresponden al diseño]

5. Metodología y desarrollo
   5.1. Tipo y diseño del estudio
   5.2. Datos: fuente, permisos, unidad de análisis y selección
   5.3. Exploración y preparación de datos
   5.4. Métodos de referencia y propuesta
   5.5. Implementación y entorno de cómputo
   5.6. Protocolo de validación y comparación
   5.7. Métricas, incertidumbre y análisis estadístico elegido
   5.8. Reproducibilidad y consideraciones éticas pertinentes

6. Resultados
   6.1. Datos y experimentos efectivamente realizados
   6.2. Resultados principales por objetivo o experimento
   6.3. Comparación con métodos de referencia
   6.4. Análisis de sensibilidad, errores o subgrupos [si aporta evidencia]

7. Discusión
   7.1. Interpretación frente a objetivos e hipótesis
   7.2. Comparación con la literatura
   7.3. Robustez, explicaciones alternativas y alcance

8. Conclusiones
   8.1. Respuesta concreta a cada objetivo
   8.2. Aportaciones sustentadas por los resultados

9. Limitaciones y trabajo futuro
   9.1. Límites de datos, diseño, cómputo y generalización
   9.2. Mejoras y próximos experimentos justificables

Referencias bibliográficas
Anexos: resultados adicionales, protocolos, pseudocódigo, manuales o evidencias
Declaración de uso de IA [según la pauta de la universidad]
```

## Función de cada parte y evidencia de cierre

| Parte | Debe contestar | Comprobación antes de cerrar |
|---|---|---|
| Introducción | ¿Qué problema preciso resuelvo y por qué? | Puede expresarse en pocas frases y su alcance es realista. |
| Estado del arte | ¿Qué existe, cómo se evaluó y qué falta? | Los trabajos se comparan por método, datos y resultados; cada afirmación tiene fuente. |
| Marco teórico | ¿Qué necesita saber el lector para entender la propuesta? | Se explican solo conceptos utilizados después. |
| Objetivos | ¿Qué debo demostrar o construir? | Cada objetivo tiene una tarea, una evidencia y una conclusión prevista. |
| Metodología | ¿Cómo obtendré resultados creíbles y repetibles? | Otro investigador podría reconstruir datos, particiones, parámetros y análisis. |
| Resultados | ¿Qué ocurrió? | Hay cifras, unidades, tablas/figuras legibles y referencia al protocolo. |
| Discusión | ¿Qué significan los resultados? | Se distinguen hallazgos, interpretación y límites. |
| Conclusiones | ¿Qué quedó demostrado? | Cada afirmación está respaldada y se corresponde con un objetivo. |
| Limitaciones | ¿Qué no puedo afirmar? | Se exponen sesgos, fallos, condiciones de validez y mejoras concretas. |

## Decisiones de estructura que puedes tomar con el director

- **Estado del arte y marco teórico:** juntos si el fundamento técnico es breve; separados si la revisión de trabajos y la explicación de conceptos son amplias. El TFM de IA de 2023–2024 los separa; el de 2018–2019 no.
- **Objetivos:** antes o después del estado del arte. Elige una ubicación y asegura que el lector entiende el problema antes de leerlos.
- **Resultados y discusión:** un capítulo combinado, como el TFM 2023–2024, o dos separados, como el TFM 2018–2019. Evita repetir tablas en la discusión.
- **Limitaciones y futuro:** capítulo propio o apartado final. Hazlos explícitos en cualquier caso.
- **Anexos:** no son un depósito de material irrelevante. Úsalos para el detalle que respalda resultados y que interrumpe la lectura principal.

## Reglas de coherencia interna

1. Problema → objetivo → método → experimento → resultado → conclusión.
2. Toda tabla y figura tiene título, unidades cuando aplican, fuente y comentario en el texto.
3. Las referencias citadas en el texto figuran en bibliografía y viceversa según la norma elegida.
4. Los resultados desfavorables se muestran y se interpretan; no se omiten por no favorecer la hipótesis.
5. Los nombres de conjuntos de datos, modelos, métricas y particiones son constantes en todo el documento.

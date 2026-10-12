# Prompt para que otra inteligencia artificial busque antecedentes (tesis y artículos científicos)

Versión 2 (2026-10-02): sin siglas y con consultas de búsqueda concretas. Uso: copiar el bloque de abajo en la otra herramienta (con búsqueda web) y traer la respuesta a esta carpeta para verificarla. Toda referencia debe comprobarse abriendo el enlace antes de citarla en la memoria: una inteligencia artificial puede inventar referencias.

```text
ROL
Eres un asistente de revisión bibliográfica para un Trabajo de Fin de Máster del Máster en Inteligencia Artificial de la Universidad Internacional de Valencia. Necesito antecedentes REALES y VERIFICABLES. No inventes nada. Si no puedes comprobar que un trabajo existe, no lo incluyas.

MI PROYECTO
Voy a predecir el precio de Bitcoin con una red neuronal espigante propia. Es un reservorio de 1000 neuronas de tipo "integración y disparo con fuga" (en inglés, leaky integrate-and-fire) de DOS compartimentos (dendrita y soma), basada en la neurona TS-LIF presentada en la Conferencia Internacional sobre Representaciones de Aprendizaje de 2025. Los estados del reservorio se leen con un modelo lineal (regresión logística o regresión de cresta). No se entrena toda la red con retropropagación: se ajusta la lectura.

Qué predigo, con datos REALES de Bitcoin:
- la dirección del siguiente retorno (sube o baja) y el movimiento (si el retorno absoluto del siguiente periodo supera un umbral, es decir, una forma de predecir volatilidad);
- en escalas de 1 minuto, 5 minutos, 15 minutos, 1 hora, 2 horas, 4 horas y 1 día;
- con validación cronológica: entrenar con el pasado, evaluar en un bloque final futuro que no se toca hasta el final.

Con qué la comparo, con la misma información y la misma ventana de evaluación:
- referentes simples: persistencia (repetir el último valor), media móvil exponencial del retorno absoluto, y el modelo autorregresivo heterogéneo de volatilidad realizada (en inglés, heterogeneous autoregressive model of realized volatility);
- aprendizaje automático: regresión logística, bosques aleatorios (random forest), refuerzo de gradiente (gradient boosting), perceptrón multicapa, red convolucional temporal y red de memoria a largo y corto plazo (long short-term memory);
- un control no espigante: red de estado de eco (echo state network) con la misma entrada y la misma lectura.
También uso series sintéticas con una señal predecible de tamaño conocido (de 0 % a 100 %) como control positivo y negativo del protocolo.

Resultados preliminares (para que busques trabajos que los confirmen o los contradigan):
- En Bitcoin diario no hay señal de dirección (acierto cercano a 51 %). Hay algo de señal de movimiento (área bajo la curva ROC cercana a 0,56 a 0,58), y una media móvil exponencial del retorno absoluto la capta igual o mejor que mi red.
- A 1 hora, mi red y el refuerzo de gradiente empatan (área bajo la curva ROC 0,703 contra 0,699, con intervalo de confianza del 95 % que incluye cero).
- La intensidad de regularización de la lectura cambia mucho el resultado y las diferencias entre versiones de la red.

QUÉ BUSCAR, EN ESTE ORDEN DE PRIORIDAD

Bloque 1. Tesis doctorales, trabajos de fin de máster y trabajos de fin de grado (primero en español, luego en inglés) sobre:
 a) redes neuronales espigantes aplicadas a series temporales financieras o a criptomonedas;
 b) computación de reservorio (reservoir computing), máquinas de estado líquido (liquid state machines) o redes de estado de eco aplicadas a predicción de Bitcoin, de acciones o de divisas;
 c) comparaciones de aprendizaje automático y aprendizaje profundo para predecir la dirección o la volatilidad de Bitcoin con validación cronológica.
Repositorios donde buscar: Repositorio Institucional de la Universidad de Alicante, O2 de la Universitat Oberta de Catalunya, Tesis Doctorales en Red (TDX), Dialnet, Zenodo, ProQuest, DART-Europe, EThOS, arXiv y SSRN.

Bloque 2. Artículos científicos revisados por pares y preprints (2015 a 2026) sobre:
 a) redes neuronales espigantes para predicción de series temporales, incluyendo el artículo original de la neurona TS-LIF (localiza su título exacto, autores y enlace) y las neuronas de integración y disparo con varios compartimentos o con dendritas;
 b) computación de reservorio y máquinas de estado líquido en predicción financiera y de criptomonedas;
 c) predictibilidad de la dirección y de la volatilidad de Bitcoin según la escala temporal; eficiencia débil del mercado de criptomonedas; efecto del tamaño de la muestra;
 d) metodología: sobreajuste en pruebas retrospectivas de estrategias (backtest overfitting), fuga de información temporal (data leakage), validación progresiva (walk-forward) y validación con purga y embargo, comparación justa contra referentes simples, calibración de probabilidades (puntuación de Brier, curva de fiabilidad), y pruebas estadísticas para comparar modelos con pocas realizaciones independientes (remuestreo por bloques, prueba de Diebold y Mariano, corrección de Holm);
 e) RESULTADOS NEGATIVOS: trabajos que muestren que modelos complejos no superan a referentes simples en criptomonedas o en finanzas.

Bloque 3. Revisiones sistemáticas recientes (2022 a 2026) sobre redes neuronales espigantes en series temporales y sobre aprendizaje automático para predecir criptomonedas.

Cadenas de búsqueda sugeridas (adáptalas, no te limites a ellas):
 - "spiking neural network" AND (Bitcoin OR cryptocurrency) AND (forecasting OR prediction)
 - "reservoir computing" OR "liquid state machine" OR "echo state network" AND (Bitcoin OR "financial time series")
 - "leaky integrate-and-fire" AND "time series forecasting" AND "two-compartment" OR "dendritic"
 - Bitcoin AND "directional predictability" AND (intraday OR "high frequency") AND "out-of-sample"
 - "does not outperform" OR "fails to beat" AND "random walk" AND (Bitcoin OR cryptocurrency) AND "machine learning"
 - "redes neuronales espigantes" AND (predicción OR series temporales) AND (Bitcoin OR criptomonedas OR finanzas)
 - trabajo de fin de máster predicción de Bitcoin aprendizaje automático validación cronológica

Trabajos que YA conozco (no los repitas salvo para ampliar su información): Gao, Luk y Weston (2021) sobre predicción de alta frecuencia con redes neuronales espigantes; Bellec y colaboradores (2020) sobre aprendizaje en redes recurrentes de neuronas espigantes (e-prop); Bacry y Muzy (2015) sobre procesos de Hawkes en finanzas; Wheatley y Sornette (2018) sobre burbujas de Bitcoin.

FORMATO DE RESPUESTA
Una tabla por bloque, con un máximo de 15 entradas por bloque, ordenadas por relevancia. Cada fila debe incluir:
 1. Cita completa: autores, año, título, revista, congreso o repositorio.
 2. Identificador de objeto digital (DOI) o enlace estable. Es obligatorio; si no existe, escribe "SIN DOI NI ENLACE".
 3. Tipo: tesis doctoral, trabajo de fin de máster, artículo, comunicación de congreso, preprint o revisión.
 4. Método principal y datos usados: activo, periodo y frecuencia.
 5. Métrica y resultado principal, con el número exacto que aparece en el texto.
 6. Cómo se evaluó: si usó validación cronológica, si comparó con un referente simple y si aplicó pruebas estadísticas.
 7. Relevancia para mi trabajo, en una frase, y limitación principal, en una frase.
 8. Nivel de verificación: "LEÍDO el texto completo", "LEÍDO solo el resumen" o "NO ABIERTO, solo metadatos".

REGLAS ESTRICTAS
 1. Incluye solo trabajos que hayas localizado en una fuente real y accesible.
 2. No inventes identificadores, páginas, números ni resultados. Si un dato no aparece, escribe "NO ENCONTRADO".
 3. Separa lo que dice el trabajo de lo que opinas tú: marca tus opiniones con "[OPINIÓN]".
 4. No copies texto largo de los trabajos; resume con tus palabras, máximo 2 líneas por entrada.
 5. Al final entrega: (a) los vacíos que no pudiste cubrir; (b) los 5 trabajos más importantes para justificar mi tesis; (c) los 3 trabajos que más contradicen mi enfoque o muestran resultados negativos.
 6. Indica la fecha de tu búsqueda y las consultas exactas que usaste.
```

## Cómo verificar lo que devuelva la otra herramienta

1. Abrir cada identificador o enlace y comprobar autores, año, título y el resultado citado.
2. Descartar cualquier referencia que no se pueda abrir.
3. Registrar las comprobadas en `FUENTES.md` con la fecha de consulta.
4. No citar nada marcado "NO ABIERTO" sin abrirlo personalmente.

# Correo a la profesora (versión de propuesta; lo envías tú)

**Para:** mortega@professor.universidadviu.com
**Asunto:** TFM 09MIAR – propuesta de título y proyecto propio (individual) – Lucas Ivan Tamara Trejo

Buenas tardes profesora Ortega:

Le envío mi propuesta de título y de proyecto propio para el TFM, con los datos que pide el formulario, y le solicito el formato y la estructura que debe seguir una memoria de TFM del máster en Inteligencia Artificial (apartados, extensión, estilo de citas y plantilla, si existe).

**1. Título del proyecto propuesto**
Predicción de la Dirección de Bitcoin utilizando una Red Neuronal Espigante de Segmentos Temporales y Aprendizaje Automático.

**2. Contexto y motivación**
Muchos modelos de aprendizaje automático para predecir Bitcoin pierden su ventaja al compararlos con referentes simples, como el precio anterior, o al usar validación cronológica estricta. Las redes neuronales espigantes son una alternativa ligera, pero se han evaluado poco con ese rigor en criptomonedas. Propongo estudiar si una red de este tipo aporta información real para predecir Bitcoin.

**3. Objetivos**
General: determinar, con un protocolo reproducible, si una red neuronal espigante aporta información predictiva sobre el movimiento y la dirección de Bitcoin más allá de referentes simples y de modelos de aprendizaje automático con la misma información.

Específicos:
1. Evaluar la red con datos de Bitcoin (diarios y de una a dos horas) frente a persistencia, media móvil del movimiento y modelo de volatilidad HAR, reservando un bloque final de prueba.
2. Compararla con regresión logística, bosques aleatorios, gradient boosting, perceptrón multicapa, TCN y LSTM, con las mismas variables y la misma validación, usando AUC, acierto, Brier, calibración y pruebas estadísticas pareadas.
3. Identificar qué componente de la red aporta o no (recurrencia, memoria multiescala, lectura) mediante ablaciones y un control no espigante.

**4. Posibles metodologías de IA**
Red espigante de reservorio con lectura logística o ridge como modelo principal. Controles: red de estado de eco y modelos lineales con retardos. Referentes de aprendizaje automático: regresión logística, bosques aleatorios, gradient boosting, perceptrón multicapa, TCN y LSTM. Evaluación con ventana móvil, bloque final de prueba, bootstrap por bloques y corrección de Holm.

**5. Descripción del dataset**
Serie diaria BTC/USD (2016–2026), velas de Binance de 1 minuto a 1 día obtenidas de su API pública, índice de volatilidad implícita DVOL de Deribit y variables de calendario. Todas las variables se construirían solo con información anterior al instante de predicción. Se respetarán las licencias de cada fuente.

**6. Tutor**
Todavía no he contactado a ningún tutor; agradecería una asignación afín a series temporales con aprendizaje automático o redes neuronales.

**7. Integrantes y justificación de TFM individual**
Integrante único: Lucas Ivan Tamara Trejo. Prefiero realizar el Trabajo de Fin de Máster de forma individual debido a la alta limitación de tiempo derivada de la combinación de mis responsabilidades laborales y el ritmo de estudio del máster. Hacerlo de manera individual me da la autonomía y la flexibilidad necesarias para organizar mis horarios de investigación y desarrollo de código, adaptándome con mayor eficiencia a mi disponibilidad actual sin depender de la coordinación de tiempos con otros compañeros.

Conviene advertir que el resultado puede ser que la red empate con los mejores modelos en lugar de superarlos. Para este caso en particular, eso también sería una conclusión válida y la memoria la trataría así.

Enviaré el formulario dentro del plazo (5 al 8 de octubre). Le agradezco de antemano el formato de la memoria.

Un saludo,
Lucas Ivan Tamara Trejo
[correo institucional]

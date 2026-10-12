# Opción de tesis sobre BTC · pendiente de confirmar

El archivo local `Seleccion_TFM_BTC_y_catalogo_tutores.xlsx` contiene **títulos propuestos para conversar con el tutor**, no una asignación confirmada. Una opción allí formulada es estudiar la dirección de BTC a 24 horas, comparando modelos tabulares y temporales bajo validación cronológica y cambios de régimen. **No des por aprobado este tema** sin confirmación del director y de la universidad.

## Formulación provisional

- **Pregunta:** ¿Mejora un modelo de IA la predicción de la dirección de BTC a 24 horas frente a referencias simples en períodos futuros, y son útiles sus probabilidades?
- **Unidad:** instante o ventana temporal definido antes de preparar datos; una etiqueta por unidad.
- **Datos candidatos:** serie OHLCV de BTC con fuente, frecuencia, zona horaria, cobertura, versión y condiciones de uso documentadas. ETH podría ser prueba secundaria solo si el alcance lo permite.
- **Aporte posible:** comparación transparente y reproducible de un referente ingenuo, un modelo tabular y uno temporal; análisis por regímenes y calidad de probabilidades.
- **Límite:** una mejora predictiva no implica por sí sola rentabilidad o utilidad comercial.

## Protocolo mínimo si se confirma

1. Definir exactamente «subida/bajada a 24 horas»: precio de referencia, horizonte, umbral, tratamiento de retornos cercanos a cero y costes si la pregunta implica una decisión de trading.
2. Congelar el período final fuera de muestra. Usar validación cronológica para el desarrollo; evitar particiones aleatorias. Si las etiquetas o ventanas se solapan, definir una separación temporal suficiente entre entrenamiento y evaluación.
3. Calcular variables únicamente con información disponible **antes** del instante de predicción. Documentar latencia y publicación de cualquier variable externa.
4. Comparar con referentes sencillos definidos previamente. Usar el mismo calendario, horizontes, datos disponibles y reglas de ajuste para todos los modelos.
5. Elegir métrica primaria antes de entrenar. Si se predicen clases: matriz de confusión y métricas por clase. Si se predicen probabilidades: log loss, Brier y curva de calibración, además de discriminación. Brier y log loss no aíslan por sí solos la calibración; interpreta también el gráfico de fiabilidad.
6. Evaluar el rendimiento por tramos temporales y regímenes definidos sin mirar el test final. Reportar estabilidad, incertidumbre y costes de cómputo.
7. Si se afirma utilidad económica, definir una regla de decisión, comisiones, deslizamiento y referencia económica antes de mirar resultados; separar esa pregunta de la calidad predictiva.
8. Guardar predicciones fechadas, parámetros, versiones, semillas y resultados de cada ventana para reproducir tablas y figuras.

La [documentación de `TimeSeriesSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) explica el orden temporal y el parámetro `gap`. La [guía de calibración de scikit-learn](https://scikit-learn.org/stable/modules/calibration.html) describe curvas de fiabilidad, Brier y log loss. El diseño final depende de la frecuencia, el origen de datos y el objetivo acordado con el director.

## Apartados que cambiarían en la memoria

- **Estado del arte:** predicción financiera temporal, aprendizaje tabular/temporal y evaluación fuera de muestra.
- **Marco teórico:** retornos, horizonte, etiquetas, cambio de régimen, probabilidades y calibración.
- **Metodología:** fuente de datos y marcas de tiempo, variables sin información futura, particiones cronológicas, referentes y modelos.
- **Resultados:** rendimiento predictivo general y por período, calibración, errores y costo.
- **Discusión:** estabilidad temporal, riesgo de sobreajuste, límites de generalización y utilidad práctica con cautela.

## Decisiones que requieren tu respuesta

Tema confirmado; director; objetivo (dirección, precio, volatilidad o riesgo); horizonte; fuente de datos; frecuencia; si el trabajo será individual o grupal; y si se pretende evaluar predicción únicamente o también una política de decisión.

# Plan_ES Detallado (52 semanas)

Complemento directo con capitulos y paginas:
- `PLAN_ES_CAPITULOS_Y_PAGINAS.md`

## Configuracion
- Dedicacion: 15 horas/semana.
- Sesiones: 5 dias x 3 horas.
- Entregable fijo semanal:
1. `resumen_semana.md` (2 paginas).
2. `notebook_semana.ipynb` (codigo reproducible).
3. 1 reporte de errores y aprendizajes (`errores_semana.md`).

## Estructura semanal fija
1. Dia 1: lectura teorica (indice + secciones nucleares).
2. Dia 2: derivaciones matematicas a mano.
3. Dia 3: implementacion desde cero.
4. Dia 4: implementacion con framework.
5. Dia 5: evaluacion, reporte y mejoras.

## Semanas 1-6: Matematica base (`capitulo-01`)
- Libros: `mml-book.pdf`, `Hands-On Mathematics for Deep Learning _ Build a Solid.pdf`, `Data Science for Mathematicians.pdf`, `Essential Math for Data Science (Thomas Nield) (Z-Library).pdf`.
- Semana 1: vectores, matrices, norma, producto interno.
- Semana 2: autovalores/autovectores, SVD, proyecciones.
- Semana 3: derivadas parciales, gradiente, jacobiano, hessiano.
- Semana 4: optimizacion convexa basica, descenso de gradiente.
- Semana 5: regla de la cadena aplicada a redes.
- Semana 6: mini-proyecto: regresion lineal/multicapa desde cero (sin framework).

## Semanas 7-11: Estadistica e inferencia (`capitulo-02`)
- Libros: `ESTADISTICA ELEMENTAL 11 Johnson.pdf`, `ESTADISITICA PARA INGENIEROS Y CIENTIFICOS Navidi.pdf`, `Statistical Inference for Engineers and Data Scientists.pdf`, `El arte de la estadística.pdf`.
- Semana 7: distribuciones, muestreo, estadisticos.
- Semana 8: estimacion puntual e intervalos de confianza.
- Semana 9: pruebas de hipotesis, p-value, potencia estadistica.
- Semana 10: regresion estadistica y diagnostico de supuestos.
- Semana 11: mini-proyecto: experimento A/B + reporte inferencial completo.

## Semanas 12-16: Python y datos (`capitulo-03`)
- Libros: `Ciencia-de-los-datos-con-python-1ra-edicion-contenido.pdf`, `Ciencia de datos desde cero.pdf`, `Data Science _ Concepts and Practice.pdf`, `Web Scraping with Python, 2nd Edition.pdf`, `WebScraping_Modulo1_WebScraping.pdf`.
- Semana 12: Python cientifico (NumPy/Pandas).
- Semana 13: limpieza, transformacion y calidad de datos.
- Semana 14: feature engineering y particionado correcto.
- Semana 15: scraping + almacenamiento reproducible.
- Semana 16: mini-proyecto: dataset propio documentado + EDA.

## Semanas 17-23: ML clasico (`capitulo-04`)
- Libros: `Aurelien-Geron-Hands-On-Machine-Learning-with-Scikit-Learn-Keras-and-Tensorflow_-Concepts-Tools-and-Techniques-to-Build-Intelligent-Systems-OReilly-Media-2019.pdf`, `AI and Machine Learning for Coders A Programmers Guide to Artificial Intelligence.pdf`, `Pattern recognition _ concepts, methods, and applications.pdf`, `Machine learning with neural networks _ an introduction.pdf`, `Genetic Algorithms and Machine Learning for Programmers.pdf`, `Mastering Machine Learning From Basics to Advanced.pdf`, `python-machine-learning-machine-learning-and-deep-learning-with-python-scikit-learn-and-tensorflow-2-3nbsped-1789955750-978-1789955750_compress.pdf`.
- Semana 17: pipeline ML y leakage.
- Semana 18: regresion y regularizacion.
- Semana 19: clasificacion, metricas, calibration.
- Semana 20: arboles, ensambles, boosting.
- Semana 21: clustering y reduccion de dimensionalidad.
- Semana 22: busqueda de hiperparametros + validacion robusta.
- Semana 23: mini-proyecto: benchmark de 6 modelos con justificacion estadistica.

## Semanas 24-27: Probabilistico avanzado (`capitulo-05`)
- Libros: `The_MIT_Press_Probabilistic_Machine_Lear.pdf`, `Gradient Expectations.pdf`, `essential-math-for-ai-next-level-mathematics-for-efficient-and-successful-ai-systems-1nbsped-1098107632-9781098107635_compress.pdf`.
- Semana 24: probabilidad multivariada y modelos generativos.
- Semana 25: decision theory, riesgo esperado, entropia.
- Semana 26: inferencia bayesiana y aproximaciones.
- Semana 27: mini-proyecto: clasificador bayesiano + comparacion con discriminativo.

## Semanas 28-34: Deep Learning base (`capitulo-06`)
- Libros: `d2l-en.pdf`, `Deep Learning _ A Comprehensive Guide.pdf`, `Learning Deep Learning _ Theory and Practice of Neural.pdf`, `The Science of Deep Learning.pdf`.
- Semana 28: MLP y backprop completo.
- Semana 29: optimizadores (SGD, Momentum, Adam) e inicializacion.
- Semana 30: regularizacion (dropout, weight decay, batch norm).
- Semana 31: CNN para vision.
- Semana 32: RNN/LSTM/GRU para secuencias.
- Semana 33: atencion basica.
- Semana 34: mini-proyecto: CNN + RNN con experimento controlado.

## Semanas 35-39: Deep Learning teorico (`capitulo-07`)
- Libros: `Deep Learning by Ian Goodfellow, Yoshua Bengio, Aaron Courville (z-lib.org).pdf`, `Neural networks and learning machines .pdf`, `Deep Learning Architectures_ A Mathematical Approach.pdf`, `2407.18384v4.pdf`.
- Semana 35: capacidad, bias-variance y generalizacion.
- Semana 36: superficies de perdida y dinamica de entrenamiento.
- Semana 37: teoria de aproximacion y expresividad.
- Semana 38: estabilidad, sensibilidad y robustez.
- Semana 39: mini-proyecto: estudio de ablacion y curvas de aprendizaje.

## Semanas 40-43: Implementacion experta (`capitulo-08`)
- Libros: `Deep Learning With Pytorch_ Code.pdf`, `programming-with-tensorflow-2021.pdf`, `Applied artificial neural network methods for engineers and.pdf`, `Neural Network Modeling and Identification of Dynamical.pdf`, `Applied Time Series Analysis and Forecasting with Python.pdf`, `time-series-forecasting-in-python-161729988x-9781617299889_compress.pdf`.
- Semana 40: PyTorch profesional (dataloaders, training loops limpios).
- Semana 41: TensorFlow/Keras para produccion.
- Semana 42: modelado de sistemas dinamicos con redes.
- Semana 43: mini-proyecto: mismo modelo en PyTorch y TensorFlow (comparativa).

## Semanas 44-46: Transformers (`capitulo-09`)
- Libros: `Mastering Transformers _ Build State-of-the-art Models From.pdf`, `Building Transformer Models with Attention Implementing a Neural Machine Translator from Scratch in Keras.pdf`, `time-series-forecasting-using-foundation-models_compress.pdf`.
- Semana 44: tokenizacion, embeddings, self-attention.
- Semana 45: fine-tuning y evaluacion en NLP.
- Semana 46: mini-proyecto: transformer fine-tuned + error analysis.

## Semanas 47-48: MLOps (`capitulo-10`)
- Libros: `Mastering MLOps Architecture From Code to Deployment Manage the production cycle of continual learning ML models with MLOps.pdf`, `Advancing Edge Artificial Intelligence System Contexts.pdf`.
- Semana 47: versionado de datos/modelos, pipeline CI/CD.
- Semana 48: despliegue + monitoreo (drift, latencia, retraining).

## Semanas 49-51: Frontera (`capitulo-11`)
- Libros: `Quantum Artificial Intelligence with Qiskit.pdf`, `Quantum Machine Learning A Modern Approach.pdf`, `Neural Engineering_ Computation, Representation.pdf`, `From Neuron to Brain, Fifth Editio.pdf`, `Modeling Life.pdf`, `Machine Learning Theory and Applications Hands-on Use Cases with Python on Classical and Quantum Machines.pdf`.
- Semana 49: introduccion quantum ML y limites reales.
- Semana 50: neuroingenieria y computacion biologica.
- Semana 51: mini-proyecto exploratorio (SNN o QML) con reporte critico.

## Semana 52: Cierre experto (`capitulo-12` + integracion)
- Libros: `Big Data, Big Design Why Designers Should Care about Artificial Intelligence.pdf`, `Learn AI-assisted Python Programming With GitHub Copilot and ChatGPT.pdf`, `Artificial Intelligence in Forecasting Tools and Techniques.pdf`.
- Entregable final:
1. Proyecto maestro end-to-end (datos -> entrenamiento -> despliegue).
2. Paper tecnico corto (6-10 paginas) con metodologia y resultados.
3. Defensa oral de 30 minutos (slides + demo).

## Super indice final que debes dominar
1. Algebra lineal y calculo para redes.
2. Probabilidad, inferencia y estadistica experimental.
3. Data engineering para ML.
4. ML clasico y seleccion de modelos.
5. Fundamentos de redes neuronales.
6. Optimizacion profunda y regularizacion.
7. CNN, RNN, seq2seq y atencion.
8. Transformers y fine-tuning.
9. Teoria de generalizacion y analisis de entrenamiento.
10. Implementacion experta en PyTorch y TensorFlow.
11. MLOps, monitoreo y despliegue.
12. SNN/Quantum/Neuro para frontera de investigacion.

## Criterios de aprobacion por fase
- Fase 1 (sem 1-16): puedes derivar gradientes y construir pipelines de datos limpios.
- Fase 2 (sem 17-34): puedes entrenar, comparar y justificar modelos ML/DL.
- Fase 3 (sem 35-48): puedes explicar teoria avanzada y desplegar modelos en produccion.
- Fase 4 (sem 49-52): puedes leer papers frontera y producir un proyecto publicable.

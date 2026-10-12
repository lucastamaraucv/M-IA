# Self-Supervised Learning for Medical Image Classification: A Systematic Review and Implementation Guidelines

- **Autores:** Shih-Cheng Huang, Anuj Pareek, Malte Jensen, Matthew P. Lungren, Serena Yeung, Akshay S. Chaudhari (Stanford University)
- **Publicación:** *npj Digital Medicine* 6:74 (2023). DOI: 10.1038/s41746-023-00811-0 (acceso abierto, CC-BY 4.0)
- **Tipo:** **Revisión sistemática** (PRISMA), no propone un método nuevo
- **¿Corresponde al curso de Aprendizaje No Supervisado?** **Sí, como revisión.** El aprendizaje auto-supervisado (SSL) es aprendizaje de representaciones **a partir de datos sin etiquetas**. Ojo: para la tarea del portafolio (explicar el *método propuesto* y sus mejoras), una revisión encaja peor que un artículo con un método propio.

---

## 1. Motivación
- El uso de imagen médica crece y un radiólogo debe interpretar **una imagen cada 3–4 segundos**, lo que lleva a retrasos y errores.
- El deep learning alcanza nivel experto en tareas concretas (rayos X, TC, RM, WSI y dermatología), pero depende del **aprendizaje supervisado con muchas etiquetas**, que son caras porque requieren expertos.
- Los modelos supervisados **generalizan mal** a otras instituciones o tareas: son "especialistas".
- El **SSL** crea modelos "**generalistas**" a partir de datos sin etiquetar que luego se ajustan con pocas etiquetas. Triunfó en PLN (BERT, GPT-3) y después en visión (SimCLR superó al supervisado en ImageNet con **100 veces menos etiquetas**).

## 2. Taxonomía de estrategias SSL (aporte conceptual)
| Categoría | Qué hace | Ejemplos | Pérdida |
|---|---|---|---|
| **Relación innata** (*innate relationship*) | Tarea pretexto diseñada a mano con la estructura interna de los datos | Predecir la rotación, jigsaw, posición relativa de parches | Clasificación o regresión. Riesgo: rasgos útiles solo para la tarea pretexto |
| **Generativa** | Aprender la distribución de los datos y reconstruir la entrada **completa** o generar datos | Autoencoders, VAE, GAN (BigBiGAN) | Reconstrucción |
| **Contrastiva** | Las aumentaciones de la misma imagen forman un **par positivo** y se acercan en el espacio latente; las negativas se alejan | **SimCLR** (requiere lotes grandes), **MoCo** (cola con momentum), sin negativos: **BYOL, SimSiam, DINO**; por clustering: **SwAV, SeLa** | Contrastiva (InfoNCE, etc.) |
| **Auto-predicción** (*self-prediction*) | Enmascarar o alterar **parte** de la entrada y reconstruirla con el resto | Context encoders (inpainting), **BEiT, MAE** (con ViT), *local pixel shuffling* | Reconstrucción |

- Diferencia entre generativa y auto-predicción: la auto-predicción altera **solo una parte** y usa el resto sin alterar para reconstruir; la generativa transforma y reconstruye **toda** la imagen.
- **Ajuste fino (stage 2):** (e) **end-to-end** (se descongelan encoder y clasificador) o (f) **extracción de rasgos** con el encoder congelado más un clasificador (*linear probing*, SVM, kNN).

## 3. Metodología de la revisión
- PRISMA; bases de datos **PubMed, Scopus y ArXiv**; enero de 2012 a mayo de 2021.
- **412 estudios** identificados → 77 duplicados eliminados → 335 cribados → 148 a texto completo → **79 incluidos**.
- Criterios: inglés, revisión por pares, SSL más una tarea **de clasificación clínicamente relevante**. Se excluyen los semi-supervisados, los que solo hacen segmentación o regresión y los veterinarios.
- Se extrajeron estrategia, modalidad, dominio, framework, tipo de ajuste, métrica y rendimiento frente a la versión supervisada (prioridad de métricas: AUROC > accuracy > F1 > sensibilidad).

## 4. Resultados
| Estrategia | Nº de estudios | Hallazgos |
|---|---|---|
| **Contrastiva** | **44** | SimCLR (13), MoCo (8), BYOL (3). Pares positivos con conocimiento médico (parches vecinos en patología, rayos X con su informe radiológico, rasgos radiómicos y profundos, metadatos del paciente). Mejora media del **6.35 %** frente al supervisado (36 estudios) |
| **Relación innata** | 15 | Rotación, volteo, orden de cortes y de parches; tareas clínicas como la **mirada del ecografista** o la consistencia temporal del ciclo cardiaco. Las tareas pretexto **clínicas mejoran más** que las basadas en transformaciones (**13.7 % frente a 5.03 %**) |
| **Combinadas** | 11 | Casi siempre contrastiva más generativa (autoencoder). Todas las que compararon con el supervisado mejoraron (0.14–8.29 %) |
| **Auto-predicción** | 6 | *Local pixel shuffling*, restauración, masked autoencoder sobre conectividad de fMRI. Mejoras pequeñas (0.69 % y 1.12 %) |
| **Generativa** | 3 | Pies de figura de libros de histopatología, fMRI (activo/pasivo), edad cerebral. Mejoras del 16.6 % y 24.5 % |

- **Dominios:** radiología con 47 de 79 estudios (27 de imagen torácica: neumonía, COVID-19, derrame pleural, embolia pulmonar; gracias a datasets públicos como CheXpert y MIMIC-CXR) y patología con 12 (WSI, cáncer colorrectal); también psiquiatría con fMRI.
- **Global:** el SSL mejora frente al mismo modelo sin SSL entre un 0.216 y un 32.6 % en AUROC, entre 0.44 y 29.2 % en accuracy y entre 0.137 y 14.3 % en F1; solo 5 estudios empeoraron (0.98–4.51 %).
- Las estrategias **combinadas tienden a rendir más** (posible sesgo de publicación).
- El ajuste **end-to-end supera a la extracción de rasgos** en 8 de 11 comparaciones.

## 5. Debilidades de la literatura revisada
- Solo 33 de 79 estudios comparan con otra estrategia SSL; 60 comparan con el supervisado.
- Solo 18 usan pesos pre-entrenados en imágenes naturales como punto de partida.
- Solo 13 comparan end-to-end con extracción de rasgos.
- Faltan **ablaciones** y pruebas en varios datasets y modalidades.

## 6. Guías de implementación (recomendaciones)
1. **Comparar varias estrategias SSL**: la óptima depende del dominio, el tamaño del dataset y la tarea.
2. **Reutilizar modelos pre-entrenados** (SSL o supervisados como BiT) en imágenes naturales y **continuar el SSL en el dominio médico** (Azizi et al.), que da los mejores resultados.
3. Combinar representaciones de varios métodos SSL (Truong et al.).
4. Preferir el ajuste **end-to-end**. MoCo es más linealmente separable (*linear probing*) y MAE rinde más al ajustar más capas.
5. El SSL necesita **muchos datos sin etiquetar**: pasar de 250 000 a 50 000 imágenes reduce la accuracy en más de un 10 %, y de 1 M a 250 000, entre un 2 y un 4 %. Solución: **aprendizaje federado** (Yan et al.).
6. **Cuidado con las aumentaciones:** en imagen médica, recortar o enmascarar puede **eliminar la lesión** y cambiar el significado (ejemplo: un cavernoma en RM frente a un perro en una foto). Se proponen **máscaras aprendidas o semánticas y recortes con restricción espacial**.
7. **Aprovechar la estructura médica**: pares positivos del mismo paciente, estudio o serie de TC, o de pacientes de edad similar; tareas pretexto como el intervalo temporal entre OCT; **multimodalidad** (imagen y genética, ecografía y voz, imagen e informe radiológico). Por ejemplo, GLoRIA permite localización y *zero-shot*.

## 7. Limitaciones de la revisión
Sesgo de publicación, imposibilidad de un metanálisis (métricas, tareas y modalidades heterogéneas), subjetividad al categorizar, solo clasificación (sin segmentación ni registro) y periodo posterior a 2012.

## 8. Conceptos clave
Tarea pretexto, tarea final (*downstream*), par positivo/negativo, InfoNCE, SimCLR/MoCo/BYOL/SimSiam/DINO/SwAV, MAE/BEiT, linear probing frente a end-to-end, PRISMA, transferencia natural→médica, aprendizaje federado.

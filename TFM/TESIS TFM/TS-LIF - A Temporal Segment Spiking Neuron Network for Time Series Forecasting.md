# TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting

> **Ficha de conocimiento completa del artículo** (extraída el 2026-10-05 de `bt/SNN/677_TS_LIF_A_Temporal_Segment_.pdf`, 21 páginas, leído íntegro). Redactada en español: paráfrasis, ecuaciones y datos de las tablas, sin copiar el texto original. Al final se analiza el artículo y se relaciona con la tesis (E20-A0C).

---

## 1. Datos bibliográficos

| Campo | Valor |
|---|---|
| Título | TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting |
| Autores | Shibo Feng\*, Wanjin Feng\*, Xingyu Gao, Peilin Zhao†, Zhiqi Shen† (\* contribución igual; † autores de correspondencia) |
| Instituciones | Nanyang Technological University; University of Chinese Academy of Sciences; Tencent AI Lab; Webank-NTU Joint Research Institute on Fintech (Singapur) |
| Publicación | Conference paper, **ICLR 2025** (con revisión por pares) |
| Código | https://github.com/kkking-kk/TS-LIF |
| Financiación | Joint NTU-WeBank Research Centre on Fintech |
| Cita sugerida | Feng, S., Feng, W., Gao, X., Zhao, P. y Shen, Z. (2025). *TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting*. ICLR 2025. |

**Traducción del título usada en la tesis:** «Red Neuronal Espigante de Segmentos Temporales».

---

## 2. Idea central en una frase

Proponen una neurona espigante de **dos compartimentos** (dendrita y soma). La dendrita se especializa en **frecuencias bajas** (tendencias) y el soma en **frecuencias altas** (cambios rápidos). Dos añadidos lo hacen posible: una **inyección directa de corriente al soma** y la capacidad de que la **dendrita también emita espigas**. Así mejoran el pronóstico de series temporales frente a las redes espigantes con neuronas LIF clásicas.

---

## 3. Problema que atacan (Introducción)

- Las **redes neuronales espigantes (SNN)** comunican con espigas discretas, procesan solo cuando hay eventos y son **eficientes en energía** en hardware neuromórfico.
- El pronóstico de series temporales encaja con ellas por su naturaleza secuencial. Citan como aplicaciones: **finanzas**, meteorología, salud y energía.
- Los modelos profundos (TCN, Transformer) capturan dependencias largas, pero son costosos en cómputo.
- Antecedente directo: **Lv et al. (2024, ICML)** mostró que las SNN son competitivas en pronóstico. Su marco experimental es el que reutiliza este artículo.
- Limitación de la neurona **LIF** clásica:
  1. Su potencial decae rápido, por lo que **olvida** y no captura dependencias largas.
  2. **No separa escalas temporales**: no distingue fluctuaciones cortas de tendencias largas.

### Contribuciones declaradas
1. La neurona **TS-LIF**, de dos compartimentos y multiescala.
2. **Condiciones de estabilidad** y **funciones de transferencia en frecuencia** de cada compartimento.
3. Validación en **4 conjuntos** de datos con arquitecturas **CNN (TCN), RNN (GRU) y Transformer**, incluida la robustez ante datos faltantes.

---

## 4. Trabajo relacionado

### 4.1 Dependencias largas en SNN
| Modelo | Idea |
|---|---|
| **GLIF** (Yao et al., 2022) | Compuertas que regulan el flujo temporal |
| Conexiones autápticas (Wang & Yu, 2024) | Mejoran la memoria larga |
| **TC-LIF** (Zhang et al., 2024, AAAI) | Dos compartimentos que reparten la memoria y mejoran la propagación del gradiente |
| **LM-H** (Hao et al., 2024, ICLR) | Parámetros aprendibles que equilibran historia e información actual |
| Heterogeneidad dendrítica temporal (Zheng et al., 2024, Nature Communications) | Neuronas multicompartimento con escalas distintas |

**Hueco que identifican:** ninguno **descompone e integra** explícitamente las escalas temporales de una misma señal.

### 4.2 Pronóstico de series temporales
- **RNN** (LSTM, GRU): les cuestan las dependencias largas y son ineficientes en datos grandes.
- **TCN**: convoluciones dilatadas, paralelizables.
- **Transformers** (Informer, Autoformer, iTransformer): atención para dependencias largas; consumen mucha energía.

---

## 5. Preliminares

### 5.1 Planteamiento del problema
Serie multivariante $X=\{x_1,\dots,x_T\}\in\mathbb{R}^{T\times C}$ ($T$ pasos, $C$ variables). Se aprende $f$ que predice $Y=\{x_{T+1},\dots,x_{T+L}\}\in\mathbb{R}^{L\times C}$, es decir, **regresión multi-paso**. La descomposición en escalas (variaciones cortas y tendencias largas) ayuda a capturar la estructura.

### 5.2 Neurona LIF (ecuaciones 1–3)
$$v[t]=\alpha\,v[t-1]+c[t]-v_{th}\,s[t-1],\qquad s[t]=H(v[t]-v_{th})$$
- $\alpha<1$: decaimiento; $c[t]$: corriente; $H$: función escalón de Heaviside; reinicio restando el umbral.
- Desarrollada desde $v[0]=0$:
$$v[t+1]=\sum_{k=1}^{t+1}\alpha^{t-k+1}c[k]-v_{th}\sum_{k=1}^{t}\alpha^{t-k}s[k]$$
- Interpretación: es una **suma ponderada con decaimiento exponencial**, que actúa como **filtro paso bajo** de ventana corta y por eso olvida pronto.

### 5.3 Modelo general de dos compartimentos (ecuación 4; base de TC-LIF y LM-H)
$$v_d[t]=\alpha_1 v_d[t-1]+\beta_1 v_s[t-1]+c[t]$$
$$v_s[t]=\alpha_2 v_s[t-1]+\beta_2 v_d[t]-v_{th}\,s_s[t-1],\qquad s_s[t]=H(v_s[t]-v_{th})$$
- $\alpha_1,\alpha_2$: decaimientos; $\beta_1,\beta_2$: interacción entre compartimentos.
- Críticas del artículo a este modelo:
  1. La corriente **solo entra por la dendrita**, así que el soma pierde las altas frecuencias.
  2. No hay **especialización clara** por frecuencia.
  3. Falta **validación teórica** de la estabilidad.

---

## 6. Metodología: la neurona TS-LIF

### 6.1 Ecuaciones (ecuación 5)
$$v_d[t]=\alpha_1 v_d[t-1]+\beta_1 v_s[t-1]+(1-\alpha_1)c[t]-\gamma_1 s_d[t-1]$$
$$v_s[t]=\alpha_2 v_s[t-1]+\beta_2 v_d[t]+(1-\alpha_2)c[t]-\gamma_2 s_s[t-1]$$
$$s_d[t]=H(v_d[t]-v_{th}),\qquad s_s[t]=H(v_s[t]-v_{th})$$

**Novedades frente al modelo general:**

| Elemento | Qué hace | Justificación biológica que dan |
|---|---|---|
| $(1-\alpha_2)c[t]$ | **Atajo**: corriente directa al soma | Sinapsis axosomáticas, sinapsis eléctricas (*gap junctions*), ramas dendríticas que actúan como identidad (Hawkins & Ahmad, 2016) |
| $(1-\alpha_1)c[t]$ | Entrada normalizada a la dendrita | Con $\alpha_1\to1$, $v_d$ se comporta como una **media móvil** (paso bajo) |
| $s_d[t]$ | **Espigas dendríticas** | Neuronas piramidales del hipocampo y la corteza; neuronas multicompartimento y HTM |
| $\gamma_1,\gamma_2$ | **Reinicio adaptativo** (no fijo) | Más flexibilidad en la respuesta |

- **Intuición:** con $\alpha_1$ cerca de 1, la dendrita retiene tendencias. Con $\alpha_2$ cerca de 0, el soma sigue los cambios rápidos de $c[t]$.
- **Umbral:** $v_{th}=1{,}0$ (apéndice A.3).

### 6.2 Mezcla de salidas (ecuación 6)
$$s_{mix}[t]=\kappa\,s_d[t]+(1-\kappa)\,s_s[t]$$
- $\kappa$ equilibra la contribución de la dendrita (baja frecuencia) y del soma (alta frecuencia), y puede variar por canal.
- **Todos los coeficientes $(\alpha,\beta,\gamma,\kappa)$ son aprendibles.**

### 6.3 Análisis de estabilidad (Teorema 1)
Parte homogénea, es decir, sin entrada ni espigas (ecuación 7):
$$v_d[t]=\alpha_1 v_d[t-1]+\beta_1 v_s[t-1],\qquad v_s[t]=\alpha_2 v_s[t-1]+\beta_2 v_d[t]$$
En forma matricial, $v[t]=A\,v[t-1]$ con
$$A=\begin{pmatrix}\alpha_1 & \beta_1\\ \alpha_1\beta_2 & \alpha_2+\beta_1\beta_2\end{pmatrix}$$
La ecuación característica es $\lambda^2-(\alpha_1+\alpha_2+\beta_1\beta_2)\lambda+\alpha_1\alpha_2=0$, y sus autovalores son
$$\lambda=\frac{(\alpha_1+\alpha_2+\beta_1\beta_2)\pm\sqrt{(\alpha_1+\alpha_2+\beta_1\beta_2)^2-4\alpha_1\alpha_2}}{2}$$
- **El sistema es estable si y solo si $|\lambda|<1$ para ambos autovalores.**
- El artículo añade que esto exige $\alpha_1+\alpha_2+\beta_1\beta_2<2$. *(Nota crítica: es una condición necesaria, no suficiente.)*
- Esto explica por qué TC-LIF, con $\alpha_1=\alpha_2=1$, necesita $\beta_1\beta_2\le 0$.

### 6.4 Respuesta en frecuencia (transformada Z, ecuaciones 14–18)
Sin espigas ni reinicio:
$$H_d(z)=\frac{(1-\alpha_1)(1-\alpha_2 z^{-1})+\beta_1 z^{-1}(1-\alpha_2)}{\det M},\qquad H_s(z)=\frac{\beta_2(1-\alpha_1)+(1-\alpha_1 z^{-1})(1-\alpha_2)}{\det M}$$
$$\det M=1-(\alpha_1+\alpha_2+\beta_1\beta_2)z^{-1}+\alpha_1\alpha_2 z^{-2}$$
El módulo da la **ganancia** por frecuencia y la fase da el **retardo**.

### 6.5 Ejemplo numérico (sección 4.4) — **verificado por nosotros con Python**
Parámetros: $\alpha_1=0{,}95$ (dendrita paso bajo), $\alpha_2=0{,}05$ (soma paso alto), $\beta_1=0$, $\beta_2=-0{,}9$.
- Autovalores: **0,95 y 0,05**, ambos estables ✔.
- $H_d(z)=\dfrac{0{,}05-0{,}0025z^{-1}}{1-z^{-1}+0{,}0475z^{-2}}$, $\quad H_s(z)=\dfrac{0{,}905-0{,}9025z^{-1}}{1-z^{-1}+0{,}0475z^{-2}}$

| Frecuencia | $\lvert H_d\rvert$ | $\lvert H_s\rvert$ |
|---|---|---|
| $\omega=0$ (baja) | **1,000** | 0,0526 |
| $\omega=\pi$ (alta) | 0,0256 (*no lo da el artículo; calculado*) | **0,8828** |

**Conclusión:** la dendrita deja pasar lo lento y el soma lo rápido, es decir, **separan frecuencias**.

---

## 7. Experimentos

### 7.1 Análisis temporal (sección 5.1 + apéndice A.4)
- **Entrada:** suma de dos senos, uno de **0,5 Hz con amplitud 3** y otro de **4 Hz con amplitud 5**.
- **TC-LIF** con $\alpha_1=\alpha_2=1$, $\beta_1=-0{,}5$, $\beta_2=0{,}5$: los dos compartimentos mezclan las frecuencias.
- **TS-LIF** con los parámetros del ejemplo anterior: **la dendrita retiene la baja frecuencia y el soma la alta** (Figura 4).
- *Ojo:* son parámetros elegidos a mano, no aprendidos.

### 7.2 Conjuntos de datos (apéndice A.2, Tabla 3)
| Conjunto | Variables | Dominio | Frecuencia | Muestras | Historia | Horizonte | Partición entr./val./prueba |
|---|---|---|---|---|---|---|---|
| Metr-la (tráfico, Los Ángeles) | 207 | R+ | 30 min | 34 272 | {12, 168} | {6, 24, 48, 96} | 0,7 / 0,2 / 0,1 |
| Pems-bay (tráfico, Bahía de San Francisco) | 325 | R+ | 30 min | 52 116 | {12, 168} | {6, 24, 48, 96} | 0,7 / 0,2 / 0,1 |
| Solar (producción solar) | 137 | R+ | 1 h | 52 560 | 168 | {6, 24, 48, 96} | 0,6 / 0,2 / 0,2 |
| Electricity (consumo kWh) | 321 | R+ | 1 h | 26 304 | 168 | {6, 24, 48, 96} | 0,6 / 0,2 / 0,2 |

### 7.3 Métricas (ecuación 22)
- **RSE** (error cuadrático relativo, raíz; menor es mejor):
$$RSE=\sqrt{\frac{\sum_m\lVert Y_m-\hat Y_m\rVert^2}{\sum_m\lVert Y_m-\bar Y\rVert^2}}$$
- **R²** (mayor es mejor), promediado sobre muestras $M$, canales $C$ y horizonte $L$:
$$R^2=\frac{1}{MCL}\sum_{m,c,l}\left[1-\frac{(Y^m_{c,l}-\hat Y^m_{c,l})^2}{(Y^m_{c,l}-\bar Y_{c,l})^2}\right]$$

### 7.4 Implementación (A.1, A.3, A.12; Tablas 4 y 5)
- Marco de **Lv et al. (2024)**: versiones espigantes de TCN, GRU y Transformer (iTransformer). **TS-former** es el iTransformer con TS-LIF.
- **Codificador de espigas** (A.12): cada paso de la serie $\Delta T$ se divide en $T_s$ sub-pasos de la SNN ($\Delta T=T_s\Delta t$). Las espigas se generan con $S=\mathrm{SNN}(\mathrm{BN}(\mathrm{Conv}(X)))$; la convolución expande a $T_s\times T\times C$ eventos posibles. Se prefiere esto a replicar cada valor $T_s$ veces, que rompería la continuidad.
- Los pasos de la SNN se alinean con la longitud de la historia.
- Hiperparámetros (tasa de aprendizaje, intervalos, pesos de mezcla) **ajustados por validación cruzada**.

| Conjunto | Capas TCN | Kernel TCN | Capas GRU | Capas Transformer | Cabezas | Dim. atención | Oculto TCN | Dilatación | Oculto GRU | d_ff | Tasa de aprendizaje | Lote |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Metr-la | 3 | 3 | 1 | 2 | 8 | 256 | 64 | 2 | 128 | 1024 | {1e-4, 5e-4} | {32, 64} |
| Pems-bay | 3 | 16 | 1 | 2 | 8 | 512 | 64 | 2 | 128 | 2048 | {1e-4, 5e-4} | {32, 64} |
| Solar | 3 | 16 | 1 | 2 | 8 | 512 | 64 | 2 | 128 | 2048 | 1e-4 | 64 |
| Electricity | 3 | 3 | 1 | 2 | 8 | 256 | 64 | 2 | 128 | 1024 | 1e-4 | 64 |

### 7.5 Resultados principales (Tabla 1) — medias y rango medio
Los resultados de los rivales **se copian de Lv et al. (2024)**; solo los modelos TS-\* se ejecutaron en este trabajo.

| Modelo | ¿Espigante? | R² medio ↑ | Rango medio R² ↓ | RSE medio ↓ | Rango medio RSE ↓ |
|---|---|---|---|---|---|
| ARIMA | No | .713 | 9.9 | .583 | 9.8 |
| GP | No | .705 | 11.1 | .605 | 10.2 |
| TCN | No | .770 | 5.8 | .483 | 5.7 |
| Spike-TCN | Sí | .750 | 7.0 | .518 | 8.9 |
| **TS-TCN** | Sí | **.777** | 5.0 | **.475** | 4.6 |
| GRU | No | .733 | 8.0 | .573 | 9.5 |
| Spike-GRU | Sí | .759 | 8.8 | .517 | 8.8 |
| Spike-RNN | Sí | .768 | 7.4 | .503 | 7.1 |
| **TS-GRU** | Sí | **.778** | 4.8 | **.460** | 4.8 |
| Autoformer | No | .753 | 7.2 | .569 | 9.1 |
| iTransformer | No | .776 | 4.4 | .480 | 4.7 |
| iSpikformer | Sí | .775 | 5.2 | .476 | 4.6 |
| **TS-former** | Sí | **.783** | **3.5** | **.441** | **3.3** |

**R² por conjunto y horizonte (6 / 24 / 48 / 96) de los modelos clave:**

| Modelo | Metr-la | Pems-bay | Solar | Electricity |
|---|---|---|---|---|
| TCN | .820 / .601 / .455 / .330 | .881 / .749 / .695 / .689 | .958 / .871 / .737 / .661 | .975 / .973 / .968 / .962 |
| TS-TCN | .810 / .605 / .473 / .328 | .897 / .759 / .698 / .652 | .964 / .884 / .762 / .720 | .980 / .971 / .968 / .962 |
| GRU | .759 / .429 / .301 / .194 | .747 / .703 / .691 / .665 | .950 / .875 / .781 / .737 | .981 / .972 / .971 / .964 |
| TS-GRU | .848 / .618 / .430 / .329 | .874 / .742 / .684 / .649 | .938 / .878 / .815 / .722 | .991 / .981 / .983 / .976 |
| iTransformer | .829 / .623 / .439 / .285 | .887 / .719 / .685 / .668 | .964 / .879 / .799 / .738 | .979 / .977 / .975 / .964 |
| TS-former | .847 / .620 / .445 / .283 | .874 / .735 / .683 / .669 | .961 / .886 / .828 / .774 | .987 / .985 / .981 / .977 |

**Afirmaciones del artículo:**
- En Solar, TS-TCN y TS-former mejoran de media un **8 % en R²** y un **16,8 % en RSE**.
- En Electricity a 96 pasos, la RSE mejora un **43,6 %** (TS-GRU) y un **25,0 %** (TS-former).
- La ventaja es mayor en **horizontes largos**.

### 7.6 Robustez ante datos faltantes (Tablas 2 y 9)
Se borran del 10 % al 80 % de los valores de la historia. Comparación: TS-LIF frente a LIF simple en la misma arquitectura.

**Electricity (Tabla 2), R² con 10 % → 80 % faltante:**
| Arquitectura | LIF simple | TS-LIF |
|---|---|---|
| Transformer, horizonte 6 | 0.977 → 0.964 | 0.987 → 0.983 |
| Transformer, horizonte 96 | 0.962 → 0.947 | 0.977 → 0.971 |
| GRU, horizonte 6 | 0.873 → 0.745 | 0.986 → 0.939 |
| GRU, horizonte 96 | 0.842 → 0.760 | 0.975 → 0.922 |
| TCN, horizonte 6 | 0.971 → 0.954 | 0.980 → 0.967 |
| TCN, horizonte 96 | 0.953 → 0.937 | 0.962 → 0.952 |

**Metr-la (Tabla 9), R² con 10 % → 80 % faltante:**
| Arquitectura | LIF simple | TS-LIF |
|---|---|---|
| Transformer, horizonte 6 | 0.815 → 0.802 | 0.843 → 0.831 |
| Transformer, horizonte 96 | 0.270 → 0.194 | 0.277 → 0.205 |
| GRU, horizonte 6 | 0.830 → 0.743 | 0.843 → 0.792 |
| GRU, horizonte 96 | 0.243 → 0.171 | 0.342 → 0.294 |
| TCN, horizonte 6 | 0.774 → 0.731 | 0.792 → 0.744 |
| TCN, horizonte 96 | 0.315 → 0.202 | 0.323 → 0.228 |

- El mayor beneficio aparece con **GRU**: aproximadamente **+20 % en R²** y **−50 % en RSE** en Electricity. Lo explican porque la GRU tiene peor memoria larga.

### 7.7 Longitud de historia de entrenamiento (Figura 5)
- Historias de 24, 96 y 168 pasos (Solar a 24 pasos; Electricity a 96).
- El rendimiento **mejora al alargar la historia**, sobre todo de 24 a 96.
- Media y desviación típica sobre **3 semillas**.

### 7.8 TS-LIF frente a otras neuronas
**Figura 6 (horizonte 24, valores de las barras):**
| Conjunto / métrica | GRU: TC-LIF / TS-LIF | TCN: TC-LIF / TS-LIF | iTransformer: TC-LIF / TS-LIF |
|---|---|---|---|
| Solar R² | 0.833 / 0.852 | 0.881 / 0.878 | 0.884 / 0.886 |
| Solar RSE | 0.412 / 0.364 | 0.336 / 0.349 | 0.325 / 0.331 |
| Electricity R² | 0.976 / 0.965 | 0.980 / 0.981 | 0.971 / 0.985 |
| Electricity RSE | 0.257 / 0.328 | 0.224 / 0.240 | 0.316 / 0.215 |

*(Asignación de las barras según el orden de la leyenda TC-LIF → TS-LIF. Varias barras favorecen a TC-LIF aunque el texto dice que TS-LIF gana «en todos los casos». Conviene verificarlo en la figura original.)*

**Tabla 8 (solo GRU), R² / RSE:**
| Neurona | Metr-la 6 | Metr-la 24 | Metr-la 96 | Elec. 6 | Elec. 24 | Elec. 96 |
|---|---|---|---|---|---|---|
| TC-LIF | .828 / .453 | .594 / .673 | .259 / .956 | .978 / .263 | .976 / .257 | .941 / .503 |
| LM-H | .812 / .464 | .570 / .719 | .246 / .973 | .971 / .269 | .969 / .280 | .936 / .512 |
| CLIF | .837 / .429 | .606 / .667 | .271 / .930 | .973 / .259 | .972 / .276 | .954 / .376 |
| **TS-LIF** | **.848 / .412** | **.618 / .651** | **.329 / .853** | **.991 / .216** | **.981 / .240** | **.976 / .271** |

### 7.9 Comparación con métodos punteros (A.6, Tabla 7), R² / RSE
| Modelo | Metr-la 24 | Metr-la 48 | Metr-la 96 | Elec. 24 | Elec. 48 | Elec. 96 |
|---|---|---|---|---|---|---|
| SparseTSF | .576 / .681 | .427 / .792 | .253 / .916 | **.991 / .167** | **.986 / .195** | **.982 / .232** |
| SparseTSF\* (ReLU → TS-LIF) | .580 / .692 | .426 / .801 | .247 / .924 | .990 / .177 | .985 / .201 | .982 / .234 |
| SAMformer | .549 / .739 | .401 / .863 | .219 / .965 | .983 / .218 | .980 / .239 | .978 / .257 |
| **TS-former** | **.620 / .655** | **.445 / .763** | **.283 / .874** | .985 / .215 | .981 / .234 | .977 / .261 |

- TS-former gana en Metr-la, pero **SparseTSF gana en Electricity**, cosa que el propio artículo admite.

### 7.10 Energía y tiempo (A.5, Tabla 6; Electricity, inferencia por muestra)
**Fórmulas:**
- Red espigante: $E=E_{AC}\times SOPs$, con $SOPs=T\times\gamma\times FLOPs$.
- Red artificial: $E=E_{MAC}\times FLOPs$.
- Constantes para hardware de 45 nm: $E_{MAC}=4{,}6$ pJ y $E_{AC}=0{,}9$ pJ.

| Modelo | Parámetros (M) | Operaciones (G) | Energía (mJ) | Reducción | Entrenamiento / inferencia (s) | R² |
|---|---|---|---|---|---|---|
| TCN | 0.460 | 0.14 | 0.64 | — | 21.34 / 11.47 | .973 |
| Spike-TCN | 0.461 | 0.15 | 0.23 | 63.60 % | 306.91 / 27.85 | .963 |
| TS-TCN | 0.465 | 0.19 | 0.25 | 60.93 % | 308.26 / 28.14 | .971 |
| GRU | 1.288 | 1.32 | 6.07 | — | 37.73 / 7.35 | .972 |
| Spike-GRU | 1.289 | 1.63 | 1.51 | 75.05 % | 235.46 / 10.05 | .964 |
| TS-GRU | 1.291 | 1.67 | 1.58 | 73.80 % | 246.23 / 9.78 | .981 |
| iTransformer | 1.634 | 2.05 | 9.47 | — | 7.24 / 6.38 | .977 |
| iSpikformer | 1.634 | 3.55 | 3.19 | 66.30 % | 49.84 / 8.69 | .974 |
| TS-former | 1.640 | 3.59 | 3.22 | 65.99 % | 50.36 / 8.72 | .985 |

- TS-LIF añade muy pocos parámetros y reduce la energía teórica de inferencia entre un **61 % y un 74 %**.
- A cambio, **entrena entre 7 y 15 veces más lento** que la red artificial equivalente.

### 7.11 Variabilidad entre semillas (A.9, Tabla 10)
- 3 semillas para TS-GRU y TS-former en Metr-la y Electricity (horizontes 6–96).
- Desviación típica de **R² entre 0,001 y 0,005** y de **RSE entre 0,002 y 0,013**. Concluyen que el modelo es estable.

### 7.12 Espectro de potencia (A.10, Figura 7)
- Espectro medio de los voltajes de dendrita y soma tras la primera capa del codificador de TS-former **ya entrenado**.
- Muestran perfiles de frecuencia distintos: la especialización también aparece con parámetros aprendidos.

### 7.13 Memoria larga: XOR retardado (A.11, Tabla 11)
- **Tarea:** espiga inicial, retardo con espigas de ruido, espiga final; la salida es el XOR entre la primera y la última, según sus tasas de disparo.
- **Montaje:** el de Zheng et al. (2024), una MLP de 2 capas con 20 neuronas ocultas y 20 entradas.

| Retardo (pasos) | ReLU | LIF | TS-LIF |
|---|---|---|---|
| 10 | 0.5 | 0.748 | **0.994** |
| 20 | 0.5 | 0.504 | **0.977** |
| 30 | 0.5 | 0.504 | **0.791** |
| 40 | 0.5 | 0.500 | **0.585** |
| 50 | 0.5 | 0.500 | **0.585** |

- TS-LIF retiene memoria mucho más tiempo, aunque su acierto también **cae** con retardos de 40 pasos o más.

---

## 8. Conclusión del artículo (paráfrasis)
- TS-LIF es una neurona espigante de dos compartimentos diseñada para pronóstico: la dendrita procesa baja frecuencia y el soma alta frecuencia.
- Demuestran condiciones de estabilidad y analizan la respuesta en frecuencia.
- En 4 conjuntos supera a las SNN con LIF y, según los autores, también a las redes artificiales, especialmente a largo plazo.
- Es robusta ante datos faltantes y eficiente, por lo que se presenta como adecuada para entornos con recursos limitados.

## 9. Limitaciones y trabajo futuro (A.13)
- **Limitación:** no modela explícitamente las **correlaciones entre variables**, como hacen SAMformer o Crossformer.
- **Trabajo futuro:**
  1. Mecanismos SNN para correlaciones entre variables.
  2. Estructuras SNN más generales para **detección de anomalías, generación de series y CLASIFICACIÓN**.

---

## 10. Referencias clave del artículo (para la tesis)
- **Lv, C. et al. (2024).** *Efficient and Effective Time-Series Forecasting with Spiking Neural Networks.* ICML, PMLR, 33624–33637. Marco experimental y fuente de los rivales.
- **Zhang, S. et al. (2024).** *TC-LIF: A Two-Compartment Spiking Neuron Model for Long-Term Sequential Modelling.* AAAI, 16838–16847.
- **Hao, Z. et al. (2024).** *A Progressive Training Framework for SNN with Learnable Multi-hierarchical Model (LM-H).* ICLR.
- **Zheng, H. et al. (2024).** *Temporal dendritic heterogeneity incorporated with SNN for learning multi-timescale dynamics.* Nature Communications 15:277.
- **Yao, X. et al. (2022).** *GLIF.* NeurIPS 35.
- **Liu, Y. et al. (2024).** *iTransformer.*
- **Lin, S. et al. (2024).** *SparseTSF.* ICML.
- **Ilbert, R. et al. (2024).** *SAMformer.* ICML.
- **Bai, S. et al. (2018).** *Empirical Evaluation of Generic Convolutional and Recurrent Networks* (TCN).
- **Hawkins, J. & Ahmad, S. (2016).** *Why Neurons Have Thousands of Synapses.* Frontiers in Neural Circuits.
- **Bellec, G. et al. (2020).** *e-prop.* Nature Communications 11:3625.
- **Chen, C.-T. (1984).** *Linear System Theory and Design* (base del análisis de estabilidad y en frecuencia).

---

## 11. Análisis crítico (cómo se defendió y puntos débiles)

### 11.1 Cómo sostuvieron sus afirmaciones
1. **Teoría:** estabilidad (Teorema 1) y transferencia en frecuencia. Las cuentas del ejemplo son correctas (verificadas).
2. **Mecanismo visible** con una señal sintética de dos frecuencias.
3. **Comparación amplia:** 4 conjuntos × 4 horizontes × 3 arquitecturas frente a 11 modelos.
4. **Robustez** ante datos faltantes y ante la longitud de la historia.
5. **Ablación de neuronas** (TC-LIF, LM-H, CLIF).
6. **Comparación con métodos punteros** (SparseTSF, SAMformer).
7. **Energía teórica.**
8. **Prueba de memoria** (XOR retardado).
9. **Variabilidad** con 3 semillas.
10. **Limitaciones declaradas.**

### 11.2 Tamaño real de la ventaja
- Frente a redes artificiales, en R² medio: **+0,007** con TS-former y con TS-TCN; **+0,045** con TS-GRU.
- Con desviaciones típicas de hasta 0,005, +0,007 equivale a solo 1–2 desviaciones.
- **No ganan siempre:**
  - TCN > TS-TCN en Metr-la a 6 pasos (.820 frente a .810) y en Pems-bay a 96 (.689 frente a .652).
  - En la Tabla 6, TCN .973 > TS-TCN .971.
  - SparseTSF > TS-former en Electricity.
  - SparseTSF\* (con TS-LIF) no mejora a SparseTSF.

### 11.3 Debilidades metodológicas
- Los rivales **no se re-ejecutan**: sus resultados se copian de Lv et al. (2024).
- Solo **3 semillas**, sin **intervalos de confianza** ni **pruebas estadísticas** de las diferencias.
- «Validación cruzada» sin detallar cómo respeta el orden temporal; sin **preregistro**.
- La conclusión («supera consistentemente a las redes artificiales») va más allá de sus tablas.
- La energía es **teórica** (45 nm) y solo de inferencia; el entrenamiento es más lento.
- La separación de frecuencias de la Figura 4 usa **parámetros elegidos a mano**.
- Erratas menores: «TD-LIF» en A.1, «Datesets», «iSpikeformer»/«iSpikformer», una frase cortada en A.12.

### 11.4 Lección
Un artículo de primer nivel fue aceptado con **ventajas pequeñas, sin pruebas estadísticas y con excepciones**. Lo que se valoró fue la **idea**, la **teoría** y la **evidencia en conjunto**.

---

## 12. Relación con la tesis (E20-A0C)

| Aspecto | Artículo TS-LIF | Tesis (E20-A0C) |
|---|---|---|
| Tarea | Regresión multi-paso (R², RSE) | **Clasificación** de la dirección del precio (AUC), que es trabajo futuro del artículo |
| Dominio | Tráfico, solar, electricidad | **Bitcoin** (finanzas, mucho más ruidoso), con réplica en ETH y PAXG |
| Uso de la neurona | Capas TS-LIF dentro de TCN/GRU/Transformer, entrenadas de extremo a extremo | **Reservorio fijo** de 1 000 neuronas TS-LIF con recurrencia; **solo se entrena la lectura** (logística, C = 1e-3) |
| Parámetros | α, β, γ y κ aprendidos | Fijos; α1 = 0,82; κ no tiene efecto |
| Entradas | Serie cruda (codificador convolucional) | Retornos + **62 indicadores técnicos** como canales |
| Mecanismo de frecuencia | Dendrita paso bajo, soma paso alto (ejemplo con α2 = 0,05) | Verificado con parámetros reales: dendrita paso bajo, **soma paso banda** (pico entre 6 y 12 pasos), coherente con su teoría |
| Rivales | Copiados de otro artículo | **Re-ejecutados con las mismas entradas** (logística, RF, GBM, MLP, LSTM, TCN) |
| Estadística | 3 semillas, sin intervalos ni pruebas | Bootstrap de bloques, intervalos de confianza, placebos, preregistro, auditoría de fugas y prueba con datos futuros |
| Resultado | +0,007 de R² frente a redes artificiales | AUC 0,5460 frente a 0,5454 de GBM: **empate**; supera al ML en las series sintéticas |
| Coste | Entrena 7–15 veces más lento | Entrena **solo la lectura**: coste mínimo |

**Cómo usar este artículo en la defensa:**
1. Citarlo como **origen de la neurona** y del análisis en frecuencia. Mostrar que su teoría (sección 4.3) aplicada a nuestros parámetros predice lo que observamos.
2. Destacar que la tesis trabaja una línea que el artículo propone como **trabajo futuro (clasificación)** en un **dominio nuevo**.
3. Señalar que nuestro protocolo es **más estricto** que el suyo: rivales re-ejecutados, intervalos de confianza, preregistro y prueba con datos futuros.
4. Copiar de su forma de defenderse:
   - una **tabla de energía y tiempo** como su Tabla 6, donde nuestra ventaja de entrenar solo la lectura se ve clara;
   - un **control de memoria** sintético, equivalente al XOR retardado;
   - un apartado explícito de **limitaciones y trabajo futuro**.
5. Explicar las diferencias: reservorio fijo frente a entrenamiento completo, clasificación frente a regresión, e indicadores técnicos como entrada.

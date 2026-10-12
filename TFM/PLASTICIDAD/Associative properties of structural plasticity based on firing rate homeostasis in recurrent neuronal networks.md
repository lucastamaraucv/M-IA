# Associative properties of structural plasticity based on firing rate homeostasis in recurrent neuronal networks

**Autores:** Júlia V. Gallinaro y Stefan Rotter (Bernstein Center Freiburg & Faculty of Biology, Univ. de Freiburg).
**Revista:** Scientific Reports 8:3754 (2018). DOI 10.1038/s41598-018-22077-3. Recibido 16-oct-2017, aceptado 16-feb-2018. Acceso abierto (CC BY 4.0).
**Archivo:** `Associative properties of structural plasticity based on firing rate homeostasis in recurrent neuronal networks.pdf` (13 páginas).
**Estado de verificación:** texto extraído con `pdftotext` y **ecuaciones, tablas y constantes críticas verificadas visualmente contra las páginas 3, 4, 6, 7 y 9 del PDF** (marcadas ✔). Lo demás es transcripción fiel del texto extraído. Símbolos tal como en el artículo: ρ = tasa objetivo, β = parámetro de crecimiento de los elementos sinápticos.

---
## 1. Resumen (traducción del abstract)
Se supone que la plasticidad hebbiana basada en correlaciones da forma a la conectividad durante el desarrollo y el aprendizaje, mientras que la plasticidad homeostática estabiliza la actividad. Los autores estudian otro aspecto de esta dicotomía: ¿pueden propiedades asociativas hebbianas surgir como efecto de red a partir de una regla de plasticidad basada en principios homeostáticos a nivel de la neurona? Simulan una red recurrente de neuronas integrate-and-fire con pérdidas (LIF) cuyas conexiones excitatorias siguen una regla de **plasticidad estructural basada en homeostasis de la tasa de disparo**. Un subgrupo de neuronas que recibe estimulación externa más fuerte desarrolla **mayor conectividad dentro del grupo**. En un escenario bien documentado experimentalmente, la **conectividad específica de rasgo** (como la observada en corteza visual de roedores) emerge de esta regla. Los cambios estructurales inducidos por la estimulación **duran mucho tiempo** y decaen lentamente al volver a una entrada inespecífica.

## 2. Contexto y motivación (introducción)
- **Plasticidad funcional** = cambio de fuerza de sinapsis existentes. **Plasticidad estructural** = cambios de morfología axonal/dendrítica y **creación y eliminación de sinapsis**, incluidos espinas y botones (observada in vitro en cultivos organotípicos de hipocampo y in vivo en corteza sensorial y motora de roedores; también cambios presinápticos).
- Las **reglas exactas** de los cambios estructurales dependientes de actividad **no se conocen**. Modelos computacionales muestran que rasgos de la conectividad cortical pueden resultar de la interacción de varios mecanismos de plasticidad y que la regulación homeostática en múltiples escalas de tiempo es necesaria para estabilizar los cambios hebbianos.
- **Homeostática** = regulación de la conectividad que estabiliza la actividad en un punto de ajuste; **hebbiana** = cambia las conexiones según la correlación entre las actividades de dos neuronas.
- **Idea de Dammasch (1986, 1989):** el aprendizaje hebbiano puede emerger como **propiedad de red** con un algoritmo basado en la homeostasis de la tasa de cada neurona **sin referencia a correlaciones**. Los autores reimplementan ese algoritmo en un marco moderno (simulador NEST). Combina modelos precursores de Dammasch, van Ooyen & van Pelt y van Ooyen; ya usado para estudiar reconexión tras lesión/ictus, redes de mundo pequeño, criticalidad en redes en desarrollo y neurogénesis en el giro dentado. Esos modelos incluían un kernel de distancia; la implementación de NEST usada aquí **no**.
- Sadeh, Clopath & Rotter (2015) mostraron que un sesgo de conectividad específico de rasgo emerge en redes equilibradas con una regla funcional que combina hebbiana y homeostática; aquí se muestra con una regla **estructural** donde las correlaciones se evalúan **implícitamente** por el emparejamiento aleatorio de elementos pre y postsinápticos, sin que las sinapsis lleven registro de la actividad presináptica, y con **efectos estructurales de larga duración** compatibles con una memoria persistente.

## 3. Modelo y métodos
### 3.1 Red (Tabla 1 ✔)
N = 12 500 neuronas LIF con corriente sináptica (80 % excitatorias NE = 10 000, 20 % inhibitorias NI = 2 500).
Potencial subumbral de la neurona i (Ec. 1): **τ_m dV_i/dt = −V_i + τ_m Σ_j J_ij s_j(t − d)**.
- J_ij = amplitud pico del PSP, depende del tipo presináptico: J_E = J = 0.1 mV; inhibición más fuerte por un factor g = 8: J_I = −gJ = −0.8 mV. J_ext = 0.1 mV.
- s_j(t) = Σ_k δ(t − t_jk) = tren de espigas de la neurona j; algunas «neuronas» representan la entrada externa (proceso de Poisson de tasa ν_ext = 15 kHz agregada por neurona, independiente entre neuronas).
- Retardo de transmisión constante d = 1.5 ms; τ_m = 20 ms; umbral V_th = 20 mV; reset V_r = 10 mV mantenido durante t_ref = 2 ms (refractario).
- Grado de entrada fijo: **0.1·NI** para I→I e I→E, y **0.1·NE** para E→I (CE = 1000 conexiones excitatorias por neurona inhibitoria; CI = 250 inhibitorias por neurona). Esas conexiones permanecen **sin cambio**. Las conexiones **E→E (EE) están inicialmente ausentes** y solo surgen de la regla de plasticidad estructural.
- Simulaciones en NEST.

### 3.2 Plasticidad estructural homeostática (SP)
- Cada neurona excitatoria tiene una **tasa de disparo instantánea r_i** = tren de espigas filtrado paso-bajo (Ec. 2 ✔): **τ_r dr_i(t)/dt + r_i(t) = s_i(t)**, con **τ_r = 10 s**. (En el modelo original la actividad es la concentración intracelular de calcio, versión filtrada paso-bajo de la tasa.)
- A cada neurona excitatoria se asigna una **tasa objetivo ρ** y un conjunto de **elementos presinápticos** z^pre (botones axonales) y **postsinápticos** z^post (espinas dendríticas). Evolución (Ec. 3 ✔):
  **dz_i^k(t)/dt = −(1/β^k)(r_i(t) − ρ),  k ∈ {pre, post}**,
  con β^k = parámetro de crecimiento. Por defecto ρ = 8 Hz y β = 2 para todos los elementos pre y post de todas las neuronas excitatorias. Función **lineal** elegida como modelo fenomenológico genérico (trabajos previos usaron lineal, gaussiana o logística; no hay datos experimentales directos de cómo varía el número de elementos con la tasa). Elementos libres **no decaen** en el modelo principal (en el original decaen con cierta tasa; con decaimiento los resultados principales no cambian, ver material suplementario).
- **Cada Δt = 100 ms** se aplican las reglas: se **eliminan** sinapsis existentes y se **crean** nuevos contactos para que el número de elementos coincida con el de contactos activos.

### 3.3 Eliminación y creación de sinapsis (Ec. 4 ✔)
Con C = matriz con el número de sinapsis entre neuronas presinápticas j y postsinápticas i:
**Δz_j^pre = z_j^pre − Σ_i C_ij  y  Δz_i^post = z_i^post − Σ_j C_ij.**
- Si Δz^k < 0 (más contactos que elementos): se **eliminan |Δz^k| sinapsis elegidas al azar** entre los contactos existentes de la neurona. Tras eliminar una sinapsis por pérdida de un elemento presináptico (postsináptico), el elemento postsináptico (presináptico) correspondiente **queda disponible** para una nueva conexión.
- Si Δz^k > 0: la neurona tiene Δz^k **elementos libres**. **Todos los elementos libres de la red se combinan al azar en pares pre–post** para formar sinapsis nuevas. El número de sinapsis formadas está limitado por el total de elementos pre y por el total de elementos post de toda la red. Cada sinapsis nueva tiene **fuerza fija J**. Se permiten sinapsis múltiples entre el mismo par pero **no autosinapsis**. (Detalles de implementación en Butz & van Ooyen 2013 y Diaz-Pier et al. 2016.)

### 3.4 Estimulación de subgrupo
Redes crecidas primero sin entrada estructurada (todas las excitatorias con Poisson de igual tasa ν_ext). Tras 750 s (cuando hay suficientes conexiones EE y todas las neuronas disparan cerca de su objetivo) un subgrupo del **10 %** de excitatorias recibe entrada externa aumentada (**1.1 ν_ext durante 150 s**); luego vuelve a ν_ext para todas. Se monitorea actividad y conectividad durante 5500 s.

### 3.5 Protocolo de estimulación visual (Tabla 3 ✔)
Cada neurona excitatoria recibe Poisson con tasa modulada por la orientación del estímulo θ y su orientación preferida de entrada θ_PO (uniforme en [0°, 180°)) (Ec. 5 ✔):
**ν_mod(θ, θ_PO) = ν_ext [1 + μ cos(2(θ − θ_PO))]**, ganancia μ = 0.15.
Un θ nuevo aleatorio uniforme en [0°, 180°) cada **t_st = 1 s**, **N_st = 5000** estímulos; luego entrada no modulada ν_ext durante **t_post = 10 000 s**.

### 3.6 Análisis de trenes de espigas
- Correlación de recuentos entre neuronas i, j (Ec. 6 ✔): **R_ij = c_ij / √(c_ii c_jj)** (covarianza de recuentos en bins de 10 ms, 20 s de actividad).
- Irregularidad (Ec. 7 ✔): **CV_i = σ_i/μ_i** (coeficiente de variación de los intervalos entre espigas, 20 s).

### 3.7 Parámetros (Tablas 1–3 ✔)
| Tabla | Parámetro | Símbolo | Valor |
|---|---|---|---|
| 1 | neuronas / excitatorias / inhibitorias | N, NE, NI | 12 500 / 10 000 / 2 500 |
| 1 | conexiones excitatorias entrantes por neurona inhibitoria; inhibitorias entrantes por neurona | CE, CI | 1000; 250 |
| 1 | peso de referencia; razón inhibición/excitación | J; g | 0.1 mV; 8 |
| 1 | peso excitatorio / inhibitorio / externo | J_E, J_I, J_ext | 0.1 mV; −0.8 mV; 0.1 mV |
| 1 | tasa de entrada externa | ν_ext | 15 kHz |
| 1 | constante de membrana; retardo; umbral; reset; refractario | τ_m; d; V_th; V_r; t_ref | 20 ms; 1.5 ms; 20 mV; 10 mV; 2 ms |
| 2 | constante de tiempo de la tasa de disparo | τ_r | 10 s |
| 2 | parámetro de crecimiento de elementos | β | 0.2, 0.625, **2**, 6.25, 20 |
| 2 | tasa objetivo | ρ | 5, 6, 7, **8**, 9 Hz |
| 2 | intervalo de plasticidad estructural | Δt | 100 ms |
| 3 | modulación de entrada; orientación del estímulo y preferida | μ; θ, θ_PO | 0.15; [0°, 180°) |
| 3 | tiempo por estímulo; número de estímulos; tiempo post-estimulación | t_st; N_st; t_post | 1 s; 5000; 10 000 s |
(Negrita = valores por defecto.)

## 4. Resultados
### 4.1 Las redes crecidas son aleatorias sin entrada estructurada (Fig. 1)
- Con ρ = 8 Hz (tasa esperada de las excitatorias con 10 % de conectividad EE) el **grado de entrada y de salida EE crece desde 0 y se estabiliza en ≈ 1000** (conectividad EE ≈ 10 %). La regla sigue activa y las conexiones individuales siguen creándose y borrándose; la red se considera en equilibrio cuando las excitatorias disparan en promedio a su tasa objetivo.
- Con sinapsis múltiples permitidas, la distribución del **número de sinapsis por par** es aproximadamente **Poisson**. Si los contactos fueran variables de Poisson independientes, grado de entrada y salida satisfarían σ² = μ; observan **σ² < μ** (distribuciones de grado más estrechas que Poisson); con tasas objetivo extraídas de distribuciones más anchas se obtienen distribuciones de grado más anchas y los resultados principales no cambian (suplemento).
- Régimen de la red: inhibición dominante con conectividad aleatoria del 10 % → tasas bajas, **asíncrono-irregular (AI)**; correlaciones por pares bajas, **CV ≈ 0.7**, tasa media de las excitatorias **8 Hz** (calculado con 20 s de espigas). Las redes crecidas presentan algunos rasgos no aleatorios (suplemento), pero las desviaciones se consideran pequeñas.

### 4.2 Constante de tiempo del crecimiento (Fig. 2 ✔)
- Definen **τ_growth = s/α**, con s = valor de meseta de la conectividad (promedio de los últimos 4 puntos temporales) y **α = pendiente máxima (casi siempre inicial)** de la serie de conectividad.
- En log-log, τ_growth vs β tiene **pendiente 1** (dependencia **lineal** de β), a lo largo de **más de 3 órdenes de magnitud**; el crecimiento es más rápido con ρ más alto. Definen el **coeficiente γ = τ_growth/β** (Fig. 2B; desde ≈ 240 s para ρ = 5 Hz hasta ≈ 130 s para ρ = 9 Hz), y reescalan el tiempo en unidades de **γ·β** (Fig. 2C): todas las curvas de crecimiento coinciden.
- Estabilidad: el proceso es estable en al menos 3 órdenes de magnitud de β; un proceso aún más lento daría simulaciones muy largas sin razón para desestabilizar; **un β que dé crecimiento en horas o días** casaría con datos experimentales; **hacerlo más rápido puede desestabilizar el sistema** porque aumentaría la tasa de contactos nuevos. Además hay límites biológicos de velocidad (recambio de proteínas y transporte).

### 4.3 Propiedades asociativas de la SP (Fig. 3) — Ec. 8 ✔
Cambio esperado de conectividad inducido por el algoritmo (adaptado de Butz & van Ooyen 2013; solo EE plásticas y sin dependencia de distancia):
```
ΔC_ij = C_ij · Δz_j^pre / z_j^pre                       si Δz_j^pre < 0
ΔC_ij = C_ij · Δz_i^post / z_i^post                     si Δz_i^post < 0
ΔC_ij = Δz_j^pre · Δz_i^post / max(Σ_k Δz_k^pre, Σ_k Δz_k^post)   si Δz_j^pre > 0 y Δz_i^post > 0
```
Interpretación de los autores: **el aumento de conectividad ocurre cuando dos neuronas están simultáneamente en estado de baja actividad** → aprendizaje hebbiano implementado como **regla de covarianza**; en periodos de actividad elevada la conectividad **disminuye de forma inespecífica**, similar a un **escalado sináptico dependiente del peso**, afectando elementos pre y post.
Experimento (Fig. 3): tras el crecimiento, un subgrupo (10 % de las excitatorias) recibe 150 s de entrada mayor. Al empezar, su tasa instantánea sube, lo aleja de su objetivo y dispara reconexión; su **conectividad decae** hasta que la tasa vuelve al objetivo. Al terminar la estimulación específica la tasa del subgrupo **cae por debajo del punto de ajuste** (la amplificación excitatoria recurrente se redujo por las conexiones eliminadas), lo que dispara de nuevo reconexión y creación de elementos pre y post; como el efecto en la tasa del resto es mucho menor, **hay más elementos disponibles del subgrupo y es más probable que formen conexiones dentro del subgrupo** que con neuronas fuera (Fig. 3B). La reconexión continúa lentamente tras alcanzar la tasa objetivo (≈ 300 s después), porque el cambio de elementos es proporcional a r(t) − ρ. La mayor conectividad dentro del subgrupo **dura más** que la desviación de actividad (Fig. 3C, E).

### 4.4 Conectividad específica de rasgo en un modelo simple de V1 (Fig. 4 ✔)
- Antes de la estimulación orientada la conectividad EE es aleatoria, sin sesgo respecto de θ_PO. Tras **5000 estímulos** las neuronas con **θ_PO similar** tienen mayor probabilidad de conexión (modulada por la diferencia de θ_PO de cada par). Mecanismo: cuando una neurona dispara por debajo de su tasa objetivo, crea elementos; por encima, los borra; neuronas con θ_PO similar aumentan sus elementos en los mismos periodos de estímulo y por tanto **tienen mayor probabilidad de crear sinapsis entre sí**. También se modula el número de sinapsis por par conectado (Fig. 4F; sinapsis múltiples).
- **Caída conspicua de la conectividad media** durante la estimulación orientada. Explicación: la no linealidad de la curva entrada-salida de LIF eleva 1 Hz la tasa media con la modulación, y con SP eso implica reducir conectividad para mantener la tasa en el objetivo (comprobado con una red estática con 10 % de conectividad: tasa +1 Hz; material suplementario).
- **Los cambios estructurales decaen muy lentamente** (Fig. 4D–G): tras 10 000 s de entrada no modulada hay todavía un ligero sesgo por orientación. Ajuste exponencial a los dos primeros componentes de Fourier de la modulación de conectividad: **τ₁ = 1102 s** (creación del sesgo específico, 1.º componente durante/tras la estimulación) y **τ₂ = 5192 s** (destrucción). **Crear el sesgo es ≈ 5 veces más rápido que destruirlo.** (Nota: en la primera ficha se transcribieron mal estas cifras; las correctas son las de la Fig. 4G del PDF.) El componente DC (conectividad media) baja durante la estimulación y vuelve rápido al valor previo cuando termina; la modulación decae lento: hay **diferentes escalas de tiempo para crear y destruir** conectividad específica. Las series temporales de multiplicidad de sinapsis son cualitativamente muy similares (suplemento).

## 5. Discusión
- **Resumen:** una regla SP basada en homeostasis de tasa, en la que solo crecen las conexiones EE, comparte propiedades funcionales importantes con una regla de aprendizaje hebbiana, con escalas de tiempo distintas de creación y decaimiento de las asociaciones; en un modelo genérico de corteza visual, la conectividad específica de rasgo similar a V1 de ratón **emerge del modelo SP** y **persiste** tras apagar la estimulación específica.
- **Escalas de tiempo:** la plasticidad estructural en el cerebro cubre minutos, horas o días; el modelo SP se puede ajustar para estudiar escalas que abarquen al menos tres órdenes de magnitud. Minerbi et al. (2009) vieron distribución de tamaños sinápticos estable durante días con remodelado individual continuo; en el modelo SP los elementos se remodelan rápido y la estructura global evoluciona más lento (grado medio y distribuciones estables, sinapsis individuales plásticas).
- **Parámetros de crecimiento:** se usó la combinación más simple (controladores lineales idénticos para elementos pre y post); hay evidencia de que el crecimiento de axones es algo más lento que el de espinas; la elección lineal es consistente con estudios empíricos (más espinas nuevas tras deprivación monocular; tras lesiones pequeñas de retina). Keck et al. mostraron aumento del tamaño de espinas sin cambio de densidad (compensación funcional); la homeostasis probablemente resulta de la interacción de plasticidad funcional y estructural. Canty et al. (2013) mostraron rebrote axonal in vivo tras ablación con densidades de botones similares a las previas (consistente con homeostasis).
- **Lo que no se reprodujo:** distribución ancha y sesgada de tasas de disparo y de fuerzas sinápticas, y estadísticas específicas de motivos de pares y tríadas. La estructura y la dinámica corticales emergen de la interacción de múltiples mecanismos; un modelo completo debería incluir varios; simular una sola regla permite ver sus efectos aislados, pero queda abierto cómo interactúa con otras plasticidades.
- **Tesis de Dammasch apoyada:** el aprendizaje hebbiano no está necesariamente ligado a sinapsis individuales; puede surgir como propiedad del sistema. El control homeostático ocurre a nivel de **neuronas completas**, no de sinapsis; las neuronas controlan el número de elementos (sinapsis putativas) pero no la formación de sinapsis específicas, que se implementa por **cableado aleatorio** de elementos disponibles. No hace falta que las neuronas sigan la actividad individual de otras: solo la propia; el cableado aleatorio implementa la dependencia de la correlación (relación con la «visión neurocéntrica del aprendizaje» de Titley et al. 2017).
- **Clasificación de Fauth & Tetzlaff (2016):** (i) **hebbiana** si el número de sinapsis aumenta (disminuye) con actividad alta (baja); (ii) **homeostática** si aumenta (disminuye) con actividad baja (alta). La regla SP es una variante **homeostática**; a nivel de red implementa una forma de plasticidad hebbiana. Otra clasificación consideraría los efectos sobre la conectividad; en experimentos solo se observa el efecto en la red y puede ser imposible conocer los mecanismos.
- **Aprender más rápido que olvidar:** el remodelado se dispara por la **discrepancia** entre actividad y tasa objetivo: con entrada modulada la tasa se aleja del punto de ajuste y hay reconexión fuerte; con entrada no modulada la actividad vuelve rápido al objetivo y la reconexión se hace muy lenta (depende de la amplitud de fluctuaciones aleatorias). Fauth et al. (2015) mostraron aprendizaje rápido y olvido lento en un modelo estocástico (formación aleatoria con probabilidad constante; eliminación dependiente del número de sinapsis y de la estimulación).
- **Comparación con otros modelos:** Hiratani & Fukai (2014) forman asambleas con depresión a corto plazo, log-STDP y homeostasis, con actividad sostenida (memoria de trabajo) y aumento del peso sináptico medio durante la estimulación; aquí la **traza de memoria está en la conectividad sin actividad sostenida** (memorias contextuales) y la **conectividad media baja durante la estimulación y sube después**: inmediatamente tras el fin de la estimulación la conectividad dentro del grupo estimulado es **menor** que la basal (contraintuitivo; compatible con deterioro perceptual tras repetición el mismo día seguido de mejora a las 24–48 h).
- **Homeostasis y sueño:** la hipótesis de homeostasis sináptica (Tononi & Cirelli) vs resultados de Hengen et al. (2016): la homeostasis se inhibe durante el sueño y se promueve en vigilia; puede haber más en la plasticidad homeostática que solo estabilizar la red.

## 6. Limitaciones declaradas
Solo EE plásticas (el resto estático); sin plasticidad funcional (STDP); sin kernel de distancia; no se estudia en profundidad el efecto de la tasa objetivo en las distribuciones de grado; los rasgos de motivos y la distribución sesgada de tasas/pesos no se reproducen.

## 7. Referencias clave citadas en el texto
Dammasch 1986 (*Biol. Cybern.* 54:211) y 1989 (en *Models of Brain Functions*, CUP); Butz & van Ooyen 2013 (*PLoS CB* 9:e1003259); Diaz-Pier et al. 2016 (*Front. Neuroanat.* 10:57); Sadeh, Clopath & Rotter 2015 (*PLoS CB* 11:e1004307); Fauth & Tetzlaff 2016 (*Front. Neuroanat.* 10:75); Fauth, Wörgötter & Tetzlaff 2015 (*PLoS CB* 11:e1004684); Deger, Seeholzer & Gerstner 2017 (multicontact cooperativity); Brunel 2000 (*J. Comput. Neurosci.* 8:183); Turrigiano 2012; Zenke et al. 2015, 2017; Hengen et al. 2013, 2016; Keck et al. 2013; Titley, Brunel & Hansel 2017.

## 8. Relevancia para E20 (interpretación, no del artículo)
- **Contraste directo con las pruebas Rsp/Rgrow del proyecto:** allí la creación se guió por **correlación pre-post** (hebbiana) y la tasa de disparo se duplicó; aquí la creación depende de que la neurona esté **por debajo** de su tasa objetivo (retroalimentación **negativa**) y la tasa se mantiene en ρ.
- Algoritmo implementable y verificable: tasa filtrada → elementos pre/post con crecimiento lineal → eliminación aleatoria → emparejamiento aleatorio de elementos libres; ΔC_ij (Ec. 8) sirve como **test numérico**; τ_growth ∝ β da la regla de escala para la velocidad.
- Parámetros de partida adaptables: razón Δt/τ_r = 1/100; β gobierna la velocidad; ρ fija la tasa de disparo deseada (para E20, la tasa de A0 ≈ 0.22–0.25).

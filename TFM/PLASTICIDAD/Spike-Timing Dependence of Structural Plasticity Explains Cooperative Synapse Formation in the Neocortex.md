# Spike-Timing Dependence of Structural Plasticity Explains Cooperative Synapse Formation in the Neocortex

**Autores:** Moritz Deger, Moritz Helias, Stefan Rotter, Markus Diesmann (Bernstein Center Freiburg; INM-6 Forschungszentrum Jülich; RWTH Aachen).
**Revista:** PLoS Computational Biology 8(9): e1002689 (2012). DOI 10.1371/journal.pcbi.1002689. Recibido 10-may-2012, aceptado 26-jul-2012, publicado 20-sep-2012. Editor: Olaf Sporns. Acceso abierto (CC BY).
**Archivo:** `Spike-Timing Dependence of Structural Plasticity Explains Cooperative Synapse Formation in the Neocortex.pdf` (13 páginas).
**Estado de verificación:** texto con `pdftotext`; **Ec. 4–7, Ec. 11–14 y la Tabla 1 verificadas visualmente contra las páginas 3, 4 y 5 del PDF** (✔). El resto es transcripción del texto extraído.

---
## 1. Resumen (traducción del abstract)
La plasticidad estructural gobierna el desarrollo a largo plazo de las conexiones sinápticas en el neocórtex. Hay fuerte evidencia de que se puede **descartar** un proceso de formación y poda de sinapsis excitatorias **aleatorio e independiente**: debe haber **cooperación** entre los contactos sinápticos que conectan un par pre/postsináptico; el mecanismo era desconocido. Los autores demuestran que la **detección local de correlación en la espina dendrítica postsináptica** basta para explicar el efecto de cooperación, sin vía de interacción directa entre contactos. Mecanismos biomoleculares candidatos para la detección de correlación dendrítica y para la plasticidad estructural basada en ella ya se han identificado. Con el análisis y ajuste de un modelo simple, muestran que la **plasticidad estructural dependiente de la correlación de espigas**, sin mecanismos adicionales de interacción entre sinapsis, reproduce las **distribuciones experimentales del número de contactos sinápticos entre pares de neuronas** en neocórtex. Además, el modelo da una primera explicación de la existencia de espinas dendríticas **transitorias y persistentes** y permite hacer predicciones para experimentos futuros.

## 2. Contexto (introducción)
- La estructura de las redes neocorticales cambia: se forman, maduran y se podan sinapsis nuevas en adultos y en desarrollo. ≈ **90 %** de los contactos excitatorios terminan en espinas dendríticas y **96 %** de las espinas forman una sinapsis. Recambio medio de espinas: **5.7 %/día** en corteza visual primaria y **15.4 %/día** en somatosensorial (Holtmaat et al.). Pese al recambio, las **estadísticas** del número de sinapsis se conservan en el adulto: creación y poda se equilibran. Estudios teóricos de redes asociativas: la plasticidad estructural **aumenta sustancialmente la capacidad de memoria** y se relaciona con aprendizaje motor.
- Tres estudios (Feldmeyer 2002; Markram 1997; Feldmeyer 1999) midieron las distribuciones del número de contactos por par en corteza somatosensorial de rata (L4→L2/3, L5→L5, L4→L4). Fares & Stepanyants (2009) mostraron que la formación **independiente** de contactos con un conjunto de sitios potenciales (aposiciones cercanas axón-dendrita) **no puede explicar** las distribuciones; hace falta una **poda cooperativa**: los contactos de una misma sinapsis se estabilizan mutuamente.
- Este trabajo va más allá en dos aspectos: (1) procesos sinápticos que operan de forma **continua en el tiempo**; (2) investiga un **mecanismo candidato explícito** de cooperación: detección local de correlación en la espina y maduración y poda dependientes de ella.
- Kasai et al. resumieron propiedades de plasticidad de espinas; su modelo (Yasumatsu et al. 2008) describe la dinámica del volumen de las espinas; aquí se restringe a **tres categorías** de estado y se introduce dependencia explícita del timing. Otros modelos de plasticidad estructural (Dammasch; Butz & Teuchert-Noodt; van Ooyen) se basan en la **tasa de disparo**, no en timing ni correlaciones, y por tanto no pueden mostrar este mecanismo de cooperación. El timing relativo pre/post sí influye en la plasticidad estructural de la espina (Helias et al. 2008, modelo biofísico con cinética de proteínas, CaMKII); este trabajo elige una escala intermedia.
- **Supuestos del modelo** (requeridos para explicar cualitativamente los resultados experimentales): (a) la liberación presináptica de glutamato causa despolarización postsináptica en sinapsis excitatorias; (b) la despolarización se propaga eléctricamente en la dendrita; (c) hay un mecanismo sensible al **tiempo relativo** pre/post (p. ej. receptores NMDA) con efectos aguas abajo sobre la amplitud sináptica evocada, tipo STDP; (d) las sinapsis de **amplitud pequeña** se podan con más probabilidad que las fuertes.

## 3. Modelo y métodos (ecuaciones numeradas como en el artículo)
### 3.1 Traza de correlación en el contacto (Ec. 1–3)
Un potencial de acción postsináptico despolariza el sitio de cada espina; la espina mantiene una señal que depende del tiempo del PA respecto de la llegada del impulso presináptico (**traza de correlación q(t)**).
- Si la neurona presináptica disparó poco antes de la postsináptica → q aumenta en 1 (**evento causal**); orden opuesto → q disminuye en 1 (**anti-causal**). La traza es «olvidadiza» (fuga con constante τ > 0) y con ruido aditivo.
- **Ec. 1:** dq/dt = −q/τ + g(t) s(t) + η(t). s(t) = Σ_k δ(t − t_k) = tren de espigas postsináptico; g(t) ∈ {−1, +1} indica evento causal o anti-causal; η(t) = ruido blanco de media 0 y varianza infinitesimal ξ². Matemáticamente q es un **ruido de disparo (shot noise)** con kernel exponencial h(t) = Θ(t) e^{−t/τ} accionado por g(t)s(t) + η(t).
- Modelo mínimo de espigas correlacionadas: para cada espiga postsináptica el evento más cercano presináptico es causal (si ocurrió antes) con probabilidad **p**; si ambas neuronas disparan independientes p = 0.5. g = +1 con probabilidad p y −1 con 1−p. (Estrictamente el proceso es no físico porque depende de eventos futuros; se considera una **descripción efectiva adiabática**; podría resultar de implementaciones biofísicas causales, p. ej. el número de macromoléculas CaMKII activadas o la potenciación a largo plazo.)
- Con espigas postsinápticas Poisson de tasa ν (la sinapsis modelada contribuye poco), y τν ≫ 1 (la plasticidad estructural es lenta frente a la actividad), la distribución de equilibrio de q es **normal** con media μ y varianza σ² (**Ec. 2, 3**):
  **μ = τν[p − (1−p)] = τν(2p−1)**,  **σ² = ½(τν + ξ²)**.
  (σ² es independiente de p. Se obtienen sumando dos procesos independientes q_s y q_η.)

### 3.2 Probabilidad causal en función del número de contactos (Ec. 4–5 ✔)
p depende del número x de sinapsis activas (cada sinapsis excitatoria aumenta la probabilidad de que la presináptica haga disparar a la postsináptica). Para neuronas integrate-and-fire (Helias et al. 2010) la probabilidad de respuesta es proporcional al peso sináptico para un amplio rango; con integración lineal el peso es proporcional al número de contactos activos:
**p(x) = p₀ + xΔ** con p₀ = 0.5 y Δ = probabilidad de respuesta por sinapsis. Para un solo contacto con EPSP de amplitud w: **Δ = P_r(w) ≈ w·m, m = 0.05 (mV)⁻¹** (Fig. 4D de Helias 2010):
**(Ec. 4) p(x) = p₀ + m w x**, y **(Ec. 5) μ(x) = τν(2p₀ − 1 + 2 m w x)**.
Se fija ν = 5 Hz para reducir parámetros libres. El modelo lineal puede dar p > 1 para x y w grandes (debería saturar en 1), pero no afecta a las soluciones halladas (probabilidad nula en esos x).

### 3.3 Plasticidad estructural basada en la traza (Ec. 6–10 ✔)
- La traza de correlación guía la plasticidad estructural. Se asume equilibrio estocástico (**aproximación adiabática**) y que un cambio estructural se inicia cuando q **cruza un umbral θ**: problema de **primer paso** con frontera absorbente; el inverso del tiempo medio de primer paso es la **tasa de escape**. Aproximando q por movimiento browniano con la misma media y varianza infinitesimal, la **aproximación de Arrhenius** da **Ec. 6: tasa de escape ∝ exp(−(θ−μ(x))²/σ²)** (para |θ−μ| ≫ σ); la constante de proporcionalidad es la constante de Arrhenius.
- Extrapolación con meseta (la maquinaria celular tiene una tasa máxima), **Ec. 7**:
  **κ(α, θ, μ, σ) = |α| · exp(−(θ−μ(x))²/σ²)  si α(θ−μ(x)) > 0;  = |α|  en otro caso**, α ∈ ℝ. Según el signo de α la función se **acerca o se aleja de la meseta** al aumentar μ (saturación a la derecha o a la izquierda; Fig. 1C).
- Maduración, encogimiento y poda son procesos distintos: se usa κ con distintos {α, θ} y ruido ξ para cada uno (subíndices m, s, p):
  **λ_m(x) = κ(α_m, θ_m, μ(x), σ_m)** (Ec. 8), **λ_s(x) = κ(α_s, θ_s, μ(x), σ_s)** (Ec. 9), **λ_p(x) = κ(α_s, θ_s, μ(x), σ_m)** (Ec. 10; la poda usa los parámetros del encogimiento salvo la magnitud de ruido ξ_m de la maduración, porque la poda ocurre en espinas finas).
- Parámetros {τ, ν, Δ, p₀} idénticos para espinas finas (contactos inactivos) y grandes (activos). Además **fluctuaciones intrínsecas**: maduración, encogimiento y poda aleatorias con tasa **λ_i**, y **creación de espinas finas con tasa λ_c** (que fija la escala de tiempo).
- Resumen del modelo: en cada contacto una traza cuenta pareamientos causales y anti-causales pre-post; su distribución depende del número de contactos activos (todos contribuyen a disparar la postsináptica); los cambios estructurales dependen de las trazas; más fluctuaciones intrínsecas.

### 3.4 Estado estacionario de la sinapsis (Ec. 11–16 ✔)
- **Tres estados por aposición cercana:** **activo** (espina grande, con AMPA y NMDA), **inactivo** (espina fina, nueva o recién encogida, mucho menos AMPA, contribuye poco a disparar) y **no realizado** (aposición cercana sin contacto, «sinapsis potencial» de Fares & Stepanyants). x + y + z = N; el estado de la sinapsis queda definido por (x, y).
- Un conjunto de sinapsis independientes, cada una con N aposiciones; la probabilidad p_(x,y) obedece a la **ecuación maestra (Ec. 11)**:
  d/dt p(x,y) = −p(x,y)[(x+2y)λ_i + (N−x−y)λ_c + xλ_s(x) + yλ_p(x) + yλ_m(x)] + (x+1)p(x+1,y−1)[λ_s(x+1)+λ_i] + (y+1)p(x,y+1)[λ_p(x)+λ_i] + (y+1)p(x−1,y+1)[λ_m(x−1)+λ_i] + (N−x−y+1)p(x,y−1)λ_c.
  (Término 1 = tasa de salir del estado; 2–3 = entradas por encogimiento y poda; 4 = maduración; último = creación de sinapsis inactivas con tasa λ_c.) La distribución estacionaria **no depende de la escala de tiempo** de las tasas: se consideran α_m, α_s, λ_i en unidades de λ_c; la escala de tiempo de la plasticidad estructural es 1/λ_c.
- Numerando los estados {(x,y)|x+y ≤ N}: **dp/dt = M p (Ec. 12)**; M es **estocástica por columnas** (proceso de Markov); por **Perron–Frobenius** hay una única solución estacionaria p⁰(N) (M p⁰ = 0 con Σ p_i⁰ = 1), construida con Cython y resuelta con SciPy. Depende del número de aposiciones N; Fares et al. dan P(N) hasta N_max = 20. **Distribución promediada (Ec. 13):** p_i^avg = Σ_{N=0}^{N_max} P(N) p_i⁰(N). **Marginales:** P(n) = Σ_i p_i^avg 1[x(i)+y(i)=n] (Ec. 14); P(x) = Σ_i p_i^avg 1[x(i)=x] (Ec. 15); P(y) = Σ_i p_i^avg 1[y(i)=y] (Ec. 16).

### 3.5 Ajuste a datos de referencia (Ec. 17–19)
Frecuencias f_n de número de contactos n ≥ 1 en pares (Feldmeyer 2002; Markram 1997; Feldmeyer 1999) y probabilidad P_con de conexión con al menos un contacto activo (Fares & Stepanyants). Distribución de referencia: **P_ref(n) = 1 − P_con (n = 0); P_con f_n/Σ_m f_m (n ≥ 1)** (Ec. 17). **Residuos r_n = [P(n) − P_ref(n)] / max_{n≥1} P_ref(n)** (Ec. 18) y **error R = Σ_{x=1}^{N_max} r_x²** (Ec. 19), minimizado con Levenberg–Marquardt en un espacio de **8 parámetros** (τ, ξ_m, ξ_s, α_m, α_s, θ_m, θ_s, λ_i) con **4⁸ = 65 536 inicializaciones** por conjunto (varios mínimos locales). También se ajustaron L4–L4 y L5–L5 con un solo conjunto de parámetros (error sumado).

### 3.6 Tiempos de vida y recambio (Ec. 20–25)
- Tiempo medio activo→inactivo: t_ia(x) = 1/(λ_i + λ_s(x)); inactivo→activo: t_ai(x) = 1/(λ_i + λ_m(x)); inactivo→no realizado: t_pi = 1/(λ_i + λ_p(x)). Tiempo medio hasta la primera transición del inactivo: t̂_i(x) = 1/(t_ai⁻¹(x) + t_pi⁻¹); P_ai(x) = t_ai⁻¹ t̂_i, P_pi(x) = 1 − P_ai(x).
- **Vida esperada del contacto inactivo (Ec. 20–22):** T_i(x) = P_pi t̂_i + P_ai [t̂_i + T_a(x+1)]; **T_a(x) = t_ia(x) + T_i(x−1)** (Ec. 21) ⇒ **T_i(x) = [t̂_i(x) + t_ia(x+1) P_ai(x)]/(1 − P_ai(x))** (Ec. 22). Promedios sobre el equilibrio: ⟨T_i⟩ = Σ_N P(N) Σ_i p_i⁰(N) T_i(x(i)) (Ec. 23); ⟨T_a⟩ análoga (Ec. 24).
- **Calibración de la escala de tiempo con el recambio de espinas (TOR, Holtmaat 2005)** (Ec. 25): TOR = (n_ganadas + n_perdidas)/(2 n_total), con n_ganadas = Σ_N P(N) Σ_i p_i⁰(N) λ_c z(i), n_perdidas = Σ_N P(N) Σ_i p_i⁰(N)(λ_p(x(i)) + λ_i) y(i), n_total = Σ_N P(N) Σ_i p_i⁰(N)(x(i)+y(i)); con **TOR = 15.4 %/día** (somatosensorial de ratón) se obtiene λ_c = 15.4 %/día / (TOR·λ_c).

### 3.7 Necesidad de contactos inactivos (Ec. 26)
Modelo simplificado sin estado inactivo (solo ausente/activo): equilibrio de flujos de probabilidad **p_{x+1}/p_x = [(N−x) λ_c(x)] / [(x+1) λ_p(x+1)]** (Ec. 26). En los tres conjuntos P_ref(1)/P_ref(0) ≈ 0, lo que exige λ_c(0)/λ_p(1) ≈ 0, y cerca del segundo pico λ_c y λ_p comparables: requiere funciones **muy no monótonas** de x difíciles de justificar biofísicamente. Con el estado inactivo intermedio es posible hallar conjuntos de parámetros biológicamente plausibles.

## 4. Resultados
### 4.1 Parámetros ajustados (Tabla 1 ✔)
Valores fijos comunes: m = 0.05 (mV)⁻¹, p₀ = 0.5, ν = 5 Hz.
| Conexión | L4–L2/3 | L5–L5 | | L4–L4 | |
|---|---|---|---|---|---|
| Referencia | Feldmeyer 2002 | Markram 1997 | | Feldmeyer 1999 | |
| w (mV) | 0.0813 | 0.63 | | 0.44 | |
| ⟨N⟩ ± DE | 4.040 ± 5.010 | 5.998 ± 7.312 | | 4.368 ± 5.358 | |
| Mostrado en | Fig. 1a | Fig. 1b | Fig. 2a | Fig. 1c | Fig. 2b |
| τ (s) | 1.28E+09 | 3.95E+08 | 2.74E+05 | 4.32E+11 | 2.74E+05 |
| ξ_m (1/√s) | 511.109 | 3.80E+03 | 31.955 | 1.75E+05 | 31.955 |
| ξ_s (1/√s) | 449.392 | 1.844 | 30.974 | 0.330 | 30.974 |
| α_m (λ_c) | −4.33E+06 | −3.68E+04 | −3.90E+04 | −1.85E+06 | −3.90E+04 |
| α_s (λ_c) | −6.80E+10 | −2.63E+08 | −7.82E+09 | −4.99E+04 | −7.82E+09 |
| θ_m | 1.82E+08 | 3.90E+08 | 6.53E+04 | 5.55E+10 | 6.53E+04 |
| θ_s | 64.259 | 2.07E+06 | −1.61E+04 | 1.04E+11 | −1.61E+04 |
| λ_i (λ_c) | 346.847 | 18.029 | 3.129 | 4.345 | 3.129 |
| R (error) | 0.0008 | 0.0460 | 0.4926 | 0.0447 | 0.1808 |
| ⟨x⟩ | 0.091 ± 0.633 | 0.182 ± 0.931 | 0.151 ± 0.729 | 0.545 ± 1.265 | 0.489 ± 1.076 |
| ⟨y⟩ | 4.66E−04 ± 0.022 | 0.020 ± 0.174 | 0.114 ± 0.619 | 0.045 ± 0.297 | 0.252 ± 0.755 |
| ⟨x+y⟩ | 0.091 ± 0.637 | 0.202 ± 1.041 | 0.265 ± 1.269 | 0.590 ± 1.421 | 0.740 ± 1.680 |
| Corr[x,y] | 0.148 | 0.581 | 0.772 | 0.440 | 0.674 |
| d⟨x⟩/dp₀ | 398.016 | 12.782 | −22.455 | −34.488 | 153.283 |
| d⟨y⟩/dp₀ | 1.789 | 1.495 | −16.185 | −2.474 | 62.665 |
| d⟨x+y⟩/dp₀ | 399.804 | 14.277 | −38.641 | −36.962 | 215.948 |
| ⟨T_s⟩ (1/λ_c) | 2.60E−04 | 0.009 | 0.032 | 0.013 | 0.130 |
| ⟨T_a⟩ (1/λ_c) | 0.407 | 0.896 | 3.165 | 0.384 | 471.925 |
| λ_c (1/día) | 3.56E−04 | 5.38E−04 | 7.11E−04 | 2.41E−03 | 3.14E−03 |
| ⟨T_s⟩ (días) | 0.731 | 16.151 | 45.242 | 5.204 | 41.450 |
| ⟨T_a⟩ (días) | 1144.198 | 1667.021 | 4453.517 | 159.640 | 150 234.202 |
(w = EPSP por contacto; N = aposiciones cercanas de Fares & Stepanyants; τ = constante de la traza; ξ = amplitud del ruido de la traza; α = escala de tasas de transición; θ = umbral de saturación; λ_i = tasa intrínseca de maduración/encogimiento/poda; R = suma de residuos cuadrados.)

### 4.2 Hallazgos principales
1. **Ajuste a datos:** los modelos reproducen las distribuciones experimentales de número de contactos (Fig. 2 y 3); la conexión L4→L2/3 toma valores de parámetros muy distintos (sus contactos están sobre todo en tallos dendríticos, no en espinas). En las tres, τ es **muy grande** frente a la escala de fluctuación de la actividad (de acuerdo con el supuesto de distribución normal de q) y el rango de τ cabe en la activación sostenida de CaMKII.
2. **Las tasas de maduración y de encogimiento/poda disminuyen con el número de contactos activos:** da estabilidad a largo plazo a las sinapsis establecidas; las tasas son mucho mayores si hay pocos contactos activos y muchos contactos activos **estabilizan el sistema**.
3. Los modelos L4–L4 y L5–L5 muestran semejanzas notables (τ comparable y λ_i baja sin haberlo impuesto a priori). Los contactos **inactivos son raros** (⟨y⟩/⟨x⟩ entre 0 y 0.5); el ajuste conjunto L4–L4/L5–L5 con un solo conjunto de parámetros también es bueno (Fig. 3).
4. **Hebbiano o anti-hebbiano según parámetros:** un modelo es **hebbiano** si d⟨x⟩/dp₀ > 0 (más contactos activos al aumentar los pareamientos causales) y **anti-hebbiano** si < 0; hay buenos ajustes de ambos tipos para cada conjunto (se eligió el mejor sin importar el tipo). Ambos tipos se han observado en neocórtex.
5. **Distribución conjunta (x, y):** x e y fuertemente correlacionados en L4–L4 y L5–L5; la expectativa de x + y está fijada por los datos; la pequeña ⟨y⟩ indica pocas espinas finas. ⟨x⟩ + ⟨y⟩ < ⟨N⟩ ⇒ muchas **sinapsis no realizadas** (aposiciones sin contacto), coherente con los experimentos.
6. **Homeostasis de la tasa dentro del modelo (Fig. 4b):** homeostasis = un aumento de tasa lleva a podar sinapsis de entrada y una caída a madurar sinapsis; en el modelo **d⟨x⟩/dν < 0 equivale a homeostasis**. Por la Ec. 5, un cambio en ν puede aumentar o disminuir μ(x) según p₀; p₀ es **efectivamente un parámetro libre**: dado un conjunto de parámetros, se puede cambiar p₀ a p₀′ sin cambiar las tasas de transición ni las propiedades de equilibrio si se **desplazan los umbrales: θ′ = 2τν(p₀′ − p₀) + θ (Ec. 27)**, porque se conservan las distancias μ(x) − θ. Así el modelo **puede establecer homeostasis de la tasa de disparo** para parámetros apropiados.
7. **Tiempos de vida:** ⟨T_a⟩ supera a ⟨T_i⟩ en **1–2 órdenes de magnitud o más** (varios contactos activos coexisten y se estabilizan mutuamente → tasas λ_m, λ_s, λ_p pequeñas; si un activo pasa a inactivo, la tasa de volver a activo aumenta). Con el λ_c estimado: **inactivos ≈ días; activos de un mes a años** (Holtmaat: transitorias < 8 días, persistentes después) → explicación estadística de **espinas transitorias (contactos inactivos) y persistentes (contactos activos)**.

## 5. Discusión
- Un modelo de plasticidad estructural explica la **formación cooperativa**; la señal local disponible para una espina depende de la correlación pre/post (traza de correlación), posible por fosforilación de **CaMKII**, necesaria para la plasticidad estructural y a largo plazo y quizá para cambios presinápticos. Se asume una traza abstracta, así que los resultados no dependen del mecanismo específico. La traza «olvidadiza» integra eventos causales y anti-causales como un integrador con fuga; su constante afecta la posición y varianza de la distribución de equilibrio; es comparable entre L4–L4 y L5–L5 y observable en experimentos si la traza es el ciclo de expresión/activación/degradación de CaMKII.
- La dependencia funcional de las tasas se eligió **versátil (Ec. 7)** porque no se conoce una descripción cuantitativa; los resultados muestran **selectividad fuerte** por números específicos de contactos activos: tasas mucho mayores con pocos contactos y estabilización con muchos; experimentos futuros podrían medir si el número de contactos (o amplitud EPSP) correlaciona con transitorios de calcio y tasas de maduración, encogimiento y poda.
- Modelos previos suponían **homeostasis de la tasa** (si la actividad sube por encima de un punto fijado a priori se podan contactos; lo inverso por debajo); el modelo dependiente de correlaciones (Helias et al.) lo muestra; aquí se calcula cómo cambia el número esperado de contactos activos con la tasa y esa dependencia puede elegirse arbitrariamente ajustando un parámetro libre (Fig. 4b).
- Con las fuentes de ruido y amplitud sináptica constante: una dispersión de amplitudes cambiaría la dependencia de media y varianza de q con x, pero la media seguiría creciendo monótonamente con x; en población añade ancho a la distribución de q (parte del ruido η representaría esa contribución) y reduce la precisión de la detección de correlación; se esperan ajustes cualitativamente similares con ruido adicional menor.
- **Estados discretos** (no realizado/inactivo/activo): técnicamente similar al modelo de sinapsis en cascada de Fusi et al. pero con interpretación morfológica; el contacto inactivo podría relacionarse con sinapsis silenciosas, aunque en el sistema biológico probablemente no haya una distinción tan nítida; Busetto et al. vieron muchas sinapsis silenciosas en el animal en desarrollo que desaparecen en el adulto; análisis cuántico en el neocórtex adulto muestra que casi todos los contactos de L4→L2/3 son funcionales (el modelo de esta conexión tampoco da contactos inactivos en expectativa, así que son inobservables); las espinas pequeñas son difíciles de ver (menores que el límite de resolución óptica) y pueden podarse rápido.
- **Inactivo = NMDA**: la conductancia NMDA aumenta con la despolarización postsináptica al retirarse el bloqueo de magnesio; la activación NMDA es mucho más lenta que AMPA: un PA postsináptico causado parcialmente por corrientes NMDA de un contacto ocurriría mucho después de la liberación presináptica; por eso los NMDA contribuyen poco a la traza y tienen impacto despreciable en la plasticidad cooperativa (término «inactivo» en sentido **funcional**). Sinapsis presinápticamente silenciosas (baja probabilidad de liberación) también permiten formar una traza.
- **Alcance:** plasticidad estructural abarca fenómenos no tratados (competencia entre sinapsis de neuronas distintas, migración de axones en escalas más largas); este modelo describe el **estado estacionario de la corteza adulta** (espinas se forman y retraen con arborización axonal constante); en lesiones el estado estacionario puede volverse inestable y los axones migran de nuevo. Modelos más detallados basados en CaMKII (Helias et al.; Deger/otros) incluyen necesariamente cooperación y competencia entre contactos.
- **Conclusión:** el modelo, aunque simple y abstracto, explica la cooperación de contactos postulada por Fares & Stepanyants; la **regla de aprendizaje es local** (requiere solo mecanismos en los contactos sinápticos) y aun así explica la formación cooperativa.

## 6. Limitaciones declaradas
Sinapsis independientes entre pares (sin competencia entre sinapsis de distintas neuronas); una sola amplitud EPSP por contacto activo; estado estacionario del adulto (sin cambios de arborización); modelo lineal p(x) sin saturación; los parámetros ajustados no son únicos (varios mínimos); falta evidencia experimental directa para las funciones de tasa.

## 7. Referencias clave citadas
Fares & Stepanyants 2009 (*PNAS* 106:16463); Holtmaat et al. 2005 (*Neuron* 45:279); Yasumatsu et al. 2008 (*J. Neurosci.* 28:13592); Kasai et al. 2010; Helias, Rotter, Gewaltig & Diesmann 2008 (*Front. Comput. Neurosci.* 2:7); Helias, Deger, Rotter & Diesmann 2010 (*PLoS CB* 6:e1000929); Feldmeyer et al. 1999, 2002; Markram et al. 1997; Lisman, Yasuda & Raghavachari 2012 (*Nat Rev Neurosci* 13:169); Brunel 2000; Chklovskii, Mel & Svoboda 2004 (*Nature* 431:782); Knoblauch, Palm & Sommer 2010; Butz, Wörgötter & van Ooyen 2009; van Ooyen et al. 1995; Dammasch, Wagner & Wolff 1986.

## 8. Relevancia para E20 (interpretación, no del artículo)
- Da una definición operativa de **traza de correlación causal/anti-causal** con constante larga (τν ≫ 1): útil para `activity_ij` y para la señal pre→post de la especificación del usuario.
- Muestra que la **misma** regla estructural puede ser **hebbiana o anti-hebbiana** según el signo de d⟨x⟩/dp₀ y que la **homeostasis** exige d⟨x⟩/dν < 0 (se ajusta con p₀ y la Ec. 27): el signo es un **parámetro de diseño**; para estabilidad se necesita el signo negativo, coherente con Gallinaro & Rotter y Butz & van Ooyen.
- La cooperación entre contactos y la estabilización de los activos dan **persistencia estructural**; la teoría es de **equilibrio**, no de predicción; el análisis de tiempos de vida y la calibración vía TOR sugieren cómo fijar la escala temporal con un dato externo.

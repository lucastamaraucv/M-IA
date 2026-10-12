# 00 — SÍNTESIS: plasticidad estructural (4 artículos) aplicada a E20
Fecha: 2026-10-02. Fuentes: `Associative properties of structural plasticity based on firing rate homeostasis in recurrent neuronal networks.md`, `Spike-Timing Dependence of Structural Plasticity Explains Cooperative Synapse Formation in the Neocortex.md`, `Formation and Maintenance of Robust Long-Term Information Storage in the Presence of Synaptic Turnover.md`, `A Simple Rule for Dendritic Spine and Axonal Bouton Formation Can Account for Cortical Reorganization after Focal Retinal Lesions.md` (cada una con sus ecuaciones, parámetros y ⚠ de verificación). Lo marcado **[derivación propia]** o **[interpretación]** es mío, no de los artículos.

## 1. Lo más importante que enseñan los cuatro artículos (en simple)
1. **Hay dos familias de plasticidad estructural** (clasificación de Fauth & Tetzlaff 2016, citada por Gallinaro & Rotter): **hebbiana** (más sinapsis cuando hay **más** actividad/correlación) y **homeostática** (más sinapsis cuando hay **menos** actividad que el objetivo; menos cuando hay más). La primera es retroalimentación **positiva** (se desboca); la segunda, **negativa** (se estabiliza).
2. **Mis pruebas fallidas (Rsp/Rgrow) y la especificación del usuario son de la familia hebbiana:** crean conexiones por coactivación/cercanía temporal (α·x_i·x_j + β·e^{−|Δt|/τ}); la homeostasis de la especificación es de **grado** (k_target), no de **tasa**. Los artículos explican por qué la actividad **se duplicó** (0.22 → 0.42–0.50): es el comportamiento esperado de la retroalimentación positiva.
3. **Gallinaro & Rotter y Butz & van Ooyen** muestran que una regla **homeostática de tasa**, sin mirar correlaciones, **hace crecer la red desde cero hasta una conectividad estable (~10 %)** y que las propiedades asociativas hebbianas **emergen** del emparejamiento aleatorio de elementos libres.
4. **Butz & van Ooyen** añaden una **actividad mínima** para crecer (η) además del punto homeostático (ε): fuera de [η, ε] se retrae; η_A (axones) alto y η_D (dendritas) bajo da reparación secuencial; ambos bajos → recurrencia masiva y **sincronía/oscilaciones** (modo de fallo a vigilar).
5. **Deger et al.** definen la **traza de correlación causal/anti-causal** q(t) con τ largo y muestran que el mismo modelo puede ser hebbiano o anti-hebbiano: **el signo de d⟨x⟩/dν** decide si hay homeostasis (negativo) o no.
6. **Fauth et al.** dan el marco exacto para **fijar de antemano la distribución de grado**: d_I[S] = ((N−S+1)/S)·(p_I[S−1]/p_I[S])·b (equilibrio detallado) y muestran que la **biestabilidad** da memoria estructural duradera con aprendizaje mucho más rápido que el olvido (a costa de 1 bit por conexión).
7. **Ninguno** de los artículos conecta la estructura con el **rendimiento predictivo** de una tarea; son modelos de estabilidad, memoria de conectividad y reorganización.

## 2. Mapa: especificación del usuario ↔ literatura
| Pieza de la especificación | Equivalente en los artículos | Comentario |
|---|---|---|
| P_form = σ(α x_i x_j + β e^{−|Δt|/τ_form} + γ S_ij − θ_i) | Deger: traza de correlación q(t) (causal/anti-causal), tasa de transición k(μ) | Es de tipo hebbiano; con θ_i de grado no hay freno de tasa. |
| θ_i = θ_base + η(k_i − k_target) (homeostasis de grado) | Gallinaro/Butz: homeostasis de **tasa** vía elementos z_i (dz/dt = −(r_i − ρ)/β en Gallinaro) | La literatura estabiliza con **tasa**, no con grado. |
| P_delete = σ(θ_delete − U_ij) por utilidad | Gallinaro/Butz: eliminación **aleatoria** entre elementos al perder z; Deger: poda dependiente de la correlación y de la cooperación entre contactos | La utilidad por peso/actividad es propia de la especificación. |
| S_ij similitud de neuronas | Butz: kernel de distancia K_ij = exp(−d²/σ²); Gallinaro: no usa kernel | Análogo posible: kernel de similitud de entrada. |
| STDP simultáneo | Deger: la correlación guía la estructura; Gallinaro/Butz: **sin STDP** (solo estructura) | Gallinaro/Butz muestran que la estructura sola ya reproduce asociación y remapeo. |
| «Probabilidad en cada par y paso» | Gallinaro/Butz: **elementos libres emparejados al azar**; el número de sinapsis nuevas lo limita el número de elementos libres | Resuelve el problema de «se crean demasiadas conexiones». |

## 3. Algoritmo propuesto: HSP-E20 (estructural homeostático de tasa) — combina Gallinaro/Butz con la especificación
Pseudocódigo (**[interpretación]**, a probar):
```
Para cada neurona excitatoria i (solo E→E y E→I plásticas; I→* fijas, como Gallinaro):
    r_i(t) = tasa filtrada:  τ_r dr_i/dt = −r_i + s_i(t)           (Gallinaro Ec. 2; o calcio de Butz Ec. 3)
    z_i^k(t+1) = z_i^k(t) − (1/β)(r_i − ρ_i)·Δt,  k ∈ {pre, post}  (Gallinaro Ec. 3, lineal; ρ = tasa objetivo, β = crecimiento)
         o bien dz/dt = ν(2 exp(−((r−ξ)/ζ)²) − 1), ξ=(η+ε)/2, ζ=(ε−η)/(2√ln2)   (Butz Ec. 4, con actividad mínima η)
Cada K pasos (conectividad):
    Si z_i^k < 0: eliminar |z| sinapsis al azar entre las existentes de i (elementos complementarios quedan libres)
    Si z_i^k > 0: i aporta z elementos libres
    Emparejar al azar todos los elementos libres pre con post de TODA la red (cualquier par i→j, sin restricción de distancia);
        opcional: ponderar la probabilidad del par por un kernel K_ij (similitud S_ij)
    Sinapsis nuevas con peso w_init (ley de Dale por la presináptica)
```
Propiedades esperadas según los artículos: la tasa de cada neurona converge a ε; la densidad converge sola; las correlaciones se evalúan **implícitamente** (hebbiana emergente); la asociación persiste; velocidad de crecimiento ∝ ν.

## 4. Ecuaciones útiles verificadas en los artículos
- Tasa filtrada y crecimiento lineal: τ_r ṙ = −r + s; ż = −(r − ρ)/β, con ρ = tasa objetivo y β = parámetro de crecimiento. (Gallinaro 2018, Ec. 2–3 ✔)
- Curva gaussiana con mínimo y punto homeostático: ż = ν(2e^{−((Ca−ξ)/ζ)²} − 1). (Butz & van Ooyen 2013, Ec. 4)
- Pérdida esperada de sinapsis al borrar elementos: ΔC⁻_ij = C_ij·ΔD_i/D_i; ΔC⁻_ij = C_ij·ΔA_j/A_j. (Butz 2013, Ec. 6–7)
- Traza de correlación: q̇ = −q/τ + g(t)s(t) + η; μ = τν(2p−1); σ² = ½(τν + ξ²). (Deger 2012, Ec. 1–3)
- Homeostasis dentro del modelo de Deger: d⟨x⟩/dν < 0; desplazamiento de umbral h' = 2τν(p₀'−p₀)+h. (Ec. 27)
- Eliminación por equilibrio detallado: d_I[S] = ((N−S+1)/S)(p_I[S−1]/p_I[S])·b. (Fauth 2015, Ec. 4)

## 5. Derivaciones propias (no de los artículos) para el diseño
1. **Estabilidad de la regla de integral discreta** [derivación propia; en la notación de Gallinaro ε = ρ y ν = β]. Con ε fija y ganancia de bucle g = ∂r/∂z > 0 (más elementos → más sinapsis → más tasa), la actualización z ← z − (r−ε)Δt/ν se linealiza como e ← (1 − gΔt/ν)·e, estable si **0 < gΔt/ν < 2** y sin oscilación si < 1. Sirve para acotar ν frente a Δt (coherente con la advertencia de Gallinaro: «hacerlo más rápido puede desestabilizar»).
2. **Grado esperado de la regla de la especificación** [derivación propia]. Con M pares candidatos, tasa de formación media p_f por par y tasa de eliminación media d por sinapsis: dk/dt = (M − k)·p_f − k·d ⇒ **k\* = M·p_f/(p_f + d)**; para densidad objetivo ρ = k\*/M se fija **p_f/d = ρ/(1−ρ)** (p. ej., ρ = 0.1 ⇒ p_f = d/9). Es la ecuación para fijar la «tasa de creación que mantiene la densidad objetivo». Con elementos libres (Gallinaro/Butz) el número de creaciones lo fija z, no p_f.
3. **Condición de eco (ESP)** — los artículos **no** la tratan; queda como hueco (ver prompt de investigación): hay que acotar el radio espectral de W durante la estructura cambiante, p. ej. normalizando la fuerza de entrada total de cada neurona.

## 6. Parámetros de partida con fuente (adaptar a paso diario)
| Parámetro | Valor en el artículo | Fuente | Propuesta E20 (decisión de diseño) |
|---|---|---|---|
| τ_r (tasa filtrada) | 10 s | Gallinaro | 20–60 pasos |
| Δt de reconexión | 100 ms (Δt/τ_r = 1/100) | Gallinaro/Butz | cada 5–10 pasos (Δt/τ_r ≈ 0.1–0.25, más rápido que el artículo por tener series cortas; vigilar la estabilidad con la condición g·Δt/β < 1) |
| β (crecimiento, Gallinaro) / ν (Butz) | β ∈ {0.2, 0.625, **2**, 6.25, 20} (lineal) · ν = 10⁻⁴ ms⁻¹ (Butz) | Gallinaro/Butz | fijar en desarrollo; τ_growth = γ·β (γ ≈ 130–240 s según ρ) |
| ρ (objetivo de tasa, Gallinaro) / ε (punto homeostático, Butz) | ρ = 8 Hz (5–9 Hz probados) · ε = Ca 0.7 | ambos | tasa de A0 ≈ 0.22–0.25 |
| η (actividad mínima) | η_D = 0.1, η_A = 0.4 (Butz; η_A > η_D) | Butz | η_D ≈ 0.4ε, η_A ≈ 0.6ε (heurística, a validar en desarrollo) |
| τ_vac (decaimiento de elementos libres) | 10 actualizaciones | Butz | 10 actualizaciones |
| Densidad objetivo | ≈ 10 % (grado ≈ 1000/10000) | Gallinaro | 10 % (la de E20) |
| Peso nuevo | fijo J | Gallinaro/Butz | w_init de la matriz inicial |
| STDP/traza de correlación (si se usa) | τ larga, τν ≫ 1 | Deger | τ_q ≈ 5–20 pasos |

## 7. Qué cambia en los planes del repositorio
1. En `plans/PLAN_E20_PLASTICIDAD_ESTRUCTURAL_COMPLETA_v1.md`, el brazo **D+** (homeostasis de **tasa**) deja de ser una «extensión de diagnóstico» y pasa a ser el **brazo principal HSP** (Gallinaro/Butz); el brazo **D** de la especificación (hebbiano + grado) se mantiene como **control de la familia hebbiana**, con la predicción explícita (por la literatura) de que **duplicará la tasa**.
2. Nuevas hipótesis falsables: **HS-a** la tasa de HSP se mantiene en ε ± 20 % mientras D la duplica; **HS-b** HSP mantiene el rendimiento de A0 con la misma o menor densidad; **HS-c** HSP crece desde cero hasta la densidad objetivo sin intervención.
3. Huecos que persisten tras leer los artículos (deben ir al prompt de investigación): condición de estabilidad ESP con estructura cambiante; criterio de creación **ligado a la predicción** (ninguno de los cuatro lo trata); adaptación a paso diario (solo hay mapeo por razones Δt/τ_r).

## 8. Advertencias de honestidad
- Los cuatro son modelos de **neurociencia** con neuronas LIF/Izhikevich y escalas de ms–s; la traducción a un reservorio con paso diario es **mía** y debe validarse.
- No hay evidencia en estos artículos de que la plasticidad estructural **mejore la predicción**; el criterio para decidir sigue siendo el experimental de este proyecto (9 pasos, controles RAND/ANTI, series nunca vistas).
- Las ecuaciones marcadas ⚠ en cada ficha salieron desordenadas del PDF y deben contrastarse con el original antes de citarlas en la tesis.

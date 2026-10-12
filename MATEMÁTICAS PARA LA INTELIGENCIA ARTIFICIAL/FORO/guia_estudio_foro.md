# Guía de Estudio — Foro Cadenas de Markov
> Lee esto antes de revisar las respuestas del foro. Cada concepto explicado simple.

---

## 1. Proceso estocástico — qué es en palabras normales

**Determinista** = puedes predecir el futuro con certeza.
Ejemplo: si sueltas una pelota desde 10m de altura, sabes exactamente cuándo toca el suelo.

**Estocástico** = el futuro tiene aleatoriedad. No sabes qué va a pasar, solo sabes *cuán probable* es cada cosa.
Ejemplo: el precio de BTC mañana, si va a llover, cuántos clientes llegan a una tienda.

Un **proceso estocástico** es simplemente una secuencia de estas variables aleatorias a lo largo del tiempo:
```
X_0, X_1, X_2, X_3, ...
```
Cada X_t es una variable aleatoria. El subíndice t es el tiempo.

**Los 4 tipos importantes:**

```
                 ESPACIO DE ESTADOS
                 Discreto          Continuo
TIEMPO   ┌────────────────────────────────────────┐
Discreto │ Cadena de Markov  │  Serie temporal    │
         │ (clima, tablero)  │  (BTC precio diario│
         ├───────────────────┼────────────────────┤
Continuo │ Proceso Poisson   │  Brownian Motion   │
         │ (llegada clientes)│  (base de DALL-E)  │
         └────────────────────────────────────────┘
```

**Discreto** = los estados son contables: {Soleado, Nublado, Lluvioso}, {0,1,2,3...}
**Continuo** = los estados son números reales: precio, temperatura, voltaje

---

## 2. Cadenas de Markov — la propiedad sin memoria

Una cadena de Markov es un proceso estocástico con estados discretos que tiene una propiedad especial llamada **propiedad de Markov** o "sin memoria":

> **El futuro solo depende del estado ACTUAL. No del historial.**

**Ejemplo concreto con el clima:**

❌ Con memoria (NO es Markov):
"Si ayer llovió Y hoy está nublado → mañana hay 80% de probabilidad de lluvia"

✅ Sin memoria (SÍ es Markov):
"Si hoy está nublado → mañana hay 30% de probabilidad de lluvia"
(no importa lo que pasó ayer, ni antes de ayer)

**Formalmente:**
```
P(X_{n+1} = j | X_n = i, X_{n-1}, X_{n-2}, ...) = P(X_{n+1} = j | X_n = i)
```

Lo que está a la derecha del | es la condición (lo que ya sabes).
La propiedad dice: da igual cuánto historial tengas, solo importa X_n (el estado actual).

---

## 3. Matriz de transición — cómo leerla

La matriz de transición P guarda todas las probabilidades de pasar de un estado a otro.

**Para el modelo del clima** con 3 estados (Soleado=S, Nublado=N, Lluvioso=L):

```
        ¿A dónde voy MAÑANA?
          S     N     L
     S [ 0.2   0.5   0.3 ]   ← si hoy es Soleado
     N [ 0.1   0.6   0.3 ]   ← si hoy es Nublado
     L [ 0.5   0.3   0.2 ]   ← si hoy es Lluvioso
¿Dónde
estoy HOY?
```

**Cómo leerla:**
- Fila = estado de HOY
- Columna = estado de MAÑANA
- p_ij = P(mañana = j | hoy = i)

Ejemplo: p_12 = 0.5 → si hoy es Soleado, mañana hay 50% de probabilidad de Nublado.

**Las dos condiciones para que sea válida:**
1. Todos los valores ≥ 0 (son probabilidades, no pueden ser negativas)
2. Cada FILA suma exactamente 1 (desde cualquier estado, tienes que ir a algún lado)

**Por qué la matriz Q del foro NO es válida:**
```
Q = | 0.2   0.5   0.4 |   ← fila 1 suma 1.1 ≠ 1  ✗
    | 0.1   0.5   0.3 |   ← fila 2 suma 0.9 ≠ 1  ✗
    | 0.7   0.5  -0.2 |   ← tiene -0.2 < 0        ✗
```

---

## 4. Vector de estado — qué significa

El vector de estado v_n = (p1, p2, p3) te dice:
**"¿cuál es la probabilidad de estar en cada estado en el instante n?"**

No te dice DÓNDE está el sistema. Te dice cuán probable es cada posibilidad.

**Ejemplo:**
```
v_0 = (0.75, 0.20, 0.05)

Significa: hoy hay 75% de prob de que esté Soleado,
                   20% de prob de que esté Nublado,
                    5% de prob de que esté Lluvioso
```

**Condiciones para ser válido:**
- Todas las componentes ≥ 0
- La suma = 1 (es una distribución de probabilidad)

**Por qué u_0=(0.3, 0.6, 0.7) NO es válido:** suma = 1.6 ≠ 1

---

## 5. Cómo calcular el estado de mañana — multiplicación v · P

**La regla:** v_{n+1} = v_n · P

**Cómo funciona la multiplicación:**

Para calcular P(Soleado mañana), miro todas las formas de llegar a Soleado:
```
P(Sol mañana) = P(Sol hoy) × P(Sol→Sol)
              + P(Nub hoy) × P(Nub→Sol)
              + P(Llu hoy) × P(Llu→Sol)

= 0.75 × 0.2  +  0.20 × 0.1  +  0.05 × 0.5
=  0.150      +   0.020       +   0.025
=  0.195
```

Esto es la primera componente de v_0 · P.
Lo mismo para Nublado y Lluvioso → v_1 = (0.195, 0.510, 0.295)

**Intuición:** cada estado de mañana "recibe" probabilidad de todos los estados de hoy, ponderada por la probabilidad de la transición.

**Para calcular v_2:** aplicas la misma operación a v_1:
```
v_2 = v_1 · P = (0.2375, 0.4920, 0.2705)
v_3 = v_2 · P = (0.2320, 0.4951, 0.2730)
```

Observa que la distribución se estabiliza rápido a pesar de que v_0 = (0.75, 0.20, 0.05) era muy extrema.

---

## 6. Estado estacionario — la distribución de largo plazo

**Qué es:** una distribución π que no cambia cuando le aplicas P.
```
Si empiezas con π → después de un paso sigues teniendo π
π · P = π
```

**Por qué existe:** si la cadena es ergódica (puedes ir de cualquier estado a cualquier otro), matemáticamente se garantiza que existe un único punto de equilibrio.

**Qué significa en la práctica:**
- Sin importar cómo empiece el sistema, eventualmente la distribución converge a π
- π_i = fracción del tiempo que el sistema pasa en el estado i a largo plazo

**Cómo calcularlo — paso a paso simple:**

Quiero π = (π_1, π_2, π_3) tal que π · P = π

Esto me da el sistema:
```
π_1 = 0.2·π_1 + 0.1·π_2 + 0.5·π_3   ← columna 1 de P
π_2 = 0.5·π_1 + 0.6·π_2 + 0.3·π_3   ← columna 2 de P
π_3 = 0.3·π_1 + 0.3·π_2 + 0.2·π_3   ← columna 3 de P
```

Reordeno (paso π al lado derecho):
```
(I)   -0.8·π_1 + 0.1·π_2 + 0.5·π_3 = 0
(II)   0.5·π_1 - 0.4·π_2 + 0.3·π_3 = 0
      + la condición: π_1 + π_2 + π_3 = 1
```

(Una ecuación es redundante, la reemplazo por la condición de normalización.)

**Resolución:**

De (I): π_2 = (0.8·π_1 - 0.5·π_3) / 0.1 = **8·π_1 - 5·π_3**

Sustituyo en (II):
```
0.5·π_1 - 0.4·(8·π_1 - 5·π_3) + 0.3·π_3 = 0
0.5·π_1 - 3.2·π_1 + 2·π_3 + 0.3·π_3 = 0
-2.7·π_1 + 2.3·π_3 = 0
→ π_3 = (2.7/2.3)·π_1 = (27/23)·π_1
```

Sustituyo π_3 en la expresión de π_2:
```
π_2 = 8·π_1 - 5·(27/23)·π_1 = (184 - 135)/23 · π_1 = (49/23)·π_1
```

Uso π_1 + π_2 + π_3 = 1:
```
π_1 + (49/23)·π_1 + (27/23)·π_1 = 1
(23 + 49 + 27)/23 · π_1 = 1
99/23 · π_1 = 1
→ π_1 = 23/99 ≈ 0.2323
   π_2 = 49/99 ≈ 0.4949
   π_3 = 27/99 ≈ 0.2727
```

**Verificación rápida:** 23+49+27 = 99 ✓ y 0.2323+0.4949+0.2727 = 1.000 ✓

**Observa la convergencia:**
```
v_0 = (0.7500, 0.2000, 0.0500)  ← empezamos casi todo soleado
v_1 = (0.1950, 0.5100, 0.2950)
v_2 = (0.2375, 0.4920, 0.2705)
v_3 = (0.2320, 0.4951, 0.2730)
π  = (0.2323, 0.4949, 0.2727)  ← límite al que converge
```

En solo 3 pasos ya estamos a menos de 0.001 del equilibrio.
La cadena "olvidó" que empezó con 75% de sol.

---

## 7. Pregunta 4 — por qué nadie puede producir ese vector

La pregunta es: ¿qué v produce (0.75, 0.20, 0.05) al día siguiente?

Resuelvo el sistema y obtengo x = (-3.5, 2.0, 2.5).
Matemáticamente funciona: x · P = (0.75, 0.20, 0.05). ✓
Pero x_1 = -3.5 < 0 → **no es una distribución de probabilidad válida**. ✗

**La razón de fondo (más importante que el algebra):**

La columna de Soleado en P es (0.2, 0.1, 0.5). Para maximizar P(Soleado mañana):
```
P(Sol mañana) = 0.2·x_1 + 0.1·x_2 + 0.5·x_3

El coeficiente más grande es 0.5 (desde Lluvioso).
Lo mejor que puedo hacer: poner todo el peso en x_3=1 → P(Sol mañana) = 0.5
```

El target es 0.75, pero el **máximo posible con esta P es 0.5**.
No importa de dónde partas: con esta matriz, es imposible tener más de 50% de probabilidad de que mañana sea Soleado.

---

## 8. MDPs — la extensión al Reinforcement Learning

La cadena de Markov modela un sistema que evoluciona solo.
Un MDP agrega **decisiones** y **recompensas**:

```
Cadena de Markov:
  estado → (P aleatoria) → siguiente estado

MDP:
  estado + ACCIÓN → (P aleatoria) → siguiente estado + RECOMPENSA
```

El agente aprende qué acción tomar en cada estado para maximizar la recompensa acumulada.

Ejemplo trading:
- Estado: precio actual + indicadores
- Acciones: comprar / vender / hold
- Recompensa: PnL realizado
- El agente aprende la política óptima de trading

Q-learning, DQN, PPO, SAC son todos algoritmos para resolver MDPs.

---

## 9. Paper de tensores — 3 ideas clave

**Problema que resuelve:**
PyTorch/TensorFlow son muy rápidos para gradientes (derivadas de funciones escalares → backprop normal). Pero para Hessianos (derivadas de segundo orden, matrices de derivadas) son 1000x más lentos.

**Por qué importa el Hessiano:**
El gradiente te dice *qué dirección bajar*. El Hessiano te dice *cuánto bajar en cada dirección*. Con Hessiano puedes dar pasos más inteligentes (optimizadores de segundo orden: Newton, K-FAC).

**Las 3 contribuciones del paper:**

1. **Operador unificado:** define una sola operación que cubre producto interno, externo y Hadamard. Compatible con notación de numpy/PyTorch (notación Einstein).

2. **Cross-country mode:** combina forward y reverse pass de forma inteligente → ~30% más rápido para Hessianos.

3. **Compresión:** en vez de calcular un tensor de orden 4 (que es enorme), lo comprime a una matriz pequeña. Resultado: 1 segundo → 10 microsegundos (factor 100,000x).

**Conclusión:** antes de este paper, calcular Hessianos de redes neuronales era computacionalmente imposible. Ahora es factible.

---

## Resumen rápido — lo que necesitas recordar

| Concepto | En una línea |
|----------|-------------|
| Proceso estocástico | Secuencia de variables aleatorias a lo largo del tiempo |
| Markov property | El futuro solo depende del estado actual, no del historial |
| Matriz estocástica | Tabla de probabilidades de transición; cada fila suma 1 |
| Vector de estado | Distribución de probabilidad sobre los estados en el instante n |
| Evolución | v_{n+1} = v_n · P |
| Estado estacionario | π tal que π · P = π; equilibrio de largo plazo |
| MDP | Cadena de Markov + acciones + recompensas = Reinforcement Learning |

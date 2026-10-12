# Cómo funciona la Actividad 1 — Explicación paso a paso para estudiar

Este documento **no es un entregable** (no se sube a la plataforma). Es una
explicación pensada para que entiendas, punto por punto, *por qué* la
solución que está en `subir/` es correcta y *cómo* se construyó — útil de
cara al examen o a defender la actividad si el profesor pregunta.

Sigue exactamente los 5 puntos del enunciado (`instrucciones.txt`), en el
mismo orden que la memoria (`Actividad1_TamaraTrejo_Lucas.pdf` en `subir/`).

---

## Punto 0 — El problema de fondo: ¿por qué lógica borrosa?

La lógica clásica (booleana) solo admite verdadero/falso. Un sistema
experto clásico con la regla "si RSI < 30, comprar" trata exactamente
igual un RSI de 29.9 (comprar) que uno de 30.1 (no comprar) — un salto
brusco e injustificado para una diferencia mínima.

La **lógica borrosa** (fuzzy logic) sustituye "pertenece / no pertenece"
por un **grado de pertenencia** entre 0 y 1. Así, RSI=29 puede ser
"sobrevendido" con grado 0.95 y RSI=32 con grado 0.6 — una transición
suave, más parecida a como razona una persona.

Un **sistema de reglas de producción con razonamiento aproximado** es
justo eso: un motor de inferencia (como CLIPS) que encadena reglas
SI-ENTONCES, pero donde tanto los hechos como las conclusiones tienen
grados de verdad borrosos en vez de ser solo verdadero/falso.

---

## Punto 1 — Dominio, objetivo, alcance, límites

**Qué pide el profesor:** elegir un dominio libre y justificar brevemente
por qué un sistema borroso aporta algo ahí.

**Qué se eligió:** un asesor de señales de trading de Bitcoin, con 2
entradas (RSI y Volatilidad) y 1 salida (Señal, de -10 a +10).

**Por qué funciona como ejemplo de razonamiento aproximado:** los
indicadores técnicos (RSI, volatilidad) son exactamente el tipo de
variable donde los umbrales rígidos son artificiales — no hay una frontera
mágica entre "sobrevendido" y "neutral" en RSI=30 exacto. Es un dominio
donde la imprecisión es inherente al problema, no forzada para el
ejercicio.

**Lo que hay que poder explicar si preguntan:** que el sistema es de
*apoyo* (no ejecuta órdenes) y que los parámetros de las funciones de
pertenencia son ilustrativos, no calibrados con datos reales.

---

## Punto 2 — Las 7 reglas (base de conocimiento)

```
R1: SI RSI=sobrevendido    Y Volatilidad=baja   ENTONCES Señal=comprar_fuerte
R2: SI RSI=sobrevendido    Y Volatilidad=alta   ENTONCES Señal=comprar
R3: SI RSI=neutral                              ENTONCES Señal=mantener
R4: SI RSI=sobrecomprado   Y Volatilidad=baja   ENTONCES Señal=vender_fuerte
R5: SI RSI=sobrecomprado   Y Volatilidad=alta   ENTONCES Señal=vender
R6: SI RSI=sobrevendido    Y Volatilidad=media  ENTONCES Señal=comprar
R7: SI RSI=sobrecomprado   Y Volatilidad=media  ENTONCES Señal=vender
```

**Por qué 7 y no 5:** el enunciado dice "alrededor de 5", así que 7 es
válido. Con solo R1–R5 la etiqueta *media* no se usaba en ninguna regla, y
había entradas sin respuesta: con RSI=20 y Volatilidad=10, baja(10)=0,
alta(10)=0 y neutral(20)=0, así que ninguna regla disparaba (lo
comprobaste tú en FuzzyCLIPS: no apareció ningún hecho SENAL). Con R6/R7
**cualquier entrada dispara al menos una regla**:
- si neutral(RSI) > 0 → dispara R3;
- si no, el RSI es ≤30 o ≥70, así que sobrevendido o sobrecomprado vale 1,
  y en todo [0,20] alguna etiqueta de volatilidad (baja, media o alta) es
  mayor que 0 → dispara R1/R2/R6 o R4/R5/R7.

**Concepto clave — "razonamiento hacia delante" (forward chaining):**
partes de los **hechos** (lo que observas: RSI=35, Volatilidad=8) y vas
disparando las reglas cuyo antecedente casa con esos hechos, generando
**nuevos hechos** (la conclusión). Es lo opuesto al razonamiento hacia
atrás (backward chaining), que parte de un objetivo y busca qué reglas lo
probarían.

En CLIPS esto lo hace el algoritmo **RETE**: mantiene una red de
"coincidencias parciales" para no tener que re-evaluar todas las reglas
contra todos los hechos cada vez — es la razón de que CLIPS sea un motor
de inferencia de verdad, y no solo una función matemática.

**Por qué la estructura es simétrica (R1↔R4, R2↔R5, R6↔R7):** solo con
volatilidad baja se da una señal "fuerte"; con volatilidad media o alta la
señal se modera — así se demuestra que las reglas capturan una heurística
de trading real (más cautela cuando hay más ruido), no solo una tabla
arbitraria.

---

## Punto 3 — MPG con universo NO continuo (relaciones borrosas)

Esta es la parte más teórica. Vamos despacio.

### 3.1 — Conjunto borroso discreto
Un conjunto borroso sobre un universo discreto es una lista de pares
(elemento, grado):
```
A = "RSI sobrevendido" = 1/20 + 0.2/50 + 0/80
```
Se lee: "el elemento 20 pertenece a *sobrevendido* con grado 1; el 50 con
grado 0.2; el 80 con grado 0".

### 3.2 — T-norma (para combinar antecedentes)
Cuando una regla tiene 2 antecedentes ("RSI sobrevendido **Y** Volatilidad
baja"), hay que combinar sus grados con un operador AND borroso: la
**t-norma**. La más simple y la que se usa en el curso es el **mínimo**:
```
(A×C)(x,z) = min(A(x), C(z))
```
Esto reemplaza el AND booleano clásico.

### 3.3 — Implicación borrosa (para construir la regla como relación)
La regla "SI A ENTONCES B" se convierte en una **relación borrosa**
`R(x,y)` sobre el producto de universos X×Y, usando una función de
**implicación** `I(a,b)`. Se eligió **Lukasiewicz**:
```
I(a,b) = min(1, 1-a+b)
```
¿Por qué esta y no otra? Porque es a la vez S-implicación y R-implicación
(las dos grandes familias de implicaciones borrosas), lo que la hace una
elección "segura" y muy citada en los cursos de lógica borrosa.

`R(x,y) = I(A(x), B(y))` — se calcula para cada combinación de x (o de
(x,z) si hay 2 antecedentes) con cada y del universo de salida. Es
literalmente una tabla (matriz).

### 3.4 — Modus Ponens Generalizado (MPG)
El Modus Ponens clásico dice: "si sabes A, y sabes que A→B, entonces
sabes B". El **Generalizado** hace lo mismo pero con observaciones
imprecisas: no observas A exactamente, sino algo parecido, A' (p. ej. "RSI
ronda 20-25" en vez de "RSI=20 exacto").

La fórmula general es una composición **sup-T** (T = una t-norma):
```
B'(y) = sup_(x,z) T[(A'×C')(x,z), R((x,z),y)]
```
Para cada y, miras todas las celdas, combinas lo observado con la relación
usando la t-norma T, y te quedas con el máximo (sup).

**Qué t-norma se eligió para componer: la de Lukasiewicz**
```
T_L(a,b) = max(0, a+b-1)
```
Por eso el enunciado habla de "t-normas" en plural: en la memoria se usan
**dos t-normas distintas**, cada una en su papel:
- **mínimo** → para el AND de los antecedentes;
- **T_L (Lukasiewicz)** → para la composición del MPG.

**Por qué T_L y no el mínimo (la pregunta clave si te la hacen):** la
implicación de Lukasiewicz es el *residuo* de T_L, y esa pareja cumple la
propiedad básica del Modus Ponens: **si la observación es igual al
antecedente (A'=A, C'=C), la conclusión sale exactamente igual a B**.
Con sup-min no se cumple. Compruébalo con la celda (20,8), para y=-10
(donde B=0): A×C=0.4 y R=0.6.
- sup-min: min(0.4, 0.6) = **0.4** → B'(-10)=0.4 ≠ B(-10)=0 ✗
- sup-T_L: max(0, 0.4+0.6−1) = **0** → B'(-10)=0 = B(-10) ✓

### 3.5 — El resultado en la memoria
Con A' = 0.9/20 + 0.3/50 + 0/80 y C' = 1/2 + 0.5/8 + 0/16, las únicas
celdas con observación > 0 son (20,2)=0.9, (20,8)=0.5, (50,2)=0.3 y
(50,8)=0.3. Resultado:
```
B' = 0.1/-10 + 0.1/-5 + 0.1/0 + 0.5/5 + 0.9/10
```
Cómo sale cada valor:
- y=10: celda (20,2) → T_L(0.9, 1.0) = 0.9
- y=5: celdas (20,2) y (20,8) → T_L(0.9, 0.6) = T_L(0.5, 1.0) = 0.5
- y=-10, -5, 0: celdas (20,8), (50,2), (50,8) → T_L(0.5, 0.6) =
  T_L(0.3, 0.8) = 0.1

**El "suelo" de 0.1 — qué significa:** donde B(y)=0 la relación vale
R = 1 − (A×C), y entonces T_L(A'×C', 1 − A×C) = max(0, A'×C' − A×C).
O sea, el suelo mide **cuánto se sale la observación del antecedente**:
en (20,8), 0.5 − 0.4 = 0.1; en (50,·), 0.3 − 0.2 = 0.1. Es la parte de lo
observado que la regla no cubre, y el sistema la expresa como
incertidumbre.

**Ojo:** las celdas con x=80 NO aportan nada aunque ahí `I(0,b)=1`,
porque la observación vale 0 y T_L(0, 1) = 0.

**Error de la versión anterior (para que no lo repitas):** antes se usaba
sup-min y salía un suelo de 0.5, y la explicación decía que venía de las
celdas x=80. Era falso por lo mismo de arriba: con observación 0 esas
celdas no aportan.

### 3.6 — ¿Y las otras reglas?
Se desarrolla R1 porque es la que esta observación activa con más fuerza.
Con toda la base, cada regla Ri da su relación Ri (mismos Pasos 1 y 2), y
al ser reglas de tipo implicación se combinan por **intersección**:
R = min_i Ri. Una regla cuyo antecedente vale 0 en todas las celdas
observadas da Ri = 1 ahí, y 1 es neutro para el mínimo: no cambia nada.

---

## Punto 4 — Inferencia tipo Mamdani (números borrosos, universo continuo)

Aquí ya no se usan universos discretos {20,50,80}, sino funciones de
pertenencia continuas (triangulares/trapezoidales) sobre todo el rango
[0,100], [0,20], [-10,10].

### Los 4 pasos de Mamdani (memorizar este orden):

1. **Fuzzificación:** dado un valor crisp observado (RSI=35), calcular su
   grado de pertenencia en cada etiqueta de la variable (sobrevendido=0.75,
   neutral=0.25, sobrecomprado=0). Es solo interpolación lineal en la
   función de pertenencia.

2. **Fuerza de disparo de cada regla (α):** el mínimo de los grados de
   los antecedentes que aparecen en esa regla (t-norma otra vez). Si un
   antecedente vale 0, la regla no dispara (α=0).

3. **Recorte y agregación:** la conclusión de cada regla activa se
   "recorta" (clip) a la altura de su α — es decir, su función de
   pertenencia de salida no puede superar α. Luego todas las conclusiones
   recortadas se combinan por **máximo** (unión) en una única superficie.

4. **Desborrosificación (defuzzificación):** convertir esa superficie
   borrosa en un único número crisp. El método estándar de Mamdani es el
   **centro de gravedad (COG)**:
   ```
   COG = ∫ y·μ(y) dy / ∫ μ(y) dy
   ```
   — el "centro de masa" de la superficie agregada.

### El resultado en la memoria
Con RSI=35, Volatilidad=8:
```
Borrosificación:  sobrevendido=0.75  neutral=0.25  sobrecomprado=0
                  baja=0.4           media=0.6     alta=0

R1 (sobrevendido ∧ baja)   α1 = min(0.75, 0.4) = 0.4   → comprar_fuerte
R3 (neutral)               α3 = 0.25                   → mantener
R6 (sobrevendido ∧ media)  α6 = min(0.75, 0.6) = 0.6   → comprar
R2, R4, R5, R7: α = 0 (no disparan)
```
Cómo se calcula cada grado (interpolación lineal):
- sobrevendido(35): baja de 1 en 30 a 0 en 50 → (50−35)/20 = 0.75
- neutral(35): sube de 0 en 30 a 1 en 50 → (35−30)/20 = 0.25
- baja(8): baja de 1 en 5 a 0 en 10 → (10−8)/5 = 0.4
- media(8): sube de 0 en 5 a 1 en 10 → (8−5)/5 = 0.6

**Unión de las tres conclusiones recortadas** (el máximo en cada y):
```
[-4,-3]   rampa 0 → 0.25       (mantener sube)
[-3, 1]   0.25                 (mantener recortado)
[1, 2.4]  rampa 0.25 → 0.6     (comprar = y/4 supera a mantener)
[2.4,5.6] 0.6                  (comprar recortado)
[5.6,6.4] rampa 0.6 → 0.4      (comprar baja hasta igualar a comprar_fuerte)
[6.4,10]  0.4                  (comprar_fuerte recortado)
```
**Centro de gravedad por tramos:** área total 5.480, momento total 21.529
→ **COG = 21.529 / 5.480 = 3.9287**. FuzzyCLIPS dio 3.928710462287105:
idéntico.

**Cómo defenderlo:** sale una compra moderada (+3.93). La regla que más
pesa es R6 (α=0.6, *comprar*, centrada en y=4); R1 empuja un poco hacia
arriba (comprar_fuerte) y R3 un poco hacia abajo (mantener).

⚠️ **Detalle importante para entender bien el tema:** existe un método
"rápido" de aproximar el COG usando solo los extremos de cada α-corte (en
vez de integrar toda la superficie). **No es equivalente** al centro de
gravedad real: ignora las rampas y la forma de la curva. FuzzyCLIPS
calcula el centro de gravedad exacto; por eso en la memoria el cálculo a
mano se hace por tramos (rampas y mesetas), y así coincide con FuzzyCLIPS.

---

## Punto 5 — Implementación en CLIPS / FuzzyCLIPS

### ¿Qué es CLIPS?
Un motor de sistemas de producción: mantiene una **memoria de hechos**
(working memory) y una **base de reglas**. `(reset)` carga los hechos
iniciales, `(run)` dispara reglas por encadenamiento hacia delante hasta
que no queda ninguna activable.

### ¿Qué añade FuzzyCLIPS?
Permite que un `deftemplate` tenga un **universo y funciones de
pertenencia** en vez de solo campos ordinarios:
```lisp
(deftemplate RSI
    0 100
    (
        (sobrevendido (0 1) (30 1) (50 0))
        (neutral (30 0) (50 1) (70 0))
        (sobrecomprado (50 0) (70 1) (100 1))
    )
)
```
Un hecho como `(RSI (35 0)(35 1)(35 0))` es un **singleton borroso**: un
triángulo degenerado que dice "RSI=35 con certeza total" (0 antes, 1 en
35, 0 después — todo en el mismo punto x=35).

### Las reglas
```lisp
(defrule R1
    (RSI sobrevendido)
    (VOLATILIDAD baja)
=>
    (assert (SENAL comprar_fuerte))
)
```
El patrón `(RSI sobrevendido)` no exige que RSI sea *exactamente*
sobrevendido — FuzzyCLIPS calcula automáticamente el grado de pertenencia
del hecho actual a esa etiqueta y lo usa como grado de disparo de la
regla. Por eso R1 dispara con α=0.4 aunque el hecho sea RSI=35 (no un
"sobrevendido puro").

### Comandos clave usados
| Comando | Qué hace |
|---|---|
| `(load "archivo.clp")` | Lee un `.clp` (deftemplates/defrules/deffacts) |
| `(reset)` | Limpia la memoria de trabajo y recarga los `deffacts` |
| `(facts)` | Lista los hechos actuales |
| `(run)` | Dispara todas las reglas activables (forward chaining) |
| `(moment-defuzzify <fact-index>)` | Centro de gravedad del hecho borroso indicado — el método de desborrosificación de Mamdani |

### Lo que realmente pasó al ejecutarlo (verificado por ti mismo en consola)
1. Se cargan BC (reglas) y BH (hechos) sin errores.
2. `(reset)` + `(facts)` → aparecen los hechos singleton de RSI=35 y
   Volatilidad=8.
3. `(run)` → disparan R1, R3 y R6 (las únicas con antecedente > 0). R2,
   R4, R5 y R7 no disparan porque su antecedente vale 0 con estos hechos.
4. El motor genera un único hecho `SENAL` combinando las tres conclusiones
   (el índice salta de f-2 a f-5: f-3 y f-4 fueron conclusiones
   intermedias que se retractaron al fusionarse — es la unión Mamdani
   ocurriendo en tiempo real). Sus puntos son
   `(-4,0) (-3,0.25) (1,0.25) (2.4,0.6) (5.6,0.6) (6.4,0.4)`: exactamente
   la unión calculada a mano en el punto 4.
5. `(moment-defuzzify 5)` → **3.928710462287105**, que coincide con el
   cálculo hecho a mano (21.529 / 5.480).

**Cuidado al repetirlo:** el número que va en `moment-defuzzify` es el del
hecho `SENAL` que aparece en `(facts)` (aquí f-5). Si pones otro número
sale un error (`Unable to find fuzzy fact`).

**Por qué esta ejecución real importa más que un cálculo teórico:**
demuestra que las reglas están bien escritas sintácticamente, que el
razonamiento hacia delante ocurre como se predijo, y que el número final
no es una suposición — es lo que el motor de inferencia calcula de
verdad.

---

## Glosario rápido para repasar antes de un examen

| Término | Definición corta |
|---|---|
| Conjunto borroso | Función que asigna a cada elemento un grado de pertenencia [0,1] |
| T-norma | Operador AND borroso (ej. mínimo, producto) |
| T-conorma | Operador OR borroso (ej. máximo) |
| Implicación borrosa | Función que modela "SI a ENTONCES b" con grados (ej. Lukasiewicz, Mamdani=min) |
| Relación borrosa | Conjunto borroso sobre un producto cartesiano de universos (X×Y) |
| Modus Ponens Generalizado | Regla de inferencia que obtiene B' a partir de A' y R(x,y), vía una composición sup-T |
| Composición sup-T | `B'(y) = sup_x T[A'(x), R(x,y)]`; en la memoria T = Lukasiewicz |
| T-norma de Lukasiewicz | `T_L(a,b) = max(0, a+b-1)`; su residuo es la implicación de Lukasiewicz |
| Fuzzificación | Convertir un valor crisp en sus grados de pertenencia a cada etiqueta |
| Mamdani | Método de inferencia: min para α, min para recorte, max para unión, COG para desfuzzificar |
| Desborrosificación / defuzzificación | Convertir un conjunto borroso de salida en un único valor crisp |
| Centro de gravedad (COG) | Método de desborrosificación: "centro de masa" de la superficie de salida |
| Forward chaining | Razonamiento de hechos hacia conclusiones (motor RETE en CLIPS) |
| Singleton borroso | Conjunto borroso con grado 1 en un único punto y 0 en el resto |

---

## Preguntas para autoevaluarte

1. ¿Qué dos t-normas se usan en el punto 3 y en qué papel cada una? ¿Por
   qué para componer se eligió Lukasiewicz y no el mínimo?
2. ¿Qué pasaría con B' si la implicación fuera de Mamdani (`I(a,b)=min(a,b)`)
   en vez de Lukasiewicz? (Pista: Mamdani da 0 cuando a=0, sin "suelo"
   residual — compara ambos enfoques.)
3. ¿Por qué R2, R4, R5 y R7 no disparan con RSI=35, Volatilidad=8? ¿Qué
   aporta R6 en ese caso?
3b. ¿Por qué con solo R1–R5 el caso RSI=20, Volatilidad=10 no daba ninguna
   señal?
4. Si cambias la observación a RSI=70 (sobrecomprado), Volatilidad=15
   (alta) — ¿qué regla dispararía y qué signo (positivo/negativo)
   esperarías en la señal final, sin calcular el número exacto?
5. ¿Por qué el método de "2 puntos por α-corte" para el centro de
   gravedad puede dar un resultado distinto al centro de gravedad real?

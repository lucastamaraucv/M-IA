## Sistema de razonamiento aproximado aplicado a señales de trading BTC

**Autor:** Lucas Ivan Tamara Trejo
**Asignatura:** Razonamiento Aproximado (VIU) — J. A. Olivas
**Fecha:** Septiembre 2026

---

## 1. Dominio, objetivo, alcance y límites

**Dominio propuesto:** un sistema experto borroso de apoyo a la decisión que
recomienda una **señal de trading graduada** sobre Bitcoin (BTC), a partir de
dos indicadores técnicos habituales entre inversores minoristas:

- **RSI** (*Relative Strength Index*, 0-100): mide si el activo está
  sobrevendido (posible rebote al alza) o sobrecomprado (posible corrección
  a la baja).
- **Volatilidad** (variación porcentual en las últimas 24h, 0-20%): mide el
  riesgo/incertidumbre del momento.

**Objetivo:** en vez de una regla binaria rígida tipo "si RSI&lt;30, comprar"
(que trata igual un RSI de 29 que uno de 5, y no distingue un RSI de 31 de
uno de 29 aunque sean casi idénticos), el sistema modela ambos indicadores
como **conjuntos borrosos** y combina su información con reglas imprecisas,
devolviendo una recomendación graduada entre "vender fuerte" y
"comprar fuerte" — mucho más fiel a cómo un trader experimentado razona en
la práctica ("está bastante sobrevendido, pero hay mucha volatilidad, así
que mejor entrar con cautela").

**Alcance:** sistema de **apoyo** a la decisión, no ejecuta órdenes
automáticamente ni es un bot de trading.

**Límites:** solo 2 variables de entrada y parámetros ilustrativos, no
calibrados con datos históricos reales.

---

## 2. Base de conocimiento: 7 reglas imprecisas

Variables lingüísticas:

| Variable | Universo | Etiquetas |
|---|---|---|
| RSI (entrada) | [0, 100] | sobrevendido, neutral, sobrecomprado |
| Volatilidad (entrada) | [0, 20] (%) | baja, media, alta |
| Señal (salida) | [-10, 10] | vender_fuerte, vender, mantener, comprar, comprar_fuerte |

Reglas (razonamiento hacia delante: a partir de los hechos observados de
RSI y Volatilidad, se disparan las reglas cuyo antecedente coincide y se
concluye la Señal):

- **R1:** Si RSI es *sobrevendido* y Volatilidad es *baja*, Entonces Señal
  es *comprar_fuerte*.
- **R2:** Si RSI es *sobrevendido* y Volatilidad es *alta*, Entonces Señal
  es *comprar*. *(la alta volatilidad templa la agresividad de la señal)*
- **R3:** Si RSI es *neutral*, Entonces Señal es *mantener*.
- **R4:** Si RSI es *sobrecomprado* y Volatilidad es *baja*, Entonces Señal
  es *vender_fuerte*.
- **R5:** Si RSI es *sobrecomprado* y Volatilidad es *alta*, Entonces
  Señal es *vender*.
- **R6:** Si RSI es *sobrevendido* y Volatilidad es *media*, Entonces Señal
  es *comprar*.
- **R7:** Si RSI es *sobrecomprado* y Volatilidad es *media*, Entonces
  Señal es *vender*.

La estructura es simétrica a propósito (R1↔R4, R2↔R5, R6↔R7): solo con
volatilidad baja se emite una señal *_fuerte; con volatilidad media o alta
la señal se "modera", reflejando que en momentos de mucho ruido conviene
ser más cauto aunque el RSI sea extremo. Las reglas cubren las tres
etiquetas de volatilidad, de modo que **para cualquier entrada se dispara al
menos una regla**: si neutral(RSI)>0 dispara R3; si no, el RSI es ≤30 o ≥70
(sobrevendido o sobrecomprado vale 1) y alguna etiqueta de volatilidad es
mayor que 0 en todo [0,20]. Sin R6/R7 esto no se cumplía: con RSI=20 y
Volatilidad=10 ninguna regla se activaba (baja(10)=alta(10)=neutral(20)=0),
lo que se comprobó en FuzzyCLIPS.

---

## 3. Ejemplo con universo NO continuo — Relaciones borrosas + Modus Ponens Generalizado

Para ilustrar el mecanismo se toma la regla completa **R1** ("Si RSI es
sobrevendido **y** Volatilidad es baja, Entonces Señal es comprar_fuerte"),
con sus **dos antecedentes**, sobre universos discretos pequeños:

- Universo X (RSI): {20, 50, 80}
- Universo Z (Volatilidad): {2, 8, 16}
- Universo Y (Señal): {-10, -5, 0, 5, 10}

Conjuntos borrosos de la regla:
```
A = "RSI sobrevendido"      = 1/20 + 0.2/50 + 0/80
C = "Volatilidad baja"      = 1/2  + 0.4/8  + 0/16
B = "Señal comprar_fuerte"  = 0/-10 + 0/-5 + 0/0 + 0.6/5 + 1/10
```

**Parámetros elegidos:**

- **Conjunción de antecedentes:** t-norma **mínimo**,
  `(A×C)(x,z) = min(A(x), C(z))`.
- **Implicación:** **Lukasiewicz**, `I(a,b) = min(1, 1-a+b)`. Es a la vez
  S-implicación y R-implicación.
- **Composición del MPG:** sup-T con la t-norma de **Lukasiewicz**,
  `T_L(a,b) = max(0, a+b-1)`. Se elige porque la implicación de Lukasiewicz
  es precisamente el residuo de T_L, y esa pareja garantiza la propiedad
  básica del Modus Ponens: **si la observación coincide con el antecedente
  (A'=A, C'=C), la conclusión es exactamente B'=B**. Con la composición
  sup-min esta propiedad no se cumple (se comprueba más abajo).

**Paso 1 — Antecedente combinado** `(A×C)(x,z) = min(A(x), C(z))`:

| (x,z) | (20,2) | (20,8) | (20,16) | (50,2) | (50,8) | (50,16) | (80,2) | (80,8) | (80,16) |
|---|---|---|---|---|---|---|---|---|---|
| A×C | 1.0 | 0.4 | 0.0 | 0.2 | 0.2 | 0.0 | 0.0 | 0.0 | 0.0 |

**Paso 2 — Relación** `R((x,z),y) = I((A×C)(x,z), B(y))`:

|         | y=-10 | y=-5 | y=0 | y=5 | y=10 |
|---|---|---|---|---|---|
| **(20,2)**  | 0.0 | 0.0 | 0.0 | 0.6 | 1.0 |
| **(20,8)**  | 0.6 | 0.6 | 0.6 | 1.0 | 1.0 |
| **(20,16)** | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| **(50,2)**  | 0.8 | 0.8 | 0.8 | 1.0 | 1.0 |
| **(50,8)**  | 0.8 | 0.8 | 0.8 | 1.0 | 1.0 |
| **(50,16)** | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| **(80,2)**  | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| **(80,8)**  | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| **(80,16)** | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

**Observación real** (lecturas imprecisas: RSI ronda 20-25, Volatilidad
ronda 2-5):
```
A' = 0.9/20 + 0.3/50 + 0/80
C' = 1/2 + 0.5/8 + 0/16
(A'×C')(x,z) = min(A'(x), C'(z))
```

| (x,z) | (20,2) | (20,8) | (20,16) | (50,2) | (50,8) | (50,16) | (80,2) | (80,8) | (80,16) |
|---|---|---|---|---|---|---|---|---|---|
| A'×C' | 0.9 | 0.5 | 0.0 | 0.3 | 0.3 | 0.0 | 0.0 | 0.0 | 0.0 |

**Paso 3 — Modus Ponens Generalizado:**
`B'(y) = sup_(x,z) T_L[(A'×C')(x,z), R((x,z),y)]`,
con `T_L(a,b) = max(0, a+b-1)`.

Solo aportan las celdas con observación mayor que 0: (20,2), (20,8), (50,2)
y (50,8). Calculando para cada y (se indica la celda o celdas que alcanzan
el supremo):

| y | Celda(s) ganadora(s) | Cálculo | B'(y) |
|---|---|---|---|
| -10 | (20,8), (50,2), (50,8) | T_L(0.5, 0.6) = T_L(0.3, 0.8) = 0.1 | 0.1 |
| -5 | (20,8), (50,2), (50,8) | ídem | 0.1 |
| 0 | (20,8), (50,2), (50,8) | ídem | 0.1 |
| 5 | (20,2), (20,8) | T_L(0.9, 0.6) = T_L(0.5, 1.0) = 0.5 | 0.5 |
| 10 | (20,2) | T_L(0.9, 1.0) = 0.9 | 0.9 |

```
B' = 0.1/-10 + 0.1/-5 + 0.1/0 + 0.5/5 + 0.9/10
```

**Interpretación:** con esas lecturas de RSI y Volatilidad, el sistema
infiere una señal claramente concentrada en la zona de compra fuerte
(grado 0.9 en y=10, 0.5 en y=5). El pequeño "suelo" de 0.1 en el resto
del universo tiene una lectura precisa: donde B(y)=0, la relación vale
R = 1 − (A×C), y entonces `T_L(A'×C', 1 − A×C) = max(0, A'×C' − A×C)`.
Es decir, el suelo mide **cuánto excede la observación al antecedente de
la regla** (en (20,8): 0.5 − 0.4 = 0.1; en (50,·): 0.3 − 0.2 = 0.1). Esa
parte de la observación no está cubierta por la regla, y el sistema la
traduce honestamente en un grado de incertidumbre.

**Comprobación de la elección de parámetros** (observación idéntica al
antecedente, A'=A y C'=C):

| Composición | B' obtenido | ¿B' = B? |
|---|---|---|
| sup-min | 0.4/-10 + 0.4/-5 + 0.4/0 + 0.6/5 + 1/10 | No |
| **sup-T_L** (elegida) | 0/-10 + 0/-5 + 0/0 + 0.6/5 + 1/10 | **Sí** |

Con sup-min, la celda (20,8) da min(0.4, 0.6) = 0.4 para y=-10, aunque
B(-10)=0; con sup-T_L da max(0, 0.4+0.6−1) = 0. Por eso sup-T_L es la
composición adecuada para la implicación de Lukasiewicz.

**Extensión a la base completa de reglas:** cada regla Ri se transforma en
su relación Ri con el mismo procedimiento (Pasos 1 y 2). Al tratarse de
reglas de tipo implicación, la base se agrega por **intersección**,
`R = min_i Ri`, y la conclusión es `B' = (A'×C') ∘ R` con la misma
composición sup-T_L. Una regla cuyo antecedente vale 0 en todas las celdas
observadas da Ri = I(0, b) = 1 en ellas y no restringe el resultado (1 es
el elemento neutro del mínimo). Se ha desarrollado R1 porque es la regla que
esta observación (RSI ≈ 20-25, volatilidad ≈ 2-5) activa con más fuerza.

*Nota:* los grados de los conjuntos discretos de este ejemplo son
ilustrativos, elegidos para el ejemplo; no son un muestreo exacto de las
funciones continuas de la sección 4.

---

## 4. Ejemplo con números borrosos (continuo) — Inferencia tipo Mamdani

Ahora se usan **todas las reglas** (R1-R7) sobre universos **continuos**,
representando cada etiqueta como un número borroso triangular/trapezoidal
(pares `(valor, grado)`, mismo formato que usa FuzzyCLIPS):

```
RSI [0,100]:
  sobrevendido  = (0,1) (30,1) (50,0)
  neutral       = (30,0) (50,1) (70,0)
  sobrecomprado = (50,0) (70,1) (100,1)

Volatilidad [0,20]:
  baja  = (0,1) (5,1) (10,0)
  media = (5,0) (10,1) (15,0)
  alta  = (10,0) (15,1) (20,1)

Señal [-10,10]:
  vender_fuerte  = (-10,1) (-8,1) (-4,0)
  vender         = (-8,0) (-4,1) (0,0)
  mantener       = (-4,0) (0,1) (4,0)
  comprar        = (0,0) (4,1) (8,0)
  comprar_fuerte = (4,0) (8,1) (10,1)
```

**Observación:** RSI = 35, Volatilidad = 8 (medidas concretas del momento).

**Paso 1 — Borrosificación** (grado de pertenencia de la observación en
cada etiqueta):
```
RSI=35:         sobrevendido=0.75   neutral=0.25   sobrecomprado=0
Volatilidad=8:  baja=0.4            media=0.6      alta=0
```

**Paso 2 — Grado de aplicabilidad de cada regla** (mínimo de sus
antecedentes, método de Mamdani):
```
R1 (sobrevendido ∧ baja → comprar_fuerte):  α1 = min(0.75, 0.4) = 0.4
R2 (sobrevendido ∧ alta → comprar):         α2 = min(0.75, 0)   = 0   (no dispara)
R3 (neutral → mantener):                    α3 = 0.25
R4 (sobrecomprado ∧ baja → vender_fuerte):  α4 = min(0, 0.4)    = 0   (no dispara)
R5 (sobrecomprado ∧ alta → vender):         α5 = min(0, 0)      = 0   (no dispara)
R6 (sobrevendido ∧ media → comprar):        α6 = min(0.75, 0.6) = 0.6
R7 (sobrecomprado ∧ media → vender):        α7 = min(0, 0.6)    = 0   (no dispara)
```
Están activas **R1** (α=0.4), **R3** (α=0.25) y **R6** (α=0.6) — el resto
no aporta nada porque su antecedente vale 0. Nótese que R6 recoge el grado
0.6 de volatilidad *media*, información que sin esta regla se perdería.

**Paso 3 — Recorte y combinación** (cada conclusión se recorta a la altura
de su α y se combinan por MÁXIMO/unión, como en el ejemplo del péndulo
visto en clase):

- α-corte de *comprar_fuerte* a 0.4: intervalo **[5.6, 10]**
- α-corte de *mantener* a 0.25: intervalo **[-3, 3]**
- α-corte de *comprar* a 0.6: intervalo **[2.4, 5.6]**

La unión de las tres conclusiones recortadas es:
```
μ(y) = rampa de 0 a 0.25 en [-4,-3];  0.25 en [-3,1];
       rampa de 0.25 a 0.6 en [1,2.4] (comprar = y/4 supera a mantener);
       0.6 en [2.4,5.6];  rampa de 0.6 a 0.4 en [5.6,6.4] (comprar baja);
       0.4 en [6.4,10] (comprar_fuerte recortado)
```

**Paso 4 — Desborrosificación** (centro de gravedad de la superficie
combinada, método estándar de Mamdani), descomponiendo μ(y) en tramos:

| Tramo | Forma | Área | Centroide | Área × centroide |
|---|---|---|---|---|
| [-4, -3] | rampa 0 → 0.25 | 0.125 | -3.333 | -0.417 |
| [-3, 1] | meseta 0.25 | 1.000 | -1.000 | -1.000 |
| [1, 2.4] | rampa 0.25 → 0.6 | 0.595 | 1.796 | 1.069 |
| [2.4, 5.6] | meseta 0.6 | 1.920 | 4.000 | 7.680 |
| [5.6, 6.4] | rampa 0.6 → 0.4 | 0.400 | 5.973 | 2.389 |
| [6.4, 10] | meseta 0.4 | 1.440 | 8.200 | 11.808 |
| **Total** | | **5.480** | | **21.529** |

```
COG = ∫ y·μ(y) dy / ∫ μ(y) dy = 21.529 / 5.480 = 3.9287
```

**Conclusión del ejemplo:** con RSI=35 (ligeramente sobrevendido, entre la
zona plena de sobreventa y la neutral) y Volatilidad=8 (entre baja y
media), el sistema recomienda una señal de **+3,93 sobre 10** — una compra
moderada: ni "fuerte" (el RSI ya no está en la zona más extrema y la
volatilidad es mayoritariamente media), ni "mantener puro" (sigue habiendo
bastante componente de sobreventa). La regla que más pesa es R6
(*comprar*, α=0.6), cuyo centro está justamente en y=4.

---

## 5. Implementación en CLIPS/FuzzyCLIPS

Las 7 reglas y las observaciones del ejemplo de la sección 4 (RSI=35,
Volatilidad=8) se implementaron en FuzzyCLIPS, en dos archivos separados
(adjuntos): **`BC_btc_trading.clp`** (base de conocimiento: los 3
`deftemplate` borrosos + las 7 `defrule`) y **`BH_btc_trading.clp`** (base
de hechos: la observación como singleton, mismo formato que usa el curso).

Traza **real**, ejecutada en FuzzyCLIPS V6.10d sobre los propios archivos
`BC_btc_trading.clp` / `BH_btc_trading.clp` adjuntos (captura literal de
consola, sin editar):

```
FuzzyCLIPS> (clear)
FuzzyCLIPS> (load "C:/Users/Lucas Tamara/Desktop/M IA/RAZONAMIENTO APROXIMADO/Actividad 1 Desarrollo de un sistema borroso/subir/BC_btc_trading.clp")
Defining deftemplate: RSI
Defining deftemplate: VOLATILIDAD
Defining deftemplate: SENAL
Defining defrule: R1 +j+j
Defining defrule: R2 =j+j
Defining defrule: R3 +j
Defining defrule: R4 +j+j
Defining defrule: R5 =j+j
Defining defrule: R6 =j+j
Defining defrule: R7 =j+j
TRUE

FuzzyCLIPS> (load "C:/Users/Lucas Tamara/Desktop/M IA/RAZONAMIENTO APROXIMADO/Actividad 1 Desarrollo de un sistema borroso/subir/BH_btc_trading.clp")
Defining deffacts: hechos
TRUE

FuzzyCLIPS> (reset)

FuzzyCLIPS> (facts)
f-0     (initial-fact) CF 1.00
f-1     (RSI ???) CF 1.00
( (35.0 0.0) (35.0 1.0) (35.0 0.0)  )
f-2     (VOLATILIDAD ???) CF 1.00
( (8.0 0.0) (8.0 1.0) (8.0 0.0)  )
For a total of 3 facts.

FuzzyCLIPS> (run)

FuzzyCLIPS> (facts)
f-0     (initial-fact) CF 1.00
f-1     (RSI ???) CF 1.00
( (35.0 0.0) (35.0 1.0) (35.0 0.0)  )
f-2     (VOLATILIDAD ???) CF 1.00
( (8.0 0.0) (8.0 1.0) (8.0 0.0)  )
f-5     (SENAL ???) CF 1.00
( (-4.0 0.0) (-3.0 0.25) (1.0 0.25) (2.4 0.6) (5.6 0.6)
  (6.4 0.4) )
For a total of 4 facts.

FuzzyCLIPS> (moment-defuzzify 5)
3.928710462287105
```

**Lectura de la traza:** disparan R1, R3 y R6 (coincide con la predicción
de la sección 4: R2, R4, R5 y R7 tienen antecedente 0 con estos hechos).
El motor combina las tres conclusiones en un único hecho `SENAL` (el índice
salta de `f-2` a `f-5`: `f-3` y `f-4` fueron conclusiones intermedias que
se retractaron al combinarse, comportamiento estándar de unión Mamdani).
Los puntos del hecho resultante coinciden exactamente con la función μ(y)
calculada a mano en el Paso 3 de la sección 4: (-4,0), (-3,0.25),
(1,0.25), (2.4,0.6), (5.6,0.6), (6.4,0.4) y 0.4 hasta y=10. El resultado
de `(moment-defuzzify 5)` es **3.9287**, idéntico al centro de gravedad
calculado a mano (21.529 / 5.480).

---

## Anexo — Código fuente completo (BC y BH)

Se reproduce aquí el contenido íntegro de ambos archivos `.clp`, adjuntos
también por separado.

**`BC_btc_trading.clp`** (base de conocimiento: 3 `deftemplate` borrosos +
7 `defrule`):

```lisp
(deftemplate RSI
	0 100
	(
		(sobrevendido (0 1) (30 1) (50 0))
		(neutral (30 0) (50 1) (70 0))
		(sobrecomprado (50 0) (70 1) (100 1))
	)
)

(deftemplate VOLATILIDAD
	0 20
	(
		(baja (0 1) (5 1) (10 0))
		(media (5 0) (10 1) (15 0))
		(alta (10 0) (15 1) (20 1))
	)
)

(deftemplate SENAL
	-10 10
	(
		(vender_fuerte (-10 1) (-8 1) (-4 0))
		(vender (-8 0) (-4 1) (0 0))
		(mantener (-4 0) (0 1) (4 0))
		(comprar (0 0) (4 1) (8 0))
		(comprar_fuerte (4 0) (8 1) (10 1))
	)
)

(defrule R1
	(RSI sobrevendido)
	(VOLATILIDAD baja)
=>
	(assert (SENAL comprar_fuerte))
)

(defrule R2
	(RSI sobrevendido)
	(VOLATILIDAD alta)
=>
	(assert (SENAL comprar))
)

(defrule R3
	(RSI neutral)
=>
	(assert (SENAL mantener))
)

(defrule R4
	(RSI sobrecomprado)
	(VOLATILIDAD baja)
=>
	(assert (SENAL vender_fuerte))
)

(defrule R5
	(RSI sobrecomprado)
	(VOLATILIDAD alta)
=>
	(assert (SENAL vender))
)

(defrule R6
	(RSI sobrevendido)
	(VOLATILIDAD media)
=>
	(assert (SENAL comprar))
)

(defrule R7
	(RSI sobrecomprado)
	(VOLATILIDAD media)
=>
	(assert (SENAL vender))
)
```

**`BH_btc_trading.clp`** (base de hechos: observación singleton RSI=35,
Volatilidad=8, mismo formato que usa el material del curso):

```lisp
(deffacts hechos
	(RSI (35 0) (35 1) (35 0))
	(VOLATILIDAD (8 0) (8 1) (8 0))
)
```

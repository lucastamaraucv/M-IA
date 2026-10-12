# Guía de aprendizaje: CLIPS y FuzzyCLIPS

Guía paso a paso para aprender a programar en CLIPS/FuzzyCLIPS, con el
"por qué interno" de cada comando y su equivalente conceptual en Python.
Construida para la Actividad 1 de Razonamiento Aproximado (VIU), usando
como material de práctica los archivos reales de `SESIONES\` y el propio
`BC_btc_trading.clp` / `BH_btc_trading.clp` de esta carpeta.

---

## 0. Por qué CLIPS/FuzzyCLIPS y no Python

- **La actividad lo exige explícitamente** (`instrucciones.txt`, punto 5):
  "Implementar las reglas en CLIPS/FUZZY CLIPS... anexando los archivos
  de BH y BC". No es una elección de implementación, es un entregable.
- Python (con `scikit-fuzzy`, `simpful`, etc.) **sí podría** hacer los
  mismos cálculos numéricos. La diferencia es que CLIPS es un **motor de
  sistemas de producción** de verdad: encadenamiento hacia delante
  automático (algoritmo RETE), agenda de conflicto, hechos que disparan
  reglas dinámicamente. El curso evalúa que entiendas ese paradigma, no
  que sepas llamar a una función matemática.
- FuzzyCLIPS integra la borrosidad **dentro del motor de inferencia**
  (deftemplates con universos y funciones de pertenencia, propagación de
  conjuntos borrosos entre reglas encadenadas, desborrosificación nativa)
  en vez de como una capa añadida encima.

La lógica matemática (MPG, t-normas, Mamdani) es la misma que en Python;
solo cambia el lenguaje anfitrión y el hecho de que aquí hay un motor de
inferencia real ejecutándose por debajo.

---

## 1. Preparar el entorno

Ejecutable: `FuzzyClips.exe` (⚠️ **no** `CLIPSWin.exe` — ese es CLIPS puro
sin lógica borrosa y da error de sintaxis al cargar un `deftemplate`
borroso). Ver [[fuzzyclips-vs-clips-ejecutable]].

Es una **ventana de consola de texto**, no una app con botones. Se
interactúa escribiendo comandos con el teclado (paréntesis incluidos) y
pulsando Enter, junto al prompt `CLIPS>`. Para salir: `(exit)`.

⚠️ Si al pulsar Enter no vuelve a aparecer `CLIPS>`, es que falta cerrar
algún paréntesis — la consola espera a que el número de `(` y `)`
cuadre antes de ejecutar.

---

## 2. Los 4 comandos básicos de hechos (memoria de trabajo)

Internamente, CLIPS mantiene una tabla de hechos (la *working memory*).
Cada comando es una operación sobre esa tabla — el mismo modelo mental
que una lista/diccionario de Python con funciones de apoyo:

```python
memoria_de_hechos = {}   # id_hecho -> contenido del hecho
siguiente_id = 0         # nunca retrocede, aunque borres hechos

def assert_fact(hecho):
    global siguiente_id
    memoria_de_hechos[siguiente_id] = hecho
    print(f"<Fact-{siguiente_id}>")
    siguiente_id += 1

def facts():
    for fid, hecho in memoria_de_hechos.items():
        print(f"f-{fid}\t{hecho}")
    print(f"For a total of {len(memoria_de_hechos)} fact(s).")

def retract(fid):
    del memoria_de_hechos[fid]

def clear():
    global memoria_de_hechos, siguiente_id
    memoria_de_hechos, siguiente_id = {}, 0
```

| Comando CLIPS | Qué hace internamente | Equivalente Python |
|---|---|---|
| `(assert (motor no_arranca))` | Crea el hecho ordenado `(motor no_arranca)` — tupla de símbolos, sin campos con nombre porque no hay `deftemplate` — le asigna el siguiente id y lo guarda | `assert_fact(("motor","no_arranca"))` |
| `(facts)` | Recorre la tabla e imprime cada entrada con su id | `facts()` (un `for` sobre el diccionario) |
| `(retract 1)` | Borra la entrada cuyo **id** es 1 (el id que ves en `(facts)` como `f-1`, no el contenido) | `retract(1)` |
| `(clear)` | Vacía la tabla y reinicia el contador; también descarga reglas cargadas | `clear()` |

Práctica en consola (sin cargar ningún archivo):
```
(assert (motor no_arranca))
(facts)
(assert (luces no_se_encienden))
(facts)
(retract 1)
(facts)
(clear)
(facts)
```

Con solo esto, CLIPS es "una lista con funciones" — la parte que lo hace
un motor de verdad es el `defrule` del siguiente punto.

---

## 3. `defrule` y `run`: encadenamiento hacia delante

Sintaxis:
```
(defrule <nombre>
   [(declare (salience <n>))]
   (patrón_1) ... (patrón_N)
=>
   (acción_1) ... (acción_N)
)
```

Si **todos** los patrones de la izquierda casan con hechos existentes en
la memoria de trabajo, la regla queda "activable" (entra en la
*agenda*). `(run)` dispara las reglas activables una tras otra; cada
`assert`/`retract` que ejecuta una acción puede activar nuevas reglas —
eso es "razonamiento hacia delante" (forward chaining).

Modelo mental en Python (simplificado — CLIPS real usa el algoritmo
RETE para no re-comprobar todo desde cero en cada paso, pero el
resultado observable es este bucle de "emparejar y disparar"):

```python
reglas = []

def defrule(nombre, patrones, accion):
    reglas.append({"nombre": nombre, "patrones": patrones,
                    "accion": accion, "disparada": False})

def patron_casa(patron, hechos):
    return patron in hechos.values()

def run():
    disparo = True
    while disparo:
        disparo = False
        for r in reglas:
            if not r["disparada"] and all(patron_casa(p, memoria_de_hechos)
                                           for p in r["patrones"]):
                r["accion"]()          # puede hacer assert_fact(...)
                r["disparada"] = True
                disparo = True
```

### Práctica: `SESIONES\BC_coche.clp` / `BH_coche.clp` (CLIPS puro)
```
(clear)
(load "BC_coche.clp")
(load "BH_coche.clp")
(reset)
(facts)
(run 1)
(facts)
(run 1)
(facts)
(run 1)
(facts)
```
`(reset)` carga los hechos iniciales del `deffacts` (`motor no_arranca`,
`luces no_se_encienden`). Dispara las reglas **de una en una** con
`(run 1)` para ver cómo cada hecho nuevo (`problema electrico`,
`problema combustion`, `bateria en_mal_estado`...) activa la siguiente
regla, hasta llegar a `revisar en_taller`.

---

## 4. FuzzyCLIPS: `deftemplate` borroso

```
(deftemplate X1
    0 7                          ; universo [mín, máx]
    (
        (baja  (0 1) (2 0))          ; etiqueta + pares (valor grado)
        (media (1 0) (3 1) (5 0))
        (alta  (3 0) (7 1))
    )
)
```
`0 7` es el universo de la variable. Cada etiqueta es una función de
pertenencia lineal a trozos definida por los puntos `(valor grado)`,
interpolados entre sí. Equivalente Python de "evaluar el grado de
pertenencia de un valor a una etiqueta":

```python
def pertenencia(valor, puntos):
    # puntos: lista de (valor, grado) ordenada por valor, interpolación lineal
    for (v1, g1), (v2, g2) in zip(puntos, puntos[1:]):
        if v1 <= valor <= v2:
            if v2 == v1:
                return g1
            return g1 + (g2 - g1) * (valor - v1) / (v2 - v1)
    return 0.0

baja = [(0, 1), (2, 0)]
pertenencia(1, baja)   # -> 0.5
```

Un **hecho borroso puntual (singleton)** se codifica como un triángulo
degenerado en el mismo punto: `(X1 (4 0) (4 1) (4 0))` significa "X1 = 4
con certeza total".

### Práctica: `SESIONES\BC_ejemplo_fuz.clp` / `BH_ejemplo_fuz.CLP`
```
(clear)
(load "BC_ejemplo_fuz.clp")
(load "BH_ejemplo_fuz.CLP")
(reset)
(facts)
(run)
(facts)
```
FuzzyCLIPS calcula el grado de pertenencia del hecho a cada etiqueta del
`deftemplate`, ve qué reglas casan con qué grado, y combina los
conjuntos borrosos de salida en `Y` con **composición max-min** (Modus
Ponens Generalizado, automático — por defecto; también existe
max-producto).

---

## 5. Desborrosificar

| Comando | Qué calcula |
|---|---|
| `(moment-defuzzify Y)` | Centro de gravedad (el método Mamdani) |
| `(maximum-defuzzify Y)` | Criterio del máximo |
| `(plot-fuzzy-value t Y 0 100 20)` | Dibuja en ASCII la función de pertenencia resultante de `Y` entre 0 y 100 con 20 puntos |

`moment-defuzzify` es el que pide la actividad para el ejemplo tipo
Mamdani.

---

## 6. Aplicación al caso propio: `BC_btc_trading.clp`

Asesor borroso de señales de trading BTC — `RSI` [0,100] (3 etiquetas) +
`VOLATILIDAD` [0,20] (3 etiquetas) → `SENAL` [-10,10] (5 etiquetas), 5
reglas Mamdani (R1-R5). Ver [[actividad1-sistema-borroso]] para el
estado completo de la actividad.

```
(clear)
(load "BC_btc_trading.clp")
(load "BH_btc_trading.clp")
(reset)
(facts)
(run)
(facts)
(moment-defuzzify SENAL)
```
Con `RSI=35, VOLATILIDAD=8` el resultado esperado es
`(moment-defuzzify SENAL)` ≈ **4.80** (verificado a mano en la memoria
de la actividad con centro de gravedad).

---

## 7. Ejercicios para consolidar

1. Cambia `RSI` en `BH_btc_trading.clp` a `(70 0) (70 1) (70 0)`
   (sobrecomprado), manteniendo `VOLATILIDAD=8`. Antes de ejecutar,
   predice qué regla se disparará y si la señal será de compra o venta;
   compruébalo con `(reset)(run)(facts)(moment-defuzzify SENAL)`.
2. Añade una 6ª regla a `BC_btc_trading.clp` para un caso no cubierto
   (`RSI neutral` + `VOLATILIDAD alta`) y comprueba que se dispara.
3. Estrecha los vértices de la etiqueta `sobrevendido` de `RSI` y
   observa cómo cambia el grado de pertenencia con el mismo hecho.

---

## Tabla resumen de comandos

| Comando | Categoría | Para qué sirve |
|---|---|---|
| `(load "archivo.clp")` | carga | Lee un archivo `.clp` (deftemplates, defrules, deffacts) |
| `(reset)` | hechos | Limpia la memoria de trabajo y vuelve a cargar el `deffacts` |
| `(clear)` | hechos/reglas | Borra todo: hechos y reglas cargadas |
| `(assert <hecho>)` | hechos | Añade un hecho a la memoria de trabajo |
| `(retract <id>)` | hechos | Borra el hecho con ese id |
| `(facts)` | hechos | Lista los hechos actuales |
| `(run)` / `(run N)` | inferencia | Dispara reglas activables (todas / N veces) |
| `(deftemplate ...)` | definición | Define una plantilla de hecho, borrosa si lleva universo + pares (valor grado) |
| `(defrule ...)` | definición | Define una regla patrón→acción |
| `(moment-defuzzify X)` | borroso | Desborrosifica por centro de gravedad (Mamdani) |
| `(maximum-defuzzify X)` | borroso | Desborrosifica por criterio del máximo |
| `(plot-fuzzy-value t X min max n)` | borroso | Grafica en ASCII la función de pertenencia de X |
| `(exit)` | consola | Cierra FuzzyCLIPS |

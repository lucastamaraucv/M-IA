# Plan de mejora — Modo Estudio/Examen para el Depurador Visual de Python

> **Objetivo del usuario (Lucas):** estudiar para su examen de *Python para IA* con
> entendimiento profundo de las sesiones S00–S16, y poder **pegar código nunca antes
> visto** y que el depurador lo **explique con animaciones** (qué hace cada línea + qué
> concepto del curso ejercita).
>
> Este documento es el plan a ejecutar **mañana**. Está pensado para implementarse
> en una sola jornada, por fases independientes y verificables.

---

## 0. Estado actual (punto de partida)

La app `python_visualizer_flask.py` ya tiene:
- Ejecución paso a paso con `sys.settrace` y nombre de archivo único `<vis_user_code>`.
- **Narrador AST** (`_explain_lines`) que explica en español *qué* hace cada línea de
  **cualquier** código (no depende de los 40 ejemplos). Cada línea tiene `{text, kind}`.
- 40 ejemplos (S00–S16) en `const EX = [...]`, todos verificados (test estricto navegador).
- Animaciones: barra "Narrador" animada, flechas SVG con partícula viajera, paneles
  Frames/Objects, resaltado de línea activa.
- Serialización a prueba de balas (NaN/Infinity saneados), `input()` con stub.

**Lo que falta para "estudiar el examen":** el narrador explica el *qué* (mecánica),
pero no el *por qué* (concepto) ni **a qué sesión/tema del curso pertenece**. No hay
forma de que, al pegar código nuevo, el sistema diga "esto es *broadcasting* de NumPy
(S08)" ni de repasar por concepto.

---

## 1. La mejora estrella: capa de **Conceptos del curso**

### 1.1 Idea
Una capa AST adicional, `_detect_concepts(code)`, que analiza **cualquier** código y
devuelve la lista de **conceptos del curso** que ejercita, cada uno con: nombre, sesión,
explicación breve, "por qué importa en el examen", y un puntero de línea(s).

Esto funciona con código pegado nunca antes visto porque es **estructural (AST) +
heurístico por API** (detecta `np.`, `.groupby(`, `yield`, `@property`, comprensiones,
etc.), igual que el narrador ya generaliza.

### 1.2 Modelo de datos
Crear un diccionario `CONCEPTS` (en el backend, Python) con entradas como:

```python
# clave -> metadata del concepto
CONCEPTS = {
  "list_comprehension": {
    "nombre": "Comprensión de listas",
    "sesion": "S03",
    "que": "Construye una lista en una sola expresión: [f(x) for x in it if cond].",
    "porque": "Pregunta típica de examen: reescribir un bucle for como comprensión.",
  },
  "broadcasting": {
    "nombre": "Broadcasting de NumPy",
    "sesion": "S08",
    "que": "Operaciones entre arrays de formas distintas sin bucles explícitos.",
    "porque": "Clave para vectorizar; suele evaluarse el resultado de a+v, a*2, etc.",
  },
  # ... (ver tabla de cobertura en §1.5)
}
```

### 1.3 Detección (cómo)
`_detect_concepts(code)` recorre el AST y aplica reglas. Dos tipos:

**A) Estructurales (nodo AST):**
| Concepto | Disparador AST |
|---|---|
| `list_comprehension` | `ast.ListComp` |
| `dict_comprehension` | `ast.DictComp` |
| `set_comprehension` | `ast.SetComp` |
| `generator_expr` | `ast.GeneratorExp` |
| `generator_fn` | `FunctionDef` que contiene `Yield`/`YieldFrom` |
| `lambda` | `ast.Lambda` |
| `decorator` | `decorator_list` no vacío |
| `class_inheritance` | `ClassDef` con `bases` |
| `property` | decorador `@property` |
| `staticmethod`/`classmethod` | decoradores homónimos |
| `recursion` | `FunctionDef` cuyo cuerpo se llama a sí mismo |
| `try_except` | `ast.Try` |
| `context_manager` | `ast.With` |
| `args_kwargs` | `arguments.vararg`/`kwarg` |
| `slicing` | `ast.Subscript` con `ast.Slice` |
| `fstring` | `ast.JoinedStr` |
| `unpacking` | `Assign` con `Tuple`/`Starred` target |

**B) Por API/atributo (heurística de nombres):**
| Concepto | Disparador (Attribute/Name/Call) |
|---|---|
| `numpy_array` | `np.array`, `np.zeros`, `np.arange`, `np.linspace` |
| `broadcasting` | operaciones binarias sobre `ndarray` + escalar/array |
| `numpy_indexing` | subscript sobre array con tupla/booleano |
| `pandas_series` | `pd.Series` |
| `pandas_dataframe` | `pd.DataFrame` |
| `groupby` | `.groupby(` |
| `apply` | `.apply(` |
| `merge_join` | `.merge(`/`.join(` |
| `pivot` | `.pivot_table(`/`.pivot(` |
| `fillna_dropna` | `.fillna(`/`.dropna(`/`.isnull(` |
| `str_accessor` | `.str.` |
| `map_filter_reduce` | `map(`/`filter(`/`reduce(` |
| `regex` | `import re` / `re.` |
| `file_io` | `open(`/`io.StringIO` |

> Para B, basta con recorrer `ast.walk` buscando `ast.Attribute`/`ast.Call`/`ast.Import`
> y mirar nombres. NO hace falta ejecutar el código.

### 1.4 Salida del endpoint
Añadir a la respuesta de `/prepare`:
```python
return jsonify(_json_safe({..., "concepts": _detect_concepts(code)}))
```
`concepts` = lista de `{clave, nombre, sesion, que, porque, lineas:[...]}` ordenada por
primera aparición en el código.

### 1.5 Cobertura mínima por sesión (para que sirva al examen)
Cubrir al menos un concepto de cada sesión S00–S16:
S00 tipos/operadores · S01 colecciones · S02 control de flujo · S03 comprensiones ·
S04 funciones/args · S05 ficheros · S06 POO/herencia/property · S07 estructuras/TDD ·
S08 NumPy/broadcasting · S09 Pandas básico · S10 Pandas avanzado (groupby/merge/pivot) ·
S11 visualización (datos) · S12 limpieza/regex/map-filter · S13 generadores ·
S14 NLP · S15 ML · S16 imágenes/NumPy.

---

## 2. UI: panel "Conceptos de la sesión" + animación

> **Nota de layout (actualizado):** la interfaz ya es de **2 columnas**:
> izquierda **"🐍 Código Python"** (editor arriba + ejecutor paso a paso abajo, con
> divisor `vDrag` arrastrable) y derecha **"🔍 Explicabilidad"** (narrador + print
> output + Frames + Objects). El nuevo panel de Conceptos debe ir en la **columna
> derecha (Explicabilidad)**, debajo del narrador o como pestaña junto a Frames/Objects.
> `autoLayout()` ya descuenta la altura del título y del narrador del lado derecho.

### 2.1 Nuevo panel
Añadir una sección en la **columna derecha (Explicabilidad)**, bajo el Narrador, titulada
**"🎓 Conceptos detectados"**. Al cargar/ejecutar código:
- Renderiza una **tarjeta por concepto** con: badge de sesión (p. ej. `S08`), nombre,
  el *qué* y un acordeón "¿Por qué en el examen?" con el *porque*.
- Animación de entrada escalonada (reutilizar `ob-pop` con `animation-delay:${i*60}ms`).

### 2.2 Sincronización con el narrador (animación con sentido)
Cuando el paso actual cae en una línea asociada a un concepto, **resaltar** la tarjeta
de ese concepto (glow) y mostrar en el narrador un sufijo opcional:
`📌 Asigna ... «x»  ·  concepto: Broadcasting (S08)`.
Esto conecta la animación paso a paso con el tema del curso → "entendimiento profundo".

### 2.3 Ubicación en el código
- CSS nuevo junto a `.nar-k-*` (clases `.concept-card`, `.concept-badge`, `.concept-why`).
- JS: `renderConcepts(concepts)` llamado desde `runCode().then(...)`; estado
  `let concepts=[]`. Resaltado desde `go(n)` comparando `step.line` con `c.lineas`.

---

## 3. Mejora del narrador: del *qué* al *por qué* (capa "insight")

Hoy `_explain_lines` dice "Crea una lista y la asigna a «pares»". Añadir, **opcional por
kind/concepto**, una segunda frase de *insight* didáctico:
- list_comprehension → "Equivale a un bucle for que va añadiendo a una lista."
- broadcasting → "NumPy alinea las formas y opera elemento a elemento sin bucle."
- groupby → "Agrupa filas por una clave y agrega cada grupo (split-apply-combine)."

Implementación: un dict `INSIGHTS = {concepto_o_kind: "frase"}`. En el frontend, el
narrador muestra el insight en una segunda línea más tenue cuando exista. **No romper**
la estructura `{text, kind}` actual: añadir campo opcional `insight` por línea solo
cuando aplique.

---

## 4. Más ejemplos "nunca vistos" + generador de ejemplos

### 4.1 Añadir 8–12 ejemplos nuevos (S12 y refuerzos)
Faltan ejemplos de **S12** (limpieza/regex/map-filter-reduce avanzado) y variantes nuevas.
Idea para que el usuario practique con código que el sistema explique solo:
- S12: `re.findall`/`re.sub` sobre texto, `map+filter+reduce` encadenados, normalización.
- S03: comprensión anidada (matriz) explicada celda a celda.
- S06: `__str__`/`__repr__`, `super()`, polimorfismo con lista heterogénea.
- S09/S10: `pd.cut`, `value_counts`, `sort_values`, `nlargest`.

### 4.2 Caja "pega tu código" como ciudadano de primera
El flujo de pegar código ya funciona; reforzarlo:
- Botón **"Explícame este código"** que ejecuta + abre el panel de Conceptos.
- Si el código usa una librería no instalada → mensaje claro (ya hay manejo de error).

---

## 5. Plan de implementación por fases (orden recomendado)

| Fase | Qué | Archivos/funciones | Tiempo |
|---|---|---|---|
| F1 | `CONCEPTS` dict + `_detect_concepts(code)` (solo estructurales A) | backend, junto a `_explain_lines` | 60–90 min |
| F2 | Reglas por API (B) + tabla de cobertura S00–S16 | backend | 45 min |
| F3 | Exponer `concepts` en `/prepare` + tests | endpoint | 20 min |
| F4 | Panel UI "Conceptos detectados" + CSS + `renderConcepts` | HTML/CSS/JS | 60 min |
| F5 | Resaltado sincronizado con `go(n)` + sufijo en narrador | JS | 30 min |
| F6 | Capa `INSIGHTS` (qué→por qué) | backend + narrador JS | 30 min |
| F7 | 8–12 ejemplos nuevos (¡con backslashes DOBLES!) | array `EX` + `<option>` | 45 min |
| F8 | Verificación completa (ver §7) | scripts de test | 30 min |

> Se puede entregar valor ya con **F1+F3+F4** (detectar y mostrar conceptos). El resto
> es refinamiento.

---

## 6. ⚠️ Errores del pasado a NO repetir (leer antes de empezar)

Estos ya nos costaron tiempo en este proyecto (guardados también en memoria):

1. **Backslashes en los ejemplos `EX`:** están dentro de template literals JS. TODA barra
   del código Python debe ir **DOBLE** (`\\n`, `\\d`, `\\.`). Si no, el navegador la
   destruye → "unterminated f-string" o regex roto (`version_num` = NaN). **Nunca** dejar
   `\n`/`\d` simples dentro de `EX`.
2. **Nombre de archivo del tracer:** mantener `USER_FILE = '<vis_user_code>'`. Si se vuelve
   a `'<string>'`, numpy/pandas colisionan y dan falso "Step limit 500 reached".
3. **NaN/Infinity:** todo lo que vaya a `jsonify` debe pasar por `_json_safe`. El navegador
   rechaza tokens `NaN`/`Infinity` aunque Python los acepte.
4. **Testing fiel al navegador (OBLIGATORIO):** (a) extraer `EX` con **Node** (`eval`) para
   interpretar los escapes como el navegador; (b) parsear las respuestas con **JSON
   estricto** (`parse_constant` que lanza) para detectar NaN. `json.loads` normal de Python
   da falsos OK.
5. **Límite de 500 steps:** sklearn real lo supera; usar Python puro o datasets diminúsculos.
   Cuidado con bucles dobles sobre arrays grandes.
6. **Flask ordena claves:** mantener `app.json.sort_keys = False`.
7. **Cada `kind`/concepto nuevo** debe tener icono (`NAR_ICO`) y color CSS si se muestra.
8. Validar siempre el JS extrayendo `<script>` y corriendo `node --check`.

---

## 7. Criterios de aceptación / verificación

Antes de dar por terminada la mejora:

- [ ] `node extract_ex.js` regenera `ex_interpreted.json` sin error.
- [ ] **Test estricto navegador**: los 40 + nuevos ejemplos → `0 FAIL`.
- [ ] **Verificación profunda**: cada paso narrado, frames presentes, output monótono,
      último step `line==-1`.
- [ ] `_detect_concepts` probado con **5 snippets nuevos no presentes en EX** (p. ej. una
      comprensión anidada, un `groupby().agg()`, un generador con `yield`, broadcasting,
      una clase con `@property`) → detecta el concepto correcto y la sesión correcta.
- [ ] Panel de Conceptos se renderiza, anima en escalera, y se resalta al pasar por la
      línea asociada.
- [ ] Ningún `kind`/concepto sin icono o sin color.
- [ ] `node --check` del bloque `<script>` → OK; `python -c "import ast; ast.parse(...)"` → OK.

### Scripts de verificación
Se escribieron y usaron esta sesión (`extract_ex.js`, `test_strict_json.py`,
`deep_verify.py`, arneses Node del Modo Maestro/Reto) pero se guardaron en `%TEMP%`
y se borraron al limpiar — **hay que recrearlos dentro del repo** (ver §9 abajo,
es el primer pendiente de mañana). Ver también la memoria
`feedback-headless-verification-harness`.

---

## 8. Idea opcional (si sobra tiempo): Modo Examen

Un toggle "Modo Examen" que, dado un ejemplo, **oculta el output** y pide al usuario
predecir el resultado antes de revelarlo paso a paso. Mini-quiz de 1 pregunta por
concepto detectado ("¿qué imprime esta línea?"). Refuerza el estudio activo.

---

## 9. Sesión 2026-07-28 — resumen y pendientes para mañana

### Qué se hizo
- **Práctica 1 y 2 en el temario**: 8 ejemplos nuevos (`EX[40..47]`) adaptados de
  los notebooks reales de Lucas, offline (sin red/CSV externo) para poder
  trazarlos: frange (2 variantes), Ciudades en Florida, RLE (iterativo +
  recursivo), sort_by/categorizar/pivot_table de pandas.
- **🎓 Modo Maestro**: recorre los 48 temas (S00–S16 + P1 + P2) a ritmo del
  alumno, con progreso persistido en `localStorage`.
- **✍️ Reto de código**: por cada tema, editor CodeMirror (vendorizado por CDN)
  que reta a escribir la solución — modo `fill` (rellenar función/clase vaciada,
  22/48 temas) o `blank` (reescritura completa, 26/48 temas). Backend
  `_build_challenge()` + ruta `/challenge` (AST puro). Evalúa por `assert` si
  existe, si no por diff exacto de la salida impresa contra la referencia.
- **4 bugs reales encontrados y corregidos** (detalle completo en la memoria
  `feedback-master-mode-bugs`, léela antes de tocar esta parte):
  1. Orden de imports roto al reconstruir el stub (`class Figura(ABC)` con el
     import después → `NameError`) — corregido preservando el orden original.
  2. Autocompletado se autodisparaba en cada tecla y corrompía el código
     escrito (`show-hint.js` usa Enter/Tab para "aceptar sugerencia") —
     corregido: autocompletado solo bajo demanda (`Ctrl-Space`).
  3. El popup de autocompletado quedaba tapado por el z-index del modal —
     corregido forzando `.CodeMirror-hints{z-index:10000}`.
  4. Falso positivo: un código que imprime todo bien y LUEGO revienta con un
     error se marcaba "correcto" (la comparación ignoraba `d.error`) —
     corregido, ahora un error siempre invalida el resultado.

### Pendiente para mañana (en orden sugerido)
1. **Recrear los scripts de verificación dentro del repo** (no `%TEMP%`) —
   `extract_ex.js`, `test_strict_json.py`, `deep_verify.py`, y los arneses Node
   del Modo Maestro/Reto (patrón: `vm` + DOM stub + `fetch` real contra
   `localhost:5000`, ver memoria `feedback-headless-verification-harness`).
2. **Verificación visual manual en navegador real** (nunca hecha en esta
   sesión: no hay navegador disponible en este entorno) — abrir
   `http://localhost:5000`, probar el Modo Maestro y el Reto de código de
   punta a punta, y en particular el autocompletado (`Ctrl-Space`) a ojo.
3. Evaluar si sigue interesando la idea original de §1 (capa de "Conceptos del
   curso" — detectar y explicar a qué tema del temario pertenece cualquier
   código pegado) — quedó sin implementar, todo lo de hoy fue sobre Modo
   Maestro/Reto en su lugar.
4. Posible mejora del Reto: los 26 temas en modo `blank` solo se evalúan por
   diff exacto de salida — considerar agregarles `assert` explícitos (como
   tienen los de Práctica 1/2) para una evaluación más robusta que la
   comparación de texto.
5. Revisar si conviene cachear la respuesta de `/challenge` en `localStorage`
   además de en memoria (hoy se re-pide cada vez que se reabre el navegador).

---

*Generado para la sesión de estudio de Lucas. Las sesiones del curso provienen de
`MAESTRO_Python_IA.ipynb` (S00–S16). Mantener este plan actualizado al avanzar.*

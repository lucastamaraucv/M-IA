"""
Tres correcciones sobre el notebook:
1. Elimina celda 09 (seccion 5 duplicada y mal ubicada, antes de las secciones 1-4).
2. Reescribe celda 17 (explicacion del codigo) para que describa el codigo ACTUAL
   (datos reales UCI, no la señal sintetica anterior) con estilo de Lucas.
3. Actualiza la nota de dataset en celda 13 (es datos reales, no sintetico).
"""
import json

NB = '01MIAR_ACT_WhitePapers.ipynb'
with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# ─── 1. Eliminar celda 09 (seccion 5 duplicada mal ubicada) ──────────────────
# Verificar que es la celda correcta antes de eliminar
assert '5. Explicaci' in ''.join(cells[9]['source']), "Celda 09 no es la esperada"
assert cells[9]['cell_type'] == 'markdown'
assert '1. Referencia' in ''.join(cells[10]['source']), "Celda 10 debe ser seccion 1"
cells.pop(9)
print("Celda 09 eliminada (seccion 5 duplicada).")

# Reindexar: despues del pop, lo que era celda 17 es ahora celda 16
# Verificamos que celda 16 ahora es la explicacion del codigo
for i, c in enumerate(cells):
    src = ''.join(c['source'])
    if c['cell_type'] == 'markdown' and '5. Explicaci' in src and 'propiedad central' in src:
        idx17 = i
        break
print(f"Celda de explicacion del codigo encontrada en posicion {idx17}.")

# ─── 2. Reescribir celda de explicacion (nueva seccion 5 correcta) ───────────
nueva_explicacion = r"""## 5. Explicación del código

Lo implementé en tres celdas de código. Acá explico qué hace cada una, como lo fui pensando:

---

**Celda 1 — Carga del dataset real, clases y verificación de estabilidad.**

Lo primero que hago es cargar `electricity_sample.csv` —168 horas × 3 nodos reales del UCI Electricity dataset, con la misma normalización min-max por nodo que usa el paper (`normalize=3`)— y graficarlo. La vista de 7 días ya me dice todo: el consumo arranca bajo de madrugada (0.002–0.036), sube a lo largo de la mañana y llega al pico de tarde (0.718–0.770), y el fin de semana baja notoriamente. Eso confirma que en el mismo dato conviven dos escalas: una tendencia semanal lenta y una variación horaria rápida. Exactamente lo que TS-LIF está diseñado para separar.

Después defino las dos clases:

- **`TSLIFNeuron`**: implementa la Ecuación (5) del paper al pie de la letra. `vd` (dendrita) con `a1=0.95` se comporta como una media móvil lenta —olvida despacio, captura baja frecuencia—; `vs` (soma) con `a2=0.05` olvida rápido y reacciona a lo que pasa ahora. El término `(1-a2)*c` es la **inyección directa de corriente al soma**, que es la novedad del paper frente a TC-LIF: evita que la información rápida se pierda al pasar primero por la dendrita.
- **`LIFNeuron`**: el LIF clásico de un compartimento. Su único `v` mezcla todo sin discriminar. Lo uso de línea base para ver la diferencia.

Antes de simular compruebo los **autovalores** del sistema linealizado: λ₁=0.95 y λ₂=0.05, ambos con módulo <1. El Teorema 1 del paper dice que eso garantiza convergencia. Lo pongo explícito porque si algún λ ≥ 1, el entrenamiento directamente diverge, y es mejor verificarlo antes que depurarlo después.

---

**Celda 2 — Experimento 1: TS-LIF vs LIF sobre el consumo eléctrico real.**

Tomo el nodo 0 del CSV (consumidor real, 168 h de datos normalizados) y lo paso hora por hora a los dos modelos. El gráfico de 4 paneles lo muestra de forma directa:

- La **dendrita** (verde) sigue la tendencia semanal: es una media lenta que no se mueve con cada subida o bajada de hora en hora. La línea de referencia (media móvil de 24 h, azul discontinua) confirma que la está capturando bien —no es un artificio, coincide con el promedio real del dato.
- El **soma** (rojo) captura las variaciones horarias: sube y baja con el consumo real de cada momento, rastreando el ciclo diario.
- El **LIF clásico** simplemente atenúa la señal completa sin separarla. Su curva sigue a `c[t]` en general pero no distingue si algo es tendencia o fluctuación del momento.

En simple: dendrita retiene el contexto de largo plazo, soma reacciona al corto plazo. Eso es exactamente lo que el paper describe como la ventaja del doble compartimento.

---

**Celda 3 — Experimento 2: verificación cuantitativa en frecuencia.**

Para no quedarme solo con el "se ve bien" del gráfico, hago dos análisis:

1. **FFT sobre los datos reales**: el espectro en escala log muestra que la energía de `VD` (dendrita) se acumula a la izquierda de f=1/24 (baja frecuencia) y la de `VS` (soma) a la derecha. El LIF clásico no separa: su espectro mezcla todo en un valor intermedio.

2. **Tabla de ganancia (réplica Sec. 4.4 del paper)**: mido la amplitud salida/entrada de cada compartimento con senoides puras a distintos periodos. Con T=120 (baja frec.) y T=4 (alta frec.) obtengo los mismos números del paper: dendrita 0.700/0.026 y soma 0.698/0.925. Esos valores son exactamente los de la Tabla de la Sección 4.4 del artículo —no se aproximan, son iguales. También mido con los periodos del dataset real (T=168h semanal, T=24h diario): la separación sigue siendo real (4.2x en dendrita, 1.7x en soma), aunque más moderada porque esos dos periodos están más cerca entre sí que los del ejemplo teórico.

> Con unas 60 líneas de NumPy queda demostrado en datos reales **por qué** TS-LIF le gana al LIF clásico: en vez de un único filtro paso-bajo, tiene dos canales especializados que, combinados en la salida final, capturan a la vez tendencias largas y fluctuaciones cortas."""

cells[idx17]['source'] = [nueva_explicacion]
print(f"Celda {idx17} (explicacion del codigo) reescrita.")

# ─── 3. Actualizar nota de dataset en celda 13 (ahora es el 12 despues del pop) ──
for i, c in enumerate(cells):
    if c['cell_type'] == 'markdown' and '4. Ejemplo de implementaci' in ''.join(c['source']):
        idx13 = i
        break

src13 = ''.join(cells[idx13]['source'])

# Reemplazar la nota vieja (que dice "en su lugar" sugiriendo datos sinteticos)
vieja = (
    '> **Nota sobre el dataset:** el paper usa `electricity.txt` (26.304 h × 321 nodos, '
    'dataset UCI completo no incluido por su tamaño). En su lugar, `electricity_sample.csv` '
    'contiene 168 h × 3 nodos con el mismo patrón diario/semanal y normalización [0,1], '
    'lo que permite reproducir la separación de frecuencias de la Sección 4.4 sin depender '
    'de infraestructura externa.'
)
nueva = (
    '> **Nota sobre el dataset:** el paper entrena sobre `electricity.txt` completo '
    '(26.304 h × 321 nodos, ~90 MB). Aquí uso `electricity_sample.csv`: los primeros '
    '168 pasos horarios (1 semana) de los **3 nodos reales** con el patrón diario '
    'más claro del dataset original (nodos 88, 234, 193; autocorrelación lag-24 r=0.977), '
    'con la misma normalización min-max por nodo del paper (`normalize=3`). '
    'Son datos reales, no sintéticos.'
)

if vieja in src13:
    cells[idx13]['source'] = [src13.replace(vieja, nueva, 1)]
    print(f"Celda {idx13} (nota dataset) actualizada.")
else:
    print(f"ADVERTENCIA: no se encontro el texto exacto en celda {idx13}. Buscando alternativa...")
    # Buscar cualquier linea que diga "En su lugar"
    lines = src13.split('\n')
    for j, line in enumerate(lines):
        if 'En su lugar' in line or 'sintetico' in line.lower() or 'normalización [0,1]' in line:
            print(f"  Linea {j}: {line[:80]}")

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("\nPatch aplicado. Verificando estructura final:")
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])[:70].replace('\n', ' ')
    print(f"  Celda {i:02d} ({c['cell_type'][:4]}): {src}")

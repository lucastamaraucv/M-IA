# Resumen del curso — 03MIAR Algoritmos de Optimización

Orden real: Tutoría Inicial → VC1(Ses.02) → VC2(Ses.03) → AG1(Ses.04) → VC3(Ses.05) → VC4(Ses.06) → AG2(Ses.07) → VC5(Ses.08) → AG3(Ses.09) → VC6(Ses.10) → AG3 2ª parte(Ses.12). VC = videoconferencia teórica; AG = actividad guiada práctica en Python (Colab) sobre la VC anterior.

## 0. Tutoría inicial — estructura y evaluación

No es curso de programación ni colección de recetas: el objetivo es entender POR QUÉ una técnica funciona o falla para un problema concreto, para poder adaptarla a problemas nuevos.

Objetivos: teoría de algoritmos de optimización, coste/complejidad (AG); técnicas de diseño en Python (AG); enfrentar un problema real (Trabajo Práctico).

Evaluación: Portafolio 60% (Trabajo Práctico 30%*, Actividades Guiadas 10%*, artículo científico 10%*, Foro 10%) + Prueba final 40%*. (*) obligatorio aprobar cada apartado marcado. Examen: 1h, 20 preguntas test (acierto +0.5, fallo −0.165, blanco 0) + 2 de desarrollo. Foro: 2 aportaciones mínimo. AG: entrega en PDF, GitHub asegura 8/10.

Sesiones: VC1 Introducción; VC2 Diseño de algoritmos/Ordenación; VC3 Problemas tipo/Búsqueda; VC4 Descenso del gradiente; VC5 Heurísticos; VC6 Evolutivos/Genéticos. AG1: ordenación, voraces, backtracking, divide y vencerás, PD. AG2: ramificación y poda + descenso del gradiente (**no** BFS/DFS pese al índice oficial — eso está en VC3). AG3(I): búsqueda local, tabú, recocido simulado, GRASP. AG3(II): ACO, algoritmos genéticos.

Repaso matemático anunciado (sin desarrollar aquí): estructuras de datos, estadística básica, combinatoria, derivadas/gradiente/Hessiana. **La matriz Hessiana nunca se desarrolla con fórmulas en ningún PDF del curso**; solo se trabaja el gradiente (derivadas parciales primeras).

## 1. VC1 — Introducción a los algoritmos

**Algoritmo**: "conjunto de reglas ordenadas y finitas para realizar una actividad mediante la sucesión de pasos claramente establecidos". Un algoritmo probabilista no siempre da la misma solución, pero sus pasos siguen bien definidos.

Historia: al-Juarismi (780-850, origen de la palabra); Algoritmo de Euclides (m.c.d(m,n)=m.c.d(n,resto(m,n)) hasta resto 0; ej. mcd(60,24)=12; pseudocódigo `while n≠0: r←m mod n; m←n; n←r; return m`); Criba de Eratóstenes (primos hasta n marcando múltiplos desde 2 hasta √n).

**Tipos**: por cómo calculan — Deterministas (misma solución siempre) / Probabilistas (pueden variar). Por tipo de solución — Exactos (óptimo), Aproximados (buena solución con aproximación conocida al óptimo), Heurísticos (buena solución, sin poder determinar si es óptima). La 1ª mitad del curso (D&V, Voraz, Backtracking, PD) = técnicas exactas deterministas; la 2ª mitad (metaheurísticas, genéticos) = heurísticas, muchas probabilistas.

**Propiedades**: Finitud (termina en pasos finitos); Precisión (sin ambigüedad). Partes: Entrada → Proceso → Salida.

**Optimización**: "obtención del mejor valor para una función objetivo dentro de un dominio de soluciones posibles". Componentes: función objetivo (medida de bondad), variables (decisiones), restricciones (relaciones a cumplir). Resolver = hallar variables que optimizan la función objetivo cumpliendo restricciones. Optimización multiobjetivo: varias funciones objetivo en conflicto → no hay una única solución sino un conjunto donde ninguna domina a las demás en todo (**Óptimo/frente de Pareto**): una solución está en el frente si no existe otra al menos igual de buena en todo y estrictamente mejor en algo.

**Modelar/Diseñar/Analizar**: Modelar = determinar supuestos, datos y estructura de datos ("no siempre se puede ajustar al 100% a la realidad"); riesgo por exceso de realismo (modelo muy complejo) o por defecto (solución no se corresponde con la realidad) — buscar compromiso. Diseñar = aplicar técnicas conocidas. Analizar = contar operaciones. Tipos de modelo: icónico/analógico/simbólico/matemático; predictivo/evaluativo/optimización; determinista/estocástico; estático/dinámico; lineal/entero/no lineal. Fases: Conceptualización → Formalización → Evaluación.

**Ejemplo modelado — autobuses urbanos**: mínimo de autobuses para cubrir demanda en 6 tramos de 4h, cada autobús trabaja máx. 8h SEGUIDAS de 24h. Demanda por tramo: 4,8,10,7,12,4. Variables Xⱼ = autobuses que EMPIEZAN turno en tramo j (j=1..6). FO: Min ΣXⱼ. Restricciones (cada una = suma de los 2 turnos que cubren ese tramo ≥ demanda): X1+X2≥8, X2+X3≥10, X3+X4≥7, X4+X5≥12, X5+X6≥4, X1+X6≥4, todas enteras ≥0. Clave: como cada bus cubre 2 tramos consecutivos de 4h, las restricciones combinan siempre PARES consecutivos, no cada tramo aislado.

**Complejidad temporal**: depende de tamaño de entrada n, calidad del código, procesador, complejidad del algoritmo. Operaciones elementales (OE): aritméticas, asignaciones, condiciones/llamadas/retornos, accesos a estructuras. **O(f)**: tiempo de ejecución acotado (salvo constante) por f para todo n desde un n₀ — importa cómo CRECE, no el conteo exacto; 3n³+2n+7 y n³ son ambos O(n³).

Tabla de órdenes (menor a mayor): O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(nᵃ) < O(2ⁿ) < O(n!).

| n | log n | n² | 2ⁿ | n! |
|---|---|---|---|---|
| 2 | 1 | 4 | 4 | 2 |
| 8 | 3 | 64 | 256 | 40.320 |
| 32 | 5 | 1.024 | 4,3×10⁹ | 2,6×10³⁵ |
| 100 | 6 | 10⁴ | 1,2×10²⁷ | 9,3×10¹⁷⁷ |

Ejemplo: intersección de listas A(n)/B(m) con doble bucle anidado → 2(m·n)+n+2 operaciones → O(n²) (término dominante). Las constantes SÍ importan para n pequeño (O(n³) constante 5 puede ganarle a O(n²) constante 10⁷ hasta cierto n), pero asintóticamente el de menor orden siempre gana. Viajante: 4 ciudades → 3!=6 rutas; 532 ciudades → 531! rutas ("se necesita otra estrategia").

## 2. VC2 — Diseño de algoritmos y ordenación

Agenda: ordenación; técnicas voraces y grafos (Prim/Kruskal); vuelta atrás; divide y vencerás; programación dinámica (introducción; se profundiza con código en AG1).

**Ordenación** (obtener máx/mín de lista = O(n); intercambiar = O(1)):
- **Inserción**: construye sub-lista ordenada iterando. O(n) mejor caso, O(n²) peor caso. Bueno para listas pequeñas/parcialmente ordenadas.
- **Burbuja**: intercambia adyacentes reduciendo el tramo a revisar; mejorable deteniéndose si no hay intercambios (sin Big-O explícito en el PDF).
- **Selección**: busca máx/mín en cada iteración y lo coloca. O(n²) siempre (sin caso favorable).
- **Merge Sort**: divide recursivamente en 2 mitades EXACTAS y combina (D&V). O(n log n) SIEMPRE, en todos los casos.
- **Quick Sort**: divide según un pivote (menores/mayores) y combina (D&V). O(n²) peor caso, O(n log n) mejor/promedio; el caso favorable depende de la elección del pivote (si es sistemáticamente el mínimo/máximo, degenera a O(n²)), no de los datos.

Aplicaciones: búsquedas, mediana, par más cercano, outliers, duplicados, compresión, planificación, simulaciones.

**Divide y Vencerás**: "dividir el problema recursivamente en subproblemas más pequeños similares al original o sencillos". Aplicaciones: mergesort, quicksort, Strassen, subsecuencia de suma máxima, par de puntos más cercanos, superficies ocultas 3D, calendario de liga. Ejemplo guía: Torres de Hanoi (desarrollado en AG1).

**Técnica Voraz**: "elegir en cada etapa la decisión óptima/más ambiciosa sin considerar consecuencias; las decisiones descartadas se descartan para siempre". Esquema:
```
S = Ø
while (S no es solución y C ≠ Ø):
    x = selección(C); C = C - {x}
    if S∪{x} es factible: S = S∪{x}
return S si es solución, si no "No se encontró solución"
```
Problema guía: cambio de monedas (candidatos=combinaciones, selección=tomar tantas del mayor valor sin pasarse, factibilidad=valor acumulado, FO=minimizar nº monedas). Condiciones para que funcione: debe existir el valor 1, monedas infinitas; no es eficiente en todo sistema monetario (contraejemplo [1,5,11] con C=15, desarrollado en AG1).

**Grafos — árbol de recubrimiento mínimo**: Grafo=(V,A); dirigido si (u,v)≠(v,u); conexo si todos conectados; ponderado si aristas tienen valor; árbol = subconjunto de aristas que conecta todos los nodos sin ciclos. Árbol de recubrimiento mínimo = árbol del grafo ponderado con todos los vértices y peso mínimo (suma de aristas).
- **Prim**: en cada paso, arista de menor coste que une el subconjunto seleccionado con el no seleccionado; ese vértice pasa a seleccionados. O(n²) siempre.
- **Kruskal**: ordena aristas por coste y las selecciona evitando ciclos. O(a·log n) (a=aristas, n=vértices). Con muchas aristas (~n²) se acerca a O(n²·log n), peor que Prim; con pocas (~n), mejor que Prim.
Ambos son VORACES y aun así garantizan el óptimo global (excepción a que la voracidad no siempre funciona). Aplicaciones: redes, rutas, finanzas, clustering.

**Vuelta atrás / Backtracking**: "construcción sistemática por etapas de todas las soluciones posibles representables como tupla (x1,...,xn), cada xi explorable en la etapa i-ésima; árbol de expansión modela el espacio de soluciones". Eficiencia en general mala (O(2ⁿ)) salvo mejoras para evitar explorar en profundidad (ramificación y poda). La función de descarte debe ser barata; conviene identificar restricciones IMPLÍCITAS, no solo explícitas.

Ejemplo N-Reinas (4x4): tabla combinaciones(n!) vs soluciones válidas — n=4: 24 combinaciones/2 soluciones; n=8: 40.320/92; n=12: 479.001.600/14.200 (justifica la poda: la fracción válida se achica al crecer n). Modelado: tupla (x1..x4), xi=fila de la reina en columna i. Misma fila si hay valores repetidos en la tupla; misma diagonal si |xi−xj|=|i−j|.

**Programación Dinámica**: "dividir el problema en subproblemas más pequeños, guardando soluciones para reutilizar". Debe cumplirse el principio de optimalidad de Bellman (en una secuencia óptima, toda sub-secuencia también es óptima); vigilar complejidad ESPACIAL. Ojo: tener óptimos de subproblemas no garantiza poder combinarlos sin más para el óptimo global — hay que definir bien la recurrencia. Ejemplo guía: viaje por el río, n embarcaderos, tarifa directa T(i,j), a veces conviene trasbordo intermedio k: `C(i,j) = min{ T(i,j), T(i,k)+C(k,j) para todo i<k≤j }` (desarrollado con código en AG1 como P(i,j)).

## 3. AG1 — Las 4 técnicas clásicas, en profundidad y con código

**Divide y Vencerás — Torres de Hanoi**. Requisitos: subproblemas de igual naturaleza, resolubles recursivamente/caso simple, combinables, **DISJUNTOS entre sí (sin solapamiento — esto distingue D&V de PD)**, la recursión debe terminar.
```python
def torres_hanoy(N, desde, hasta):
    if N==1:
        print("LLevar desde " + str(desde) + " hasta " + str(hasta))
    else:
        torres_hanoy(N-1, desde, 6-desde-hasta)
        print("LLevar desde " + str(desde) + " hasta " + str(hasta))
        torres_hanoy(N-1, 6-desde-hasta, hasta)
torres_hanoy(4,1,3)
```
("6-desde-hasta" calcula la torre auxiliar sin variable extra, ya que 1+2+3=6). Recurrencia: T(1)=1; T(n)=1+2·T(n-1) = 2ⁿ−1. Complejidad **O(2ⁿ)**.

**Técnica Voraz — Cambio de monedas**. Elementos: candidatos, solución parcial, función selección, FO, factibilidad, criterio final.
```python
def cambio_monedas(CANTIDAD, SISTEMA):
    SOLUCION = [0 for i in range(len(SISTEMA))]
    VALOR_ACULULADO = 0
    for i in range(len(SISTEMA)):
        monedas = int((CANTIDAD-VALOR_ACULULADO)/SISTEMA[i])
        SOLUCION[i] = monedas
        VALOR_ACULULADO += monedas * SISTEMA[i]
        if VALOR_ACULULADO == CANTIDAD: return SOLUCION
    return SOLUCION
# SISTEMA=[25,10,5,1]; cambio_monedas(27,SISTEMA) -> [1,0,0,2]
```
Contraejemplo donde falla: sistema [11,5,1], N=15 → voraz da [1,0,4] (5 monedas: 1×11+4×1), pero el óptimo es 3 monedas de 5 (5+5+5=15). El voraz nunca reconsidera una decisión ya tomada.

**Vuelta atrás — N-Reinas**. Modelo: solución=tupla, xi=fila de la reina en columna i.
```python
def reinas(N, solucion=[], etapa=0):
    if len(solucion) == 0:
        solucion=[0 for i in range(N)]
    for i in range(1, N+1):
        solucion[etapa] = i
        if es_prometedora(solucion, etapa):
            if etapa == N-1:
                print("La solución es:", solucion)
            else:
                reinas(N, solucion, etapa+1)
        solucion[etapa] = 0

def es_prometedora(SOLUCION, etapa):
    for i in range(etapa+1):
        if SOLUCION.count(SOLUCION[i]) > 1:
            return False
        for j in range(i+1, etapa+1):
            if abs(i-j) == abs(SOLUCION[i]-SOLUCION[j]): return False
    return True
```
`es_prometedora` es O(n²) por nodo, pero el nº total de nodos del árbol completo es exponencial; la poda evita visitarlos todos. Vuelta atrás en general es Exponencial.

**Programación Dinámica — Viaje por el río**. Tabla T(i,j) de tarifas directas (999/inf si no hay conexión directa); tabla P(i,j) de óptimos parciales: `P(i,j) = min{ T(i,j), P(i,k)+T(k,j) para todo i<k≤j }`.
Ejemplo con 7 embarcaderos (0-6): 0→1=5, 0→2=4, 0→3=3, 1→3=2, 1→4=3, 1→6=11, 2→3=1, 2→5=4, 2→6=10, 3→4=5, 3→5=6, 3→6=9, 4→6=4, 5→6=3.
```python
TARIFAS = [
[0,5,4,3,999,999,999],
[999,0,999,2,3,999,11],
[999,999,0,1,999,4,10],
[999,999,999,0,5,6,9],
[999,999,999,999,0,999,4],
[999,999,999,999,999,0,3],
[999,999,999,999,999,999,0]]

def Precios(TARIFAS):
    N = len(TARIFAS[0])
    PRECIOS = [ [9999]*N for i in [9999]*N ]
    RUTA = [ [""]*N for i in [""]*N ]
    for i in range(N-1):
        for j in range(i+1, N):
            MIN = TARIFAS[i][j]
            RUTA[i][j] = i
            for k in range(i, j):
                if PRECIOS[i][k] + TARIFAS[k][j] < MIN:
                    MIN = min(MIN, PRECIOS[i][k] + TARIFAS[k][j])
                    RUTA[i][j] = k
            PRECIOS[i][j] = MIN
    return PRECIOS, RUTA
```
3 bucles anidados de tamaño n → **O(n³)** (vs. exponencial de fuerza bruta/backtracking: PD calcula la tabla de abajo hacia arriba, sin recursión). Reconstrucción de ruta (recursiva, a partir de la tabla RUTA):
```python
def calcular_ruta(RUTA, desde, hasta):
    if desde == hasta:
        return desde
    else:
        return str(calcular_ruta(RUTA, desde, RUTA[desde][hasta])) + ',' + str(RUTA[desde][hasta])
```
(el cálculo de P es iterativo; solo la reconstrucción del camino es recursiva).

Otro ejemplo D&V: par de puntos más cercanos (1D/2D/3D), comparando fuerza bruta vs. D&V.

## 4. VC3 — Problemas tipo y algoritmos de búsqueda

Agenda: Programación lineal; PL entera; Agente Viajero (TSP); mochila; otros problemas; BFS; DFS; Ramificación y Poda.

**Programación lineal**: optimizar una función objetivo LINEAL (continua) y multivariable sobre restricciones lineales (igualdades/desigualdades). Método Simplex (Dantzig, 1949): recorre iterativamente los vértices de la región factible hasta el óptimo (disponible en Excel Solver). Problemas tipo: dieta (Stigler), transporte (Koopmans 1949), producción, flujo, inventario, cartera, planificación, asignación de recursos.

**PL entera**: algunas/todas las variables enteras (puros/mixtos). "No existe un algoritmo específico"; resolver la relajación continua y redondear es **MALA opción** (el redondeo puede ser no factible o alejarse del óptimo entero). Alternativas: Ramificación y Poda, heurísticos. Problemas: inversión de capital/cartera, coste fijo, cubrimiento de conjuntos.

**TSP (Agente Viajero)**: formulación Dantzig-Fulkerson-Johnson (1954): xᵢⱼ=1 si se visita j justo tras i; min Σcᵢⱼxᵢⱼ; restricciones de grado + eliminación de sub-recorridos (~2ⁿ restricciones). Formulación Miller-Tucker-Zemlin (1960): mejora a ~n² restricciones con variables auxiliares uᵢ. **NP-difícil**: no hay algoritmo polinomial. Nº de rutas = (n-1)!/2; con 20 ciudades ≈6×10¹³ rutas. Resolución: fuerza bruta (inviable), exactos (ramificación y poda), heurísticos. VRP = variante multi-vehículo, mismas técnicas.

**Camino más corto** (no confundir con TSP: entre 2 nodos, no visitar todos): elección según pesos negativos, densidad del grafo, un origen vs. todos los pares.
- **Dijkstra**: desde un origen a todos los demás; NO válido con costes negativos.
- **Bellman-Ford**: más lento que Dijkstra; válido con costes negativos.
- **Floyd-Warshall**: entre TODOS los pares de vértices.

**Búsqueda A***: variación de búsqueda en amplitud con heurística: f(n)=g(n)+h(n) (g=coste real recorrido, h=estimación heurística restante). Ejemplo 8-puzzle: heurísticas = fichas mal colocadas, o distancia Manhattan total. Heurística (Feigenbaum/Feldman): "regla para engañar, simplificar o cualquier ardid que limita drásticamente la búsqueda en grandes espacios de estados".

**BFS/DFS**: "técnicas que buscan uno o varios elementos con ciertas propiedades en una estructura de datos".
- BFS (amplitud): 1) cola con el elemento raíz; 2) si el primero de la cola es solución, terminar; 3) si no, quitarlo y añadir sus hijos al FINAL de la cola; 4) si cola vacía sin solución, no hay; repetir 2.
- DFS (profundidad): igual pero los hijos se añaden al PRINCIPIO de la cola (como pila). BFS recorre nivel a nivel (camino más corto en pasos, grafos sin peso); DFS se hunde por una rama antes de retroceder.
- Ascenso de colina (hill climbing): variante de DFS con heurística para ordenar los hijos, misma fórmula f(n)=g(n)+h(n).
- Ejemplo 8-puzzle: ojo, hay disposiciones iniciales sin solución (la mitad de los casos).

**Ramificación y Poda (Branch and Bound)**: 3 etapas — selección del nodo pendiente más prometedor, ramificación (generar hijos), poda (descartar hijos que no pueden mejorar lo ya encontrado). Notación: CI(s)=cota inferior, CS(s)=cota superior, BE(s)=beneficio esperado; CI(s)≤Valor(M)≤CS(s). Regla de poda: podar nodo i si CS(i)≤CI(j) para algún j ya generado (C = máximo de cotas inferiores/soluciones ya encontradas; se poda i si CS(i)≤C). Es mejora de Vuelta Atrás; no hace falta guardar todo el árbol, solo nodos "vivos"; también aplicable a juegos con adversario (MinMax: minimizar la pérdida máxima asumiendo que el rival juega su mejor movimiento contra ti; poda alfa-beta descarta ramas que no serán buenas para ningún jugador).

**Mochila (Knapsack)**: elegir subconjunto de objetos (valor v, peso w) maximizando valor sin superar capacidad M. `Max: Σxᵢvᵢ  s.a. Σxᵢwᵢ≤M, xᵢ∈{0,1}`. Resoluble como PL entera; PD y Vuelta atrás son O(2ⁿ); hay heurísticos; **la Técnica Voraz NO funciona**. Contraejemplo: mochila 6kg, objeto A=5kg/11€, dos objetos B=3kg/6€ c/u — voraz elige A (11€, sobran 1kg sin uso); óptimo es los 2 B (6kg exactos, 12€). Problema similar: suma de subconjuntos. Aplicaciones: finanzas, transporte de cargas, corte de materiales, robótica.

Otros problemas: satisfacibilidad booleana (SAT), asignación de tareas a agentes (desarrollado en AG2), coloreado de grafos.

## 5. VC4 — Descenso del gradiente y complejidad P/NP

**Gradiente**: función diferenciable = derivable en n dimensiones. ∇f(r) = (∂f/∂x₁,...,∂f/∂xₙ), vector de derivadas parciales (campo vectorial). Ejemplo: f(x,y)=x²+2x+y²+y³+xy → ∇f=(2x+y+2, 2y+3y²+x). El gradiente apunta a la dirección de mayor crecimiento; para minimizar, moverse en dirección CONTRARIA. **La matriz Hessiana nunca se desarrolla con fórmulas en el curso.**

**Convexidad**: descenso del gradiente (AGD) es un algoritmo iterativo para hallar mínimos de funciones multivariable convexas y diferenciables; la convexidad garantiza que el óptimo hallado es GLOBAL, no solo local. (Si la función es cóncava y se buscan mínimos, trabajar con −f(x)).

**Algoritmo**: `pₜ₊₁ = pₜ − αₜ·∇f(pₜ)`. αₜ (tasa de aprendizaje) debe garantizar factibilidad y mejora; muy pequeña → exceso de iteraciones; muy grande → puede no converger/oscilar. Buena estrategia: reducir αₜ dinámicamente (según magnitud del gradiente o nº de iteraciones). Diagrama: x⁰ inicial → comprobar |∇f(xᵏ)|<ε → si no, sᵏ=∓∇f(xᵏ)/|∇f(xᵏ)|, optimizar f(xᵏ+λsᵏ) hallando λᵏ, xᵏ⁺¹=xᵏ+λᵏsᵏ, repetir → al parar, evaluar FO en el óptimo.

**Clasificación/variantes**: minimizar error entre predicción y valor real (función de coste: error cuadrático medio en regresión lineal —diferenciable—; entropía cruzada en clasificación binaria/imágenes). Hiperplano separador: mejor recta/plano que separa clases, priorizando mayor distancia a ambos conjuntos; si ninguna recta separa bien, puede servir una función no lineal (ej. f(x,y)=x²+y² separa un grupo central rodeado de otro).

3 variantes según volumen de datos por iteración:
- **Batch**: todos los puntos cada iteración. Directo pero muy lento.
- **Estocástico**: un solo punto cada iteración. Rápido pero muy disperso.
- **Mini-batch**: mezcla de ambos. Equilibrio (clave: tamaño del mini-lote).

**Complejidad P/NP**:
| Clase | Verificable en tiempo polinómico | Solución en tiempo polinómico |
|---|---|---|
| P | Sí | Sí |
| NP | Sí | Algunos |
| NP-Completo | Sí | Desconocido |
| NP-Duro | Algunos | Desconocido |

NP: no se conoce solución polinomial pero sí se puede verificar una propuesta en tiempo polinomial. NP-Completo: si se demuestra que uno es P, entonces P=NP (el resto de NP se transforma con complejidad polinomial). NP-Duro: al menos tan complejo como cualquier NP pero puede no ser NP (ni siquiera verificable en tiempo polinomial). Ejemplos: NP-Completo → SAT (Cook, 1971, todos los NP-Completos se reducen a SAT); NP-Duro → TSP. Sobre P=NP: "todo indica que P≠NP", por lo que casi seguro solo se pueden resolver estos problemas con métodos aproximados o heurísticas — de ahí que desde VC5 el curso pase a metaheurísticas.

**Fibonacci recursivo** (ejemplo de recurrencia exponencial):
```python
def Fibonacci(N:int):
    if N < 2: return 1
    else: return Fibonacci(N-1)+Fibonacci(N-2)
```
T(n)=T(n-1)+T(n-2) → ecuación característica x²−x−1=0, raíces x₁=(1+√5)/2≈1,618 (número áureo), x₂=(1−√5)/2. T(n)=A·x₁ⁿ+B·x₂ⁿ — crecimiento exponencial (misma familia que 2ⁿ); motiva resolver Fibonacci con PD en vez de recursión ingenua.

Teorema Maestro (recurrencias por división, ej. Quick Sort T(n)=2·T(n/2)+n):
- T(n)=O(nᵏ) si a<bᵏ
- T(n)=O(nᵏ·log n) si a=bᵏ (caso Quick Sort)
- T(n)=O(n^(log_b a)) si a>bᵏ

**Trabajo Práctico**: 3 problemas a elegir — 1) sesiones de doblaje (10 actores, 30 tomas, máx. 6 tomas/día, minimizar desplazamientos); 2) horarios de partidos de La Liga (maximizar audiencia, con coeficientes de reducción); 3) combinar dígitos 1-9 y signos +,−,*,/ sin repetir para obtener una cantidad dada (ej. 4+2-6/3*1=4). Preguntas obligatorias del entregable: nº de posibilidades sin restricciones, estructura de datos, FO, max/min, complejidad por fuerza bruta, diseño mejorado y su complejidad, juego de datos aleatorio.

## 6. AG2 — Ramificación y poda (asignación de tareas) + descenso del gradiente

(Pese al índice oficial, AG2 NO desarrolla BFS/DFS — eso está en VC3.)

**Ramificación y Poda — asignación de tareas** (Brassard y Bratley): asignar n tareas a n agentes (1 c/u), coste cᵢⱼ≥0, minimizar coste total. Ejemplo n=4:
```python
COSTES = [[11,12,18,40],
          [14,15,13,22],
          [11,17,19,23],
          [17,14,20,28]]
```
Solución = tupla, ej. (1,0,3,2) = agente0→tarea1, agente1→tarea0, agente2→tarea3, agente3→tarea2.
```python
def valor(S,COSTES):
    VALOR = 0
    for i in range(len(S)):
        VALOR += COSTES[i][S[i]]
    return VALOR

def CI(S,COSTES):  # cota inferior: coste fijado + mínimo posible restante
    VALOR = 0
    for i in range(len(S)):
        VALOR += COSTES[i][S[i]]
    for i in range(len(S), len(COSTES)):
        VALOR += min([COSTES[j][i] for j in range(len(S), len(COSTES))])
    return VALOR

def crear_hijos(NODO, N):
    HIJOS = []
    for i in range(N):
        if i not in NODO:
            HIJOS.append({'s':NODO+(i,)})
    return HIJOS
```
Algoritmo (6 pasos): 1) elegir nodo pendiente más prometedor (menor CI); 2) ramificar; 3) si un hijo es solución completa, comparar con la mejor (cota superior); 4) podar hijos cuya CI no pueda mejorar esa cota superior; 5) añadir hijos supervivientes a pendientes; 6) quitar el nodo ramificado de pendientes. Complejidad: difícil de precisar exacto; peor caso = expandir todos los niveles; mejor caso = podar todos los nodos de un nivel menos uno; en general exponencial.

**Descenso del gradiente — práctica**: fórmula pₜ₊₁=pₜ−αₜ∇f(pₜ), αₜ decreciente dinámico. 3 variantes (batch/estocástico/mini-batch) igual que VC4. Ejercicio sobre paraboloide f(x,y)=x²+y²:
```python
f  = lambda X: X[0]**2 + X[1]**2
df = lambda X: [2*X[0], 2*X[1]]

TA=.1
for _ in range(500):
    grad = df(P)
    P[0],P[1] = P[0] - TA*grad[0], P[1] - TA*grad[1]
```
Resultado real: punto inicial [0.7569,0.9223] → tras 500 iteraciones [-0.005,-0.005], f(P)≈5×10⁻⁵ (converge al mínimo global real en (0,0), consistente con que f es convexa). Función reto adicional no resuelta numéricamente: f(x,y)=sin(½x²−¼y²+3)·cos(2x+1−eʸ).

## 7. VC5 — Algoritmos heurísticos / metaheurísticas

**Metaheurística** (Glover, 1986): técnica general/estrategia. **Heurístico**: algoritmo concreto. Se usan cuando no hay método exacto viable o no hace falta el óptimo, solo una buena solución. Definición: "técnicas de algoritmos aproximados, iterativos, que exploran el espacio de soluciones con estrategias inteligentes/de sentido común adaptadas al problema". Ventajas: propósito general, buenos resultados, fáciles de implementar, paralelizables. Desventajas: aproximados, no deterministas, sin base teórica que los valide.

Exactos: óptimo garantizado, tiempo según dimensión, aptos para problemas pequeños. Heurísticos: soluciones de calidad, tiempo controlable, aptos para problemas grandes. Medidas de calidad: Eficacia (esfuerzo computacional), Bondad (cercanía al óptimo en promedio), Robustez (probabilidad de dar malas soluciones).

**Intensificación vs. Diversificación**: intensificar = centrarse en la región actual; diversificar = explorar otras regiones. Objetivo: equilibrio — identificar rápido regiones buenas sin sobre-invertir en zonas ya exploradas o poco prometedoras. Exceso de intensificación → atrapado en óptimo local; exceso de diversificación → no se aprovechan zonas buenas ya halladas.

**No Free Lunch** (Wolpert y Macready, 1997): por cada par de algoritmos, hay tantos problemas donde uno gana como donde gana el otro — no existe un algoritmo universalmente mejor; hace falta conocimiento específico del problema.

**Búsqueda aleatoria**: genera soluciones aleatorias cada iteración, devuelve la mejor.
```
GENERA(Solución Inicial); Solución Actual <- Inicial; Mejor <- Actual
Repetir: GENERA(Solución Actual); si mejor que Mejor, actualizar Mejor
Hasta criterio de parada; DEVOLVER Mejor
```
Con m soluciones posibles, prob. de acertar el óptimo con 1 intento = 1/m; para probabilidad p con n intentos: `n > log(1-p)/log(1-1/m)`.

**Búsqueda local**: Vecindad = soluciones en el entorno de una referencia, delimitado por un operador/movimiento. Proceso: desde una solución inicial, seleccionar iterativamente una nueva solución del entorno (intensificación, poca diversificación). Elementos: solución inicial, codificación, operador de vecino, criterio de parada.
```
GENERA(Inicial); Actual <- Inicial; Mejor <- Actual
Repetir: Vecina <- GENERA_VECINO(Actual); si Acepta(Vecina): Actual <- Vecina
         si mejor que Mejor: Mejor <- Actual
Hasta parada; DEVOLVER Mejor
```
Desventaja: quedar atrapado en óptimo local. Escapes: (1) cambiar estructura de entornos, (2) permitir movimientos a peores soluciones (tabú, recocido), (3) multiarranque. Operadores de vecindad para TSP: insertar elemento en otra posición; intercambiar dos (swap/2-opt); invertir sub-lista; barajar sub-lista.

**Búsqueda Tabú**: búsqueda por entornos con memoria adaptativa (prohibiciones temporales, análogo a tabúes socioculturales). Permite movimientos a peores soluciones para escapar de mínimos locales; evita ciclos prohibiendo temporalmente repetir soluciones ya visitadas (lista tabú); memoria corto plazo (evitar ciclos) y largo plazo (intensificar/diversificar). Tipos de lista: de SOLUCIONES, de MOVIMIENTOS, de ATRIBUTOS (prohibir un movimiento es más estricto que prohibir solo la solución resultante).

**Recocido simulado** (Kirkpatrick, Gelatt, Vecchi, 1983): búsqueda con aceptación probabilista; diversificar al principio, intensificar al final. Analogía termodinámica: estados↔soluciones, energía↔coste, temperatura↔parámetro de control, estado congelado↔solución final.
```
T <- T0 (alta)
Generar x1; F* <- F(x1); x* <- x1
Mientras no se cumpla parada:
  Generar x aleatorio en el entorno de xn
  si F(x) ≤ F(xn): xn+1 <- x
  si F(x) ≤ F*: F* <- F(x); x* <- x
  si no: generar p aleatorio en [0,1]; si p ≤ p(n): xn+1 <- x (acepta peor con cierta prob.)
  Disminuir temperatura
```
Criterio de Metropolis: `P_aceptación = exp(−δ/T)`, δ=C(s')−C(s). A mayor T, mayor prob. de aceptar peores; a menor diferencia de costes, mayor prob. de aceptar. Enfriamiento: constante; por tramos; exponencial T_(k+1)=α·T_k; Boltzmann T_k=T0/(1+log k); Cauchy T_k=T0/(1+k).

**Multiarranque**: repetir generación de solución inicial + búsqueda local hasta criterio de parada; iniciales aleatorias o dirigidas.

**GRASP** (Feo y Resende, 1995): multiarranque voraz-aleatorio-adaptativo. Voraz: construcción inicial voraz. Aleatorio: probabilidad sobre un conjunto de candidatos (no siempre el mejor). Adaptativo: se re-evalúan beneficios para condicionar siguientes elecciones.
```
procedure GRASP(maxIt, seed):
  ReadInput()
  for i in 1..maxIt:
    Solution = GreedyRandomizeConstruction(seed)
    Solution = LocalSearchSolution(Solution)
    UpdateSolution(Solution)
  return BestSolution
```
Ejemplo TSP 6 ciudades con Lista Restringida de Candidatos (LRC): desde 1, LRC={4,2,6}→elige 6 (1 6 - - - -); desde 6, LRC={3,5,2}→elige 3; desde 3, LRC={2,5,4}→elige 5; desde 5, LRC={4,2}→elige 2; desde 2, LRC={4}→elige 4: solución (1 6 3 5 2 4).

**Colonia de hormigas / ACO** (Dorigo, 1992): multiagente, construcción probabilística aprovechando info de otros agentes. Rastro de feromonas guía a otras hormigas; componente aleatorio permite descubrir soluciones nuevas; feromona proporcional a calidad (inversa al coste en minimización); se evapora con el tiempo (evita mínimos locales).
```
Depositar feromona inicial en todas las aristas
Crear m hormigas
Repetir:
  Reiniciar hormigas
  Cada hormiga construye solución usando feromonas y coste de aristas
  Cada hormiga deposita feromona en aristas de su solución
  Evaporar feromona de todas las aristas
Devolver mejor solución
```

## 8. AG3 — Heurísticas aplicadas al TSP

Aplica sobre TSP: búsqueda aleatoria, búsqueda local, recocido simulado, ACO (no evaluable).

Instancia real "swiss42.tsp" (42 ciudades), grafo completo, inicio/fin en nodo 0. Mejor solución conocida (TSPLIB): **1273**.
```python
def distancia_total(solucion, problem):
    distancia_total = 0
    for i in range(len(solucion)-1):
        distancia_total += distancia(solucion[i], solucion[i+1], problem)
    return distancia_total + distancia(solucion[-1], solucion[0], problem)
```
Resultados comparados sobre swiss42 (óptimo=1273): Búsqueda aleatoria (5.000 iter) → 3495. Búsqueda local 2-opt (hasta óptimo local) → de 3712 inicial a 3255 en un paso, converge a 1749 en 42 iteraciones. Recocido simulado (T0=10.000.000, enfriamiento T=T·0,999, parada T<0,0001) → 1906. Orden de cercanía al óptimo: local(1749) > recocido(1906) > aleatoria(3495).

Generador de vecina 2-opt: intercambiar 2 nodos; con N nodos se generan (N-1)(N-2)/2 soluciones. Para recocido, versión aleatoria: elegir 2 posiciones al azar e intercambiar.

Fórmula ACO aplicada a TSP — probabilidad de que la hormiga k vaya de i a j:
```
p^k_ij(t) = [τ_ij(t)]^α · [ν_ij]^β / Σ_(l∈J^k_i) [τ_il(t)]^α · [ν_il]^β
```
τ=feromona en (i,j); ν=inversa de la distancia; α=peso de la feromona; β=peso de la distancia; J^k_i=nodos aún no visitados por k (si no, probabilidad 0). Si α=0 → se asemeja a voraz puro. Si β=0 → solo importa la feromona.

## 9. VC6 — Computación evolutiva y algoritmos genéticos

Historia: Darwin (1809-1882, selección natural: variaciones heredables hacen que la población evolucione); Mendel (1822-1884, leyes de herencia); Bremermann (1926-1996, primeras simulaciones con cadenas binarias y reproducción/selección/mutación, 1962); Holland (1929-2015, "Adaptation in Natural and Artificial Systems" 1975: algoritmo genético como abstracción de evolución natural; población, cromosomas, cruce+mutación, selección).

Fundamento: se evoluciona una población de individuos (soluciones), sometida a mutaciones/recombinaciones aleatorias; selección según fitness decide quién sobrevive. Individuo=solución candidata; población=conjunto de soluciones en paralelo; fitness=función objetivo del problema.

**Componentes de un AG**: representación de soluciones; función de evaluación (fitness); creación de población inicial; operadores genéticos (cruce/mutación); mecanismo de selección probabilística. Representación binaria: Cromosoma=cadena de bits (individuo); Gen=posición; Alelo=valor de un gen. Fitness: función objetivo del problema, asigna valores reales a cada fenotipo, base de la selección (puede ser función matemática, simulador, robot; restricciones como penalizaciones). Población inicial: normalmente aleatoria, debe ser variada (todos los alelos representados); puede incorporar individuos de otras heurísticas.

**Operadores**: Mutación = modificación al azar sobre un individuo (actúa sobre genotipo, aleatoria, introduce diversidad — únicos operadores que producen variedad). Cruce = combinación de 2+ individuos (info elegida al azar; descendientes pueden ser peores, pero se espera que algunos mejoren). Cruce=intensificación (explora cerca de una solución); mutación=diversificación (explora espacios distintos). Buena estrategia usar ambos; sin cruce serían algoritmos evolutivos.

Tipos de cruce: 1-punto (corte al azar, intercambio de partes; sesgo: genes próximos permanecen juntos, extremos no se juntan); n-puntos (varios cortes); uniforme (cada gen se hereda al azar de un padre, sin sesgo posicional). Ejemplo TSP 2 puntos: P1=5 6 4|3 7 9|1 2 8, P2=1 5 3|9 8 7|4 6 2 — requiere "asegurar la factibilidad" (reparar duplicados/ausentes en permutaciones, ver Factibilizar en sección 10).

**Selección**: de supervivientes — por fitness (solo mejores sobreviven), por edad (hijos sustituyen padres), o ELITISMO (combinación: los mejores sobreviven siempre, indep. de edad). Rudolph (1994) demostró que el elitismo es necesario para converger al óptimo global. Selección por ruleta: porción proporcional al fitness (peores también pueden salir, con menor prob.). Selección por ranking: ρ(i)=rank(i)/(n·(n-1)). Selección por torneo: se eligen k al azar, gana el mejor.

Esquema general: Población inicial → Evaluar (fitness) → ¿satisfactoria? Sí→fin, devolver mejores; No→Selección→Cruce→Mutación→nueva población→reevaluar (bucle).

**Cierre oficial del curso** (diapositiva "Resumen de lo aprendido"): técnicas clásicas deterministas (voracidad, D&V, PD, PL, búsquedas en grafos); implicaciones de la complejidad computacional; problemas tipo para clasificar problemas nuevos; destreza para modelizar (espacio de soluciones, FO, restricciones); técnicas metaheurísticas (trayectorias, constructivas, poblacionales); Practicar→Investigar→Practicar→Investigar...

## 10. AG3 (2ª parte) — Algoritmo Genético para el TSP (práctica en grupo)

Codificación: individuo = lista/permutación de índices de nodos (igual que AG3). Población inicial: aleatoria, reutilizando `crear_solucion(Nodos)`. Cruce: 1 PUNTO — los hijos NO son soluciones válidas (nodos repetidos/faltantes), por eso existe `Factibilizar(solucion, problem)` que repara la permutación. Mutación: por intercambio (swap) de dos nodos al azar, con probabilidad = parámetro `mutacion`. Selección: `Seleccionar(problem, poblacion, N, elitismo)` elimina los menos aptos (fitness alto=distancia alta=peor) hasta volver a tamaño N, respetando % de elitismo; el resto por ruleta proporcional al fitness. Parada: nº fijo de generaciones.

Ejecución real: `algoritmo_genetico(problem=problem, N=500, mutacion=.3, elitismo=.40, generaciones=250)` → Generación #0: distancia 3979; Generación #1: distancia 3749 (mejora ya evidente).

**Variante TSP-TW (Time Windows)** — dos artículos citados como referencia (no código de la práctica):
- a) "Genetic Algorithm for Optimizing TSP-TW": `Penalty = (Time close tour location − End time schedule) / 60`; `Fitness = 1 / (ΣPenalty + ΣDistance)`.
- b) "Implementation of GA to Solving TSP-TW... Malang City" (ec. 1): `Fitness Value = 1000 / (ΣD + ΣT + (ΣP × 60))` (ΣD=distancia total, ΣT=tiempo total, ΣP=penalización total en minutos).
No mezclar ambas fórmulas: son propuestas de artículos distintos, no una fórmula oficial única del curso.

## 11. Mapa conceptual final — cómo elegir técnica

- ¿Subproblemas DISJUNTOS que se combinan al final? → **Divide y Vencerás** (Hanoi, Merge/Quick Sort, par de puntos más cercanos).
- ¿Basta la decisión localmente óptima en cada etapa y se puede demostrar que lleva al óptimo global? → **Técnica Voraz** (cambio de monedas con sistema canónico, Prim/Kruskal). Ojo: no siempre funciona (monedas [11,5,1], mochila).
- ¿Explorar sistemáticamente TODO un espacio discreto representable en árbol? → **Vuelta atrás/Backtracking** (N-Reinas), mejorable con **Ramificación y Poda** si hay cotas calculables (asignación de tareas, TSP exacto).
- ¿Subproblemas se REPITEN y se cumple Bellman? → **Programación Dinámica** (viaje por el río, mochila 0/1; por analogía, Floyd-Warshall/Bellman-Ford).
- ¿Optimización continua con función derivable (idealmente convexa)? → **Descenso del Gradiente**.
- ¿Problema tan grande que ningún exacto es viable (ej. TSP grande, NP-duro)? → **Metaheurísticas**: búsqueda aleatoria (referencia mínima); local/tabú/recocido (trayectoria); GRASP/ACO (constructivas); genéticos/evolutivos (poblacionales).

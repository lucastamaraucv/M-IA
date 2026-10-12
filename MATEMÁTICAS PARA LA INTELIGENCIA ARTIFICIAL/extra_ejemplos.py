"""Banco de ejemplos progresivos (básico → intermedio → experto).

Cada entrada está indexada por (sección, título_lección) → lista de 3
strings. La GUI los muestra en un popup cuando el usuario pulsa
«💼  Ejemplos progresivos».

Generado por 4 agentes a partir del Manual VIU + casos de IA reales.
"""

EXTRA_EJEMPLOS = {

    # ============== CAPÍTULO 1 — LÓGICA ==============
    ("1.1  Lógica proposicional", "Implicación (→, 'si... entonces')"): [
        "[BÁSICO]  Sea p='llueve' y q='el suelo está mojado'. Evaluamos p → q.\nCaso 1: p=V, q=V → V (llueve y está mojado).\nCaso 2: p=V, q=F → F (llueve pero NO está mojado: la implicación falla).\nCaso 3: p=F, q=V → V (no llueve, pero está mojado por otra causa).\nCaso 4: p=F, q=F → V.\nSólo es falsa cuando el antecedente es V y el consecuente F.",
        "[INTERMEDIO]  Demostrar que p → q ≡ ¬p ∨ q construyendo la tabla.\np=V, q=V: p→q=V ; ¬p ∨ q = F ∨ V = V ✔\np=V, q=F: p→q=F ; ¬p ∨ q = F ∨ F = F ✔\np=F, q=V: p→q=V ; ¬p ∨ q = V ∨ V = V ✔\np=F, q=F: p→q=V ; ¬p ∨ q = V ∨ F = V ✔\nLas columnas coinciden, luego son lógicamente equivalentes.",
        "[EXPERTO]  Modus Ponens en un sistema experto médico.\nRegla R: fiebre ∧ tos → gripe. Premisas: fiebre=V, tos=V.\nPaso 1: fiebre ∧ tos = V ∧ V = V.\nPaso 2: (V) → gripe, aplicando MP concluimos gripe=V.\nSi añadimos R2: gripe → reposo, encadenando: fiebre ∧ tos → reposo.\nEsta inferencia transitiva es la base del forward-chaining usado en motores de reglas tipo Prolog o CLIPS.",
    ],

    ("1.1  Lógica proposicional", "Leyes de Morgan"): [
        "[BÁSICO]  Negar 'hace sol Y hace calor'.\nSean p='hace sol', q='hace calor'. Queremos ¬(p ∧ q).\nPor De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q.\nEn lenguaje natural: 'no hace sol O no hace calor'.\nVerificación con p=V, q=F: ¬(V ∧ F)=¬F=V ; ¬V ∨ ¬F = F ∨ V = V ✔.\nObserva que el AND se convierte en OR al pasar la negación.",
        "[INTERMEDIO]  Simplificar ¬(¬p ∨ (q ∧ ¬r)).\nPaso 1, De Morgan exterior: ¬(¬p) ∧ ¬(q ∧ ¬r).\nPaso 2, doble negación: p ∧ ¬(q ∧ ¬r).\nPaso 3, De Morgan interior: p ∧ (¬q ∨ ¬¬r).\nPaso 4, doble negación: p ∧ (¬q ∨ r).\nResultado final: p ∧ (¬q ∨ r), forma normal mucho más legible.",
        "[EXPERTO]  Optimización de filtros booleanos en ML.\nUn dataset se filtra con: NOT(edad<18 AND ingreso<1000).\nAplicando De Morgan: (edad≥18) OR (ingreso≥1000).\nEn NumPy: ~((edad<18) & (ingreso<1000)) ≡ (edad>=18) | (ingreso>=1000).\nLa segunda forma evita una negación bit a bit sobre un array grande, ahorrando una pasada de memoria O(n).",
    ],

    ("1.2  Álgebra de Boole", "Propiedades — Idempotencia y Absorción"): [
        "[BÁSICO]  Idempotencia: x ∧ x = x ; x ∨ x = x.\nCon x=1: 1 ∧ 1 = 1 ✔ ; 1 ∨ 1 = 1 ✔.\nCon x=0: 0 ∧ 0 = 0 ✔ ; 0 ∨ 0 = 0 ✔.\nIntuición: repetir la misma condición no aporta información nueva.\n'Llueve Y llueve' = 'llueve'. 'Llueve O llueve' = 'llueve'.",
        "[INTERMEDIO]  Absorción: x ∨ (x ∧ y) = x.\nProbamos con los 4 casos:\nx=0, y=0: 0 ∨ (0 ∧ 0) = 0 ∨ 0 = 0 = x ✔\nx=0, y=1: 0 ∨ (0 ∧ 1) = 0 ∨ 0 = 0 = x ✔\nx=1, y=0: 1 ∨ (1 ∧ 0) = 1 ∨ 0 = 1 = x ✔\nx=1, y=1: 1 ∨ (1 ∧ 1) = 1 ∨ 1 = 1 = x ✔\nLa subexpresión (x ∧ y) queda 'absorbida' por x.",
        "[EXPERTO]  Simplificar f = (a ∧ b) ∨ (a ∧ b ∧ c) ∨ a.\nPaso 1, absorción: a ∨ (a ∧ b) = a, queda a ∨ (a ∧ b ∧ c).\nPaso 2, absorción de nuevo: a ∨ (a ∧ b ∧ c) = a.\nResultado: f = a.\nDe 3 términos AND con 5 operaciones pasamos a una sola variable. Esta reducción es lo que hacen los sintetizadores tipo Karnaugh o Quine-McCluskey.",
    ],

    ("1.3  Funciones booleanas y puertas", "Puerta XOR  —  O exclusivo"): [
        "[BÁSICO]  XOR (⊕) es V si exactamente UNA entrada es V.\nTabla:\n0 ⊕ 0 = 0\n0 ⊕ 1 = 1\n1 ⊕ 0 = 1\n1 ⊕ 1 = 0\nIntuición: 'uno u otro, pero no ambos'.\nFórmula equivalente: a ⊕ b = (a ∨ b) ∧ ¬(a ∧ b) = (a ∧ ¬b) ∨ (¬a ∧ b).",
        "[INTERMEDIO]  Sumador binario de 1 bit.\nQueremos sumar a+b sin acarreo de entrada.\nSuma = a ⊕ b ; Acarreo = a ∧ b.\nEjemplo a=1, b=1: suma = 1⊕1 = 0, acarreo = 1∧1 = 1.\nResultado binario: 10₂ = 2 decimal ✔ (1+1=2).\nEjemplo a=1, b=0: suma=1, acarreo=0 → 01₂ = 1 ✔.\nPor eso XOR es el corazón del half-adder y de toda CPU.",
        "[EXPERTO]  XOR no es linealmente separable: nace el perceptrón multicapa.\nPuntos: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0.\nNo existe recta w₁x₁+w₂x₂+b=0 que separe los 1's de los 0's.\nSolución: 2 capas. h₁=OR(x), h₂=AND(x), salida=AND(h₁,¬h₂)=XOR.\nMinsky-Papert (1969) frenó la IA conexionista hasta el retorno con backprop en 1986. XOR = chispa de las redes profundas.",
    ],

    ("1.3  Funciones booleanas y puertas", "Puertas NAND y NOR  —  las 'invertidas'"): [
        "[BÁSICO]  NAND = ¬(a ∧ b).\nTabla:\n0 NAND 0 = 1, 0 NAND 1 = 1, 1 NAND 0 = 1, 1 NAND 1 = 0.\nNAND sólo da 0 cuando AMBAS entradas son 1. Es la 'negación del AND'.\nAnálogamente NOR sólo da 1 cuando ambas son 0.",
        "[INTERMEDIO]  Construir NOT, AND y OR usando sólo NAND.\nNOT(a) = a NAND a. Comprobación: 0 NAND 0 = 1 ✔, 1 NAND 1 = 0 ✔.\nAND(a,b) = NOT(a NAND b) = (a NAND b) NAND (a NAND b).\nOR(a,b) = NOT(a) NAND NOT(b) = (a NAND a) NAND (b NAND b).",
        "[EXPERTO]  Universalidad funcional: NAND como base mínima.\n{NAND} es funcionalmente completo: cualquier función booleana puede expresarse SÓLO con NAND. Igual con {NOR}.\nLas FPGAs y ASICs fabrican toda la lógica con un único tipo de transistor CMOS configurado como NAND, reduciendo costes y máscaras litográficas. Una BNN puede compilarse a puro NAND para inferencia en edge AI.",
    ],

    ("1.4  Lógica de predicados", "Cuantificador ∀ (para todo)"): [
        "[BÁSICO]  Sea P(x): 'x es par'. Universo U = {2, 4, 6, 8}.\nEvaluamos ∀x ∈ U, P(x).\nP(2)=V, P(4)=V, P(6)=V, P(8)=V.\nComo todos son V, ∀x P(x) = V.\nSi añadimos 7: P(7)=F, entonces ∀x P(x) = F. Basta un contraejemplo.",
        "[INTERMEDIO]  Traducir y evaluar: 'Todo número natural elevado al cuadrado es no negativo'.\nFormalización: ∀n ∈ ℕ, n² ≥ 0.\nProbamos: 0²=0 ≥ 0 ✔ ; 3²=9 ≥ 0 ✔ ; 100²=10000 ≥ 0 ✔.\nPrueba general: n² = n·n. Si n ≥ 0, n·n ≥ 0. En ℕ no hay negativos, luego se cumple para TODO n.",
        "[EXPERTO]  Definición ε-δ de límite con ∀.\nlim_{x→a} f(x) = L ⇔ ∀ε > 0, ∃δ > 0 : ∀x (0 < |x−a| < δ → |f(x)−L| < ε).\nEjemplo: lim_{x→2} 3x = 6. Dado ε=0.03, buscamos δ tal que |3x−6|<0.03.\n|3x−6| = 3|x−2| < 0.03 ⇒ |x−2| < 0.01 ⇒ δ=0.01 sirve.\nEl ∀ε exige que la propiedad valga para CUALQUIER tolerancia, base del cálculo riguroso.",
    ],

    ("1.4  Lógica de predicados", "Cuantificador ∃ (existe)"): [
        "[BÁSICO]  Sea Q(x): 'x > 10'. Universo U = {3, 7, 12, 4}.\n¿Es V que ∃x ∈ U, Q(x)?\nProbamos: Q(3)=F, Q(7)=F, Q(12)=V → ¡encontrado!\nBasta UN ejemplo para que el ∃ sea verdadero.\nSi U fuera {3, 7, 4}, sería F porque ninguno cumple.",
        "[INTERMEDIO]  Demostrar ∃x ∈ ℝ, x² = 2.\nCandidato: x = √2 ≈ 1.4142.\nVerificación: (√2)² = 2 ✔.\nLuego ∃x ∈ ℝ con x²=2 es V.\nPero atención: ∃x ∈ ℚ, x² = 2 es FALSO (la irracionalidad de √2 lo demuestra). Misma fórmula, distinto universo, distinta respuesta.",
        "[EXPERTO]  Negación anidada e intercambio de cuantificadores.\nFrase: 'Toda persona tiene una madre' → ∀p ∃m, madre(m,p).\nNegación: ¬∀p ∃m madre(m,p) ≡ ∃p ∀m ¬madre(m,p).\nEn lenguaje natural: 'existe alguien sin madre alguna'.\nLa negación viaja invirtiendo cada cuantificador. Clave en SAT-solvers y lógica de descripción para Knowledge Graphs.",
    ],

    ("1.5  Lógica inductiva", "Programación Lógica Inductiva (ILP)"): [
        "[BÁSICO]  Hechos: padre(juan, ana). padre(juan, luis). padre(pedro, juan).\nEjemplos positivos de abuelo: abuelo(pedro, ana), abuelo(pedro, luis).\nILP busca una regla que cubra ambos:\nabuelo(X, Z) :- padre(X, Y), padre(Y, Z).\nVerificación: con X=pedro, Y=juan, Z=ana: padre(pedro,juan)=V y padre(juan,ana)=V → abuelo(pedro,ana)=V ✔.",
        "[INTERMEDIO]  Inducir 'mamífero' a partir de ejemplos.\nE⁺: mamifero(perro), mamifero(gato), mamifero(vaca).\nE⁻: mamifero(aguila), mamifero(trucha).\nHechos: tiene_pelo(perro,V), tiene_pelo(gato,V), tiene_pelo(aguila,F)…\nHipótesis: mamifero(X) :- tiene_pelo(X, V).\nCubre los 3 positivos y rechaza los 2 negativos. 100% completo y coherente.",
        "[EXPERTO]  ILP vs deep learning: aprendizaje simbólico interpretable.\nDado un dataset de fármacos, ILP induce reglas como:\nactivo(X) :- contiene(X, anillo_aromatico), peso_molecular(X, P), P < 500.\nVentajas:\n1) Regla LEGIBLE por un químico.\n2) Funciona con ~50 ejemplos.\n3) Incorpora conocimiento previo como hechos Prolog.\nBase de sistemas neuro-simbólicos (DeepProbLog, LNN).",
    ],

    ("1.6  Complejidad computacional", "Notación O grande (cota asintótica)"): [
        "[BÁSICO]  f(n) = 3n + 5. ¿Es O(n)?\nDefinición: f(n) ≤ c·n para n ≥ n₀.\nProbamos c=4: 3n+5 ≤ 4n ⇔ 5 ≤ n ⇒ n₀=5.\nEntonces ∀n ≥ 5: 3n+5 ≤ 4n. ✔\nLuego f(n) = O(n).\nIntuición: las constantes y los factores se ignoran; sólo importa el crecimiento.",
        "[INTERMEDIO]  Comparar 100n vs n²/2 para n grande.\nn=10: 1000 vs 50 → 100n gana.\nn=200: 20000 vs 20000 → empate.\nn=1000: 100000 vs 500000 → n²/2 gana, y por mucho.\nLa complejidad mide el FUTURO: O(n) < O(n²) sin importar las constantes.",
        "[EXPERTO]  Coste de entrenar una red neuronal con backpropagation.\nCapa densa con n entradas, m salidas, N muestras, E épocas:\nForward + Backward: O(E·N·n·m).\nEjemplo: E=100, N=10⁴, n=1024, m=256 ⇒ ≈ 2.6·10¹¹ ops.\nA 1 TFLOP/s ⇒ ~0.26 s por capa. Crece linealmente con el dataset pero cuadráticamente al ensanchar capas.",
    ],

    ("1.7  Teoría de grafos", "Grado de un vértice y Euler"): [
        "[BÁSICO]  Grafo G con V={A,B,C,D} y E={AB, AC, AD, BC}.\nGrado:\ndeg(A) = 3, deg(B) = 2, deg(C) = 2, deg(D) = 1.\nSuma de grados = 8 = 2·|E| = 2·4 ✔ (lema del apretón de manos).",
        "[INTERMEDIO]  ¿Tiene G circuito de Euler?\nTeorema: existe ⇔ G conexo y TODOS los vértices tienen grado par.\nGrados {3,2,2,1}: hay impares (A y D) → NO hay circuito.\n¿Camino euleriano? Existe ⇔ exactamente 2 vértices de grado impar. A=3 y D=1: justo 2. ✔ Sí hay camino, p.ej. D→A→B→C→A.",
        "[EXPERTO]  GNN y grado.\nEn una GNN, la agregación se normaliza por grado: h_v = Σ_{u∈N(v)} h_u / deg(v).\nEjemplo: nodo v con vecinos de embeddings [1,0], [0,1], [1,1]; deg(v)=3.\nh_v = ([1,0]+[0,1]+[1,1])/3 = [2/3, 2/3].\nLa normalización evita que hubs dominen el gradiente (Kipf & Welling 2017).",
    ],

    # ============== CAPÍTULO 2 — ÁLGEBRA ==============
    ("2.1  Teoría de conjuntos", "Unión, intersección y diferencia"): [
        "[BÁSICO]  Sean A={1,2,3,4} y B={3,4,5,6}.\n  • A∪B = {1,2,3,4,5,6}.\n  • A∩B = {3,4}.\n  • A−B = {1,2}.\n  • B−A = {5,6}.\nVerificación inclusión-exclusión: |A∪B| = |A| + |B| − |A∩B| = 4+4−2 = 6.  ✓",
        "[INTERMEDIO]  Dataset de píxeles etiquetados:\n  A = {x : 'gato'} con |A|=300, B = {x : 'peludo'} con |B|=500, |A∩B|=250.\n  ¿Cuántas son gato O peludas?\n  |A∪B| = 300 + 500 − 250 = 550.\n  ¿Cuántas peludas pero NO gato? |B−A| = 500 − 250 = 250.\n  En IA modela features solapadas.",
        "[EXPERTO]  Tres clases A,B,C con |A|=|B|=|C|=100, intersecciones par a par=20, |A∩B∩C|=5.\n  Inclusión-exclusión:\n  |A∪B∪C| = Σ|Aᵢ| − Σ|Aᵢ∩Aⱼ| + |A∩B∩C| = 300 − 60 + 5 = 245.\n  Etiquetas únicas en A: 100−20−20+5 = 65.\n  Útil para diagnosticar sesgo de etiquetado multi-clase.",
    ],

    ("2.1  Teoría de conjuntos", "Partes P(A) y cardinalidad 2ⁿ"): [
        "[BÁSICO]  A = {a,b,c}. P(A) = {∅, {a}, {b}, {c}, {a,b}, {a,c}, {b,c}, {a,b,c}}.\n8 subconjuntos = 2³.\nCada elemento se decide DENTRO o FUERA → 2·2·2 = 8.",
        "[INTERMEDIO]  Selección de features ML: 5 variables {edad, sexo, peso, altura, IMC}.\n¿Cuántos modelos distintos? |P(A)| = 2⁵ = 32 combinaciones.\nSin el modelo vacío: 31. Si IMC siempre presente: 2⁴ = 16 modelos.",
        "[EXPERTO]  Sea |A|=n=10. Subconjuntos de tamaño PAR.\nIdentidad: Σ_{k par} C(n,k) = 2^{n−1}.\nDemostración: (1+1)ⁿ = 2ⁿ y (1−1)ⁿ = 0.\nSumando: 2·Σ_{k par} C(n,k) = 2ⁿ ⇒ Σ_{k par} C(n,k) = 2⁹ = 512.",
    ],

    ("2.2  Relaciones y aplicaciones", "Relaciones de equivalencia"): [
        "[BÁSICO]  En ℤ, a R b ⟺ a − b es múltiplo de 3.\nReflexiva: a−a = 0 ✓. Simétrica: si a−b=3k, b−a=3(−k) ✓.\nTransitiva: a−b=3k, b−c=3m ⇒ a−c=3(k+m) ✓.\nClases: [0], [1], [2]. ℤ/3ℤ tiene 3 clases.",
        "[INTERMEDIO]  Vectores en ℝ³ equivalentes si tienen la misma dirección:\nv ~ w ⟺ ∃λ>0 con w = λv.\nv=(1,2,3), w=(2,4,6): v~w con λ=2.\nv ≁ (−1,−2,−3) (necesitaría λ=−1).\nEspacio cociente ℝ³/~ ≃ S² (esfera), base de visión proyectiva.",
        "[EXPERTO]  En M_n(ℝ), A ~ B ⟺ ∃P invertible con B = P⁻¹AP (semejanza).\nA = [[2,1],[0,2]] y B = [[2,0],[0,2]]: traza=4=4, det=4=4, pero polinomio mínimo difiere: (x−2)² vs (x−2).\nA NO es diagonalizable; B sí. NO son semejantes. Las clases son formas canónicas de Jordan.",
    ],

    ("2.2  Relaciones y aplicaciones", "Inyectiva, suprayectiva y biyectiva"): [
        "[BÁSICO]  f: ℝ → ℝ, f(x) = 2x + 1.\nInyectiva: 2a+1=2b+1 ⇒ a=b ✓.\nSuprayectiva: ∀y, x=(y−1)/2 ⇒ f(x)=y ✓.\nBiyectiva. Inversa: f⁻¹(y) = (y−1)/2.\nContraejemplo: g(x)=x² NO es inyectiva (g(2)=g(−2)) ni sobre ℝ (no alcanza negativos).",
        "[INTERMEDIO]  Capa de red neuronal f: ℝ³ → ℝ², f(x) = Wx con W = [[1,0,1],[0,1,1]].\nNúcleo: Wx=0 ⇒ ker(W)=⟨(−1,−1,1)⟩ ≠ {0} → NO inyectiva (capa reduce dim).\nRango=2=dim(ℝ²) → SÍ suprayectiva. Información comprimida pero todo el espacio cubierto.",
        "[EXPERTO]  Softmax σ: ℝⁿ → Δⁿ⁻¹.\nNO inyectiva: σ(z) = σ(z + c·1) (invariancia por traslación).\nSuprayectiva sobre el símplex abierto.\nPara biyectiva, restringir a {z : Σzᵢ=0} de dim n−1. Por eso softmax tiene n−1 grados de libertad en clasificación.",
    ],

    ("2.3  Combinatoria", "Combinaciones C(n,k) y póker"): [
        "[BÁSICO]  ¿De cuántas formas elegimos 2 cartas de 5?\nC(5,2) = 5!/(2!·3!) = 10.\nListando {A,B,C,D,E}: AB, AC, AD, AE, BC, BD, BE, CD, CE, DE → 10. ✓\nDiferencia con permutaciones: V(5,2) = 20 (con orden).",
        "[INTERMEDIO]  Probabilidad de 'doble pareja' en póker (5 cartas de 52).\nManos totales: C(52,5) = 2.598.960.\nValores: C(13,2)=78. Palos por valor: C(4,2)² = 36. Quinta carta: 11·4 = 44.\nFavorables: 78·36·44 = 123.552.\nP ≈ 0,0475 (4,75%).",
        "[EXPERTO]  Identidad de Vandermonde: C(m+n, k) = Σ_{j=0}^{k} C(m,j)·C(n,k−j).\nm=n=5, k=4: C(10,4) = 210.\nSuma: 1·5 + 5·10 + 10·10 + 10·5 + 5·1 = 210 ✓.\nUtilidad en IA: muestreo estratificado de minibatches con dos grupos.",
    ],

    ("2.4  Espacios vectoriales", "Dependencia e independencia lineal"): [
        "[BÁSICO]  v₁=(1,2), v₂=(2,4). αv₁+βv₂ = 0.\nα(1,2)+β(2,4)=(α+2β, 2α+4β)=(0,0).\nSolución no trivial: α=−2, β=1.\nDEPENDIENTES. v₂ = 2·v₁. Mismo rayo desde el origen.",
        "[INTERMEDIO]  En ℝ³: v₁=(1,0,1), v₂=(0,1,1), v₃=(1,1,2).\ndet [[1,0,1],[0,1,1],[1,1,2]] = 1·1 + 1·(−1) = 0.\nDEPENDIENTES. Relación: v₃ = v₁ + v₂.\nEn ML: features dependientes ⇒ matriz de diseño no de rango completo ⇒ OLS no único.",
        "[EXPERTO]  Funciones {1, cos(x), cos²(x)} en C([0,π]). ¿Independientes?\nα + β·cos(x) + γ·cos²(x) = 0 ∀x.\nx=π/2: α=0. x=0: β+γ=0. x=π: −β+γ=0. ⇒ α=β=γ=0.\nINDEPENDIENTES.\nPero {1, cos(2x), cos²(x)} son DEPENDIENTES: cos(2x)=2cos²(x)−1. Base de Fourier.",
    ],

    ("2.4  Espacios vectoriales", "Aplicaciones lineales y matriz asociada"): [
        "[BÁSICO]  T: ℝ² → ℝ² rotación 90° antihoraria.\nT(1,0) = (0,1), T(0,1) = (−1,0).\nM = [[0,−1],[1,0]] (columnas = imágenes de la base).\nVerificación: M·(2,3) = (−3, 2). ✓",
        "[INTERMEDIO]  Capa lineal T(x)=Wx+b con W=[[1,2,−1],[0,1,3]], b=(1,−2).\nx=(2,1,0): Wx = (4, 1). T(x) = (5, −1).\nSin sesgo: T lineal (T(0)=0). Con b≠0: afín.\nEn DL, se absorbe el bias añadiendo coordenada '1' al input.",
        "[EXPERTO]  Cambio de base. M=[[3,1],[0,2]] en base canónica.\nNueva base B'={u₁=(1,1), u₂=(1,−1)}. P=[[1,1],[1,−1]], P⁻¹=(1/2)[[1,1],[1,−1]].\nM' = P⁻¹MP = [[3,0],[1,2]] (mismos autovalores, distinta forma).",
    ],

    ("2.5  Factorización de matrices", "Valores y vectores propios"): [
        "[BÁSICO]  A = [[2,1],[0,3]] (triangular).\nPolinomio: (2−λ)(3−λ) = 0 → λ₁=2, λ₂=3.\nVector de λ=2: v=(1,0). De λ=3: v=(1,1).\nVerificación: A·(1,1) = (3,3) = 3·(1,1) ✓.",
        "[INTERMEDIO]  Matriz de covarianza C = [[4,2],[2,4]].\ndet(C−λI) = (4−λ)² − 4 = 0 ⇒ λ = 6 o 2.\nλ=6: v=(1,1)/√2. λ=2: v=(1,−1)/√2.\nEn PCA: 1ª componente principal es (1,1)/√2 con varianza 6. Total = 8 = 4+4. ✓",
        "[EXPERTO]  PageRank simplificado. 3 páginas con P estocástica.\nP = [[0, 1/2, 1/2],[1/3, 0, 1/2],[2/3, 1/2, 0]].\nVector propio de λ=1 (Perron-Frobenius): v ∝ (9, 8, 13), normalizado ≈ (0.30, 0.27, 0.43).\nLa página 3 tiene mayor PageRank. Convergencia iterando Pⁿx₀ → v.",
    ],

    ("2.5  Factorización de matrices", "SVD y su uso en IA"): [
        "[BÁSICO]  A = [[3,0],[0,−2]]. Valores singulares: σ₁=3, σ₂=2.\nU = I, Σ = [[3,0],[0,2]], V = [[1,0],[0,−1]] (recoge el signo).\nUΣVᵀ = A ✓.\nNorma ‖A‖₂ = σ_max = 3.",
        "[INTERMEDIO]  Matriz de datos A (3×2): [[1,1],[2,2],[3,3]].\nAᵀA = [[14,14],[14,14]], λ = 28 o 0.\nσ₁ = √28 = 2√7, σ₂ = 0.\nRango 1: filas proporcionales. Un único 'factor latente' explica los datos.",
        "[EXPERTO]  Compresión de imagen vía SVD truncada.\nA ∈ ℝ^{512×512}: 262.144 valores.\nA_k = Σ_{i=1}^{k} σᵢ uᵢ vᵢᵀ. Con k=50: 50·(512+512+1) = 51.250 valores (5x menos).\nError: ‖A−A_k‖_F² = Σ_{i>k} σᵢ². Base de PCA, LSI, embeddings de palabras.",
    ],

    ("2.6  Cálculo tensorial + TensorFlow", "Operaciones tensoriales y broadcasting"): [
        "[BÁSICO]  a = [1,2,3], b = [10,20,30].\nSuma: a+b = [11,22,33].\nHadamard: a*b = [10,40,90].\nEscalar: ⟨a,b⟩ = 140.\nNorma: ‖a‖ = √14 ≈ 3.74.\nEn TF: tf.reduce_sum(a*b) = producto escalar.",
        "[INTERMEDIO]  Broadcasting: A (3,3) + b (3,).\nA = [[1,2,3],[4,5,6],[7,8,9]], b = [10,20,30].\nb se 'estira' a (1,3) → (3,3). Resultado: [[11,22,33],[14,25,36],[17,28,39]].\nNo se replica físicamente. Típico: añadir bias a un batch de logits.",
        "[EXPERTO]  Reshape correctivo.\nX shape (32, 10) y μ shape (32,). X − μ requiere reshape μ.reshape(32,1) para broadcastear por features.\nRegla: dimensiones se alinean POR LA DERECHA; deben ser iguales o ser 1.\nBatchNorm normaliza por feature (axis=0), LayerNorm por muestra (axis=1).",
    ],

    # ============== CAPÍTULO 3 — ANÁLISIS ==============
    ("3.1  Cálculo infinitesimal", "Límite y continuidad"): [
        "[BÁSICO]  lim(x→2) (x² − 4)/(x − 2).\nSustitución: 0/0 (indeterminada).\nFactorizando: x² − 4 = (x − 2)(x + 2).\nSimplificando: x + 2.\nEvaluando: 2 + 2 = 4. Aunque f(2) no existe, el límite sí.",
        "[INTERMEDIO]  Continuidad de f(x) = sin(x)/x en x=0.\nf(0) = 0/0, no definida.\nL'Hôpital: lim cos(x)/1 = 1.\nDiscontinuidad evitable. Redefiniendo f(0)=1, f es continua en ℝ.",
        "[EXPERTO]  ReLU(x) = max(0,x). ¿Continua en 0?\nReLU(0)=0. lim por izquierda = 0. lim por derecha = 0. Coinciden con f(0). ✓ Continua.\nPero NO derivable allí (la derivada salta 0→1). De ahí los subgradientes en backprop.",
    ],

    ("3.1  Cálculo infinitesimal", "Derivada: definición"): [
        "[BÁSICO]  f(x) = x². Por la definición.\nf(x+h) = x² + 2xh + h².\n[f(x+h)−f(x)]/h = 2x + h.\nlim(h→0) = 2x. En x=3, pendiente = 6.",
        "[INTERMEDIO]  f(x) = 1/x en x=2.\nf(x+h)−f(x) = −h/[x(x+h)].\nDividido entre h: −1/[x(x+h)].\nlim(h→0) = −1/x². En x=2: f'(2) = −1/4.",
        "[EXPERTO]  Sigmoide σ(x) = 1/(1+e⁻ˣ). Demostrar σ'(x) = σ(x)(1−σ(x)).\nσ'(x) = e⁻ˣ/(1+e⁻ˣ)² = [1/(1+e⁻ˣ)] · [e⁻ˣ/(1+e⁻ˣ)] = σ(x)·(1−σ(x)). En backprop ahorra cómputo: la activación misma sirve para la derivada.",
    ],

    ("3.1  Cálculo infinitesimal", "Optimización: extremos absolutos"): [
        "[BÁSICO]  f(x) = x² − 4x + 3 en [0, 5].\nf'(x) = 2x − 4 = 0 → x=2.\nf(0)=3, f(2)=−1, f(5)=8.\nMáx abs = 8 en x=5. Mín abs = −1 en x=2.",
        "[INTERMEDIO]  Área máxima de rectángulo inscrito en semicírculo x²+y²=25, y≥0.\nA(x) = 2x·√(25−x²). A'(x) = (50−4x²)/√(25−x²) = 0 → x² = 12.5.\nx = √12.5 ≈ 3.54, y ≈ 3.54. Área máx = 25 u².",
        "[EXPERTO]  Regresión con regularización L2: L(w) = (w−3)² + 0.5w².\nL'(w) = 2(w−3) + w = 3w − 6.\nL'=0 → w* = 2. Sin reg: w*=3. Con L2 (λ=0.5): w*=2.\nLa regularización contrae el óptimo hacia 0 (Ridge), reduciendo overfitting.",
    ],

    ("3.1  Cálculo infinitesimal", "Integral definida y Barrow"): [
        "[BÁSICO]  ∫₀² x² dx.\nF(x) = x³/3.\nBarrow: F(2) − F(0) = 8/3 ≈ 2.667.\nÁrea bajo la parábola entre 0 y 2.",
        "[INTERMEDIO]  ∫₁ᵉ ln(x) dx por partes.\nu=ln(x), dv=dx → du=dx/x, v=x.\n∫ ln(x) dx = x·ln(x) − x.\nF(e) = e·1 − e = 0. F(1) = 0 − 1 = −1.\n∫₁ᵉ = 0 − (−1) = 1.",
        "[EXPERTO]  La gaussiana integra 1: ∫ (1/√(2π)) e^(−x²/2) dx = 1.\nI = ∫ e^(−x²/2) dx. I² en coordenadas polares = 2π.\nLuego I = √(2π) y dividido entre √(2π) da 1. Base de la verosimilitud gaussiana.",
    ],

    ("3.2  Cálculo multivariable", "Gradiente y derivada direccional"): [
        "[BÁSICO]  f(x,y) = x² + 3y². ∇f = (2x, 6y).\nEn (1,2): ∇f = (2, 12).\n‖∇f‖ = √148 ≈ 12.17. Esa es la tasa máxima de crecimiento.",
        "[INTERMEDIO]  f(x,y) = x·y + y². ∇f = (y, x+2y).\nEn P=(2,1): ∇f = (1, 4).\nu = (3,4), ‖u‖=5, û = (0.6, 0.8).\nD_û f = 1·0.6 + 4·0.8 = 3.8.",
        "[EXPERTO]  Loss L(w₁,w₂) = (w₁−1)² + (w₂+2)². SGD desde (0,0), lr=0.1.\n∇L(0,0) = (−2, 4). Dirección descenso = (2, −4)/√20.\nNuevo w = (0,0) − 0.1·(−2,4) = (0.2, −0.4). Avanzamos hacia (1,−2).",
    ],

    ("3.2  Cálculo multivariable", "Puntos críticos y hessiana"): [
        "[BÁSICO]  f(x,y) = x² + y² − 4x + 6y.\n∇f = (2x−4, 2y+6) = 0 → (2,−3).\nH = [[2,0],[0,2]], det=4>0, f_xx=2>0 → mín local (y global).\nf(2,−3) = −13.",
        "[INTERMEDIO]  f(x,y) = x³ − 3xy + y³.\n∇f=0 → x=y² y y=x² → x=0 o x=1. Críticos: (0,0) y (1,1).\nH = [[6x, −3],[−3, 6y]]. En (0,0): det=−9<0 → silla.\nEn (1,1): det=27>0, f_xx=6>0 → mín local.",
        "[EXPERTO]  L(w₁,w₂) = w₁² − w₁w₂ + w₂² + 2w₁.\n∇L=0 ⇒ 2w₁−w₂=−2 y −w₁+2w₂=0 → w₂=−2/3, w₁=−4/3.\nH = [[2,−1],[−1,2]]: autovalores 1 y 3 > 0 → definida positiva.\nMín global en (−4/3, −2/3). GD convergerá.",
    ],

    ("3.2  Cálculo multivariable", "Lagrange: optimización con restricciones"): [
        "[BÁSICO]  Maximizar xy con x+y=10.\nL = xy − λ(x+y−10).\n∂L/∂x = y−λ=0; ∂L/∂y = x−λ=0 → x=y. Con 2x=10 → x=y=5.\nMáx: f(5,5) = 25. Repartir igual maximiza el producto.",
        "[INTERMEDIO]  Minimizar x²+y² sobre 2x+y=5.\n∇f = λ∇g → (2x, 2y) = λ(2, 1).\n2x=2λ, 2y=λ → x=λ, y=λ/2.\n2λ + λ/2 = 5 → λ=2. x=2, y=1. Mín = 5. Distancia² del origen a la recta.",
        "[EXPERTO]  SVM hard-margin para 2 puntos.\nx₁=(1,0) clase +1, x₂=(−1,0) clase −1.\nMinimizar ½‖w‖² s.a. y_i(w·x_i + b) ≥ 1.\nKKT: w*=(1,0), b=0. Margen = 2/‖w‖ = 2.",
    ],

    ("3.3  Gradient descent + Backprop", "Algoritmo GD con learning rate"): [
        "[BÁSICO]  f(w) = (w−4)², w₀=0, lr=0.5.\nf'(w) = 2(w−4). w ← 0 − 0.5·(−8) = 4.\n¡Convergencia en un paso!\nCon lr=0.1 sería más lento pero seguro: w₁=0.8, w₂=1.44, …",
        "[INTERMEDIO]  f(w) = w⁴ − 3w², w₀=2, lr=0.05.\nf'(w) = 4w³ − 6w. En w₀=2: f'=20 → w₁=1.\nf'(1)=−2 → w₂=1.1. Converge a √(3/2) ≈ 1.225 (mín local).\nCon w₀=−2 caería en el simétrico. GD encuentra LOCALES.",
        "[EXPERTO]  f(w) = w². w₀=1. Comparación lr.\nw_{t+1} = w_t(1 − 2lr).\nlr=0.01 → factor 0.98, converge.\nlr=1.5 → factor −2, diverge oscilando (1, −2, 4, −8…).\nCondición: |1−2lr|<1 ⇒ 0<lr<1.",
    ],

    ("3.3  Gradient descent + Backprop", "Forward pass en red simple"): [
        "[BÁSICO]  Red 1 neurona: y = σ(w·x + b), σ sigmoide.\nw=0.5, b=−1, x=2.\nz = 0.5·2 − 1 = 0. σ(0) = 0.5.\nSi etiqueta t=1: MSE = (1−0.5)² = 0.25.",
        "[INTERMEDIO]  Red 2-2-1 con ReLU.\nW₁=[[1,−1],[2,1]], W₂=[1,1], b₁=[0,0], b₂=−1, x=(1,1).\nz₁ = (0, 3) → a₁ = (0, 3).\nz₂ = 1·0+1·3−1 = 2. ŷ = ReLU(2) = 2.",
        "[EXPERTO]  Mini-batch con softmax (3 clases).\nX = [[1,2],[0,1]], W = [[1,0,−1],[0,1,1]].\nZ = X·W = [[1,2,1],[0,1,1]].\nFila 1: exp≈[2.72, 7.39, 2.72], softmax≈[0.21, 0.58, 0.21].\nFila 2: softmax≈[0.16, 0.42, 0.42]. Cada fila suma 1.",
    ],

    ("3.3  Gradient descent + Backprop", "GD en TensorFlow (conceptual)"): [
        "[BÁSICO]  Minimizar (w−3)² con TF (pseudo).\nw = tf.Variable(0.0); opt = SGD(lr=0.1).\nwith tape: loss = (w−3)².\ngrads = tape.gradient(loss, [w]) → −6.\napply: w ← 0 + 0.6 = 0.6. Tras 30 iters w ≈ 2.99.",
        "[INTERMEDIO]  Regresión lineal: x=[1,2,3], y=[2,4,6].\nW=0, b=0 → MSE ≈ 18.67.\n∂MSE/∂w = (2/3)Σ(ŷ−y)x = −18.67. ∂MSE/∂b = −8.\nlr=0.01: w ← 0.187, b ← 0.08. Tras épocas → (2, 0).",
        "[EXPERTO]  Adam vs SGD en f(w₁,w₂) = w₁² + 100·w₂² (cond. 100:1).\n∇f en (1,1) = (2, 200). SGD lr=0.01: diverge en w₂.\nAdam normaliza por √(E[g²]): lr efectivo se reduce en w₂.\nAdam converge en ~50 pasos; SGD requiere lr=0.001 y miles. Optimizadores adaptativos manejan curvaturas heterogéneas.",
    ],

    # ============== CAPÍTULO 4 — PROBABILIDAD ==============
    ("4.1  Probabilidad", "Regla de Laplace"): [
        "[BÁSICO]  Dado de 6 caras. P(par)?\nFavorables: {2,4,6} → 3. Posibles: 6.\nP(par) = 3/6 = 0.5.\nLa regla exige equiprobabilidad.",
        "[INTERMEDIO]  Urna: 5 rojas, 3 azules, 2 verdes (10 total). 2 extracciones sin reemplazo.\nP(ambas rojas) = C(5,2)/C(10,2) = 10/45 ≈ 0.222.\nAlternativa secuencial: (5/10)·(4/9) ≈ 0.222 ✓.",
        "[EXPERTO]  Cumpleaños: n=23 personas.\nP(todos distintos) = ∏ k=0..22 (365−k)/365 ≈ 0.4927.\nP(coincidencia) ≈ 0.5073 > 0.5.\nResultado contraintuitivo: basta n=23.",
    ],

    ("4.1  Probabilidad", "Teorema de Bayes (test diagnóstico)"): [
        "[BÁSICO]  Enfermedad P(E)=0.01. Test: P(+|E)=0.9, P(+|¬E)=0.1.\nP(E|+) = (0.9·0.01)/(0.9·0.01 + 0.1·0.99) = 0.009/0.108 ≈ 0.083.\nSólo 8.3% de positivos están realmente enfermos.",
        "[INTERMEDIO]  Spam: P(spam)=0.3. P(oferta|spam)=0.6, P(oferta|¬spam)=0.05.\nP(spam|oferta) = (0.6·0.3)/(0.6·0.3 + 0.05·0.7) ≈ 0.8372.\nLa palabra eleva la prob a posteriori de 0.3 a 0.84.",
        "[EXPERTO]  Dos tests independientes. P(E)=0.001, sensibilidad 0.99, FPR=0.05.\nTras +₁: P(E|+₁) ≈ 0.0194.\nPosteriori como nueva prior: P(E|+₁,+₂) ≈ (0.99·0.0194)/(0.99·0.0194 + 0.05·0.9806) ≈ 0.281.\n¡La evidencia acumulada multiplica por 281 la creencia inicial!",
    ],

    ("4.1  Probabilidad", "Esperanza y varianza (dado)"): [
        "[BÁSICO]  Dado justo X ∈ {1..6}, P=1/6.\nE[X] = 21/6 = 3.5.\nE[X²] = 91/6 ≈ 15.167.\nVar(X) = 15.167 − 12.25 ≈ 2.917. σ ≈ 1.708.",
        "[INTERMEDIO]  Juego: 2€ por tirar, ganas X €. B = X−2.\nE[B] = 3.5 − 2 = 1.5€.\nVar(B) = Var(X) = 2.917 (invariante a traslaciones).\nJuego favorable al jugador.",
        "[EXPERTO]  Suma de 2 dados indep. S = X₁+X₂.\nE[S] = 7. Var(S) = 5.833 (independencia ⇒ varianzas suman).\nPromediando n=100 dados: σ_X̄ = √(2.917/100) ≈ 0.171.\nLa desviación del promedio decrece como 1/√n (TCL).",
    ],

    ("4.2  Estimación de parámetros", "Ley de grandes números y TCL"): [
        "[BÁSICO]  Moneda justa (p=0.5).\nn=10: posible ver 7 caras (0.7).\nn=1000: ≈ 508 (0.508). n=10⁴: ≈ 5003 (0.5003).\nLGN: X̄ₙ → 0.5. Error ~ 1/√n.",
        "[INTERMEDIO]  X ~ Unif(0,1), μ=0.5, σ²=1/12.\nn=48: X̄ ≈ N(0.5, 1/576). σ_X̄ = 1/24 ≈ 0.0417.\nP(|X̄−0.5|<0.05) = P(|Z|<1.2) ≈ 0.7699.\nCasi 77% caen a menos de 0.05 de la media.",
        "[EXPERTO]  Monte Carlo para π. Puntos en [0,1]², proporción dentro de x²+y²≤1 → π/4.\nPara error 0.01 al 95%: n ≥ (1.96·σ)²/(0.01·4)² con σ²≈0.1685 → n ≈ 4046.\nPara 3 decimales: n ≈ 4·10⁵.",
    ],

    ("4.2  Estimación de parámetros", "Máxima verosimilitud (MLE) para Bernoulli"): [
        "[BÁSICO]  Moneda n=10, k=7 caras.\nL(p) = p⁷(1−p)³.\nℓ(p) = 7 ln(p) + 3 ln(1−p).\nDerivando: 7/p − 3/(1−p) = 0 → p̂ = 0.7.\nMLE coincide con la frecuencia muestral.",
        "[INTERMEDIO]  Muestra {2.1, 1.9, 2.3, 2.0, 2.2} de N(μ, σ²=0.04).\nℓ(μ) = −Σ(xᵢ−μ)²/(2σ²).\n∂ℓ/∂μ = Σ(xᵢ−μ)/σ² = 0 → μ̂ = x̄ = 2.10.\nMLE de μ en una normal = media muestral.",
        "[EXPERTO]  Exponencial f(x;λ) = λe^(−λx). Muestra {1.2, 0.8, 1.5, 0.9, 1.1}.\nℓ(λ) = 5 ln(λ) − 5.5λ. λ̂ = 5/5.5 ≈ 0.909.\nInformación de Fisher: I(λ) = n/λ².\nVar(λ̂) ≈ 0.165, IC 95%: 0.909 ± 0.797.",
    ],

    ("4.3  Procesos estocásticos", "Cadena de Markov: lluvia y sol"): [
        "[BÁSICO]  S=sol, L=lluvia. P = [[0.8, 0.2], [0.4, 0.6]].\nHoy sol → P(mañana lluvia)=0.2, P(mañana sol)=0.8.\nMarkov: el clima de mañana sólo depende del de hoy.",
        "[INTERMEDIO]  v₀=(1,0). v₁ = (0.8, 0.2).\nv₂ = (0.72, 0.28). v₃ ≈ (0.688, 0.312).\nLa prob de sol decrece monótonamente hacia su valor estacionario.",
        "[EXPERTO]  3 estados con P = [[0.7,0.2,0.1],[0.3,0.4,0.3],[0.2,0.3,0.5]].\nπP = π: resolvemos sistema.\nπ ≈ (0.452, 0.290, 0.258). A largo plazo 45.2% días soleados, independiente del estado inicial (cadena ergódica).",
    ],

    ("4.3  Procesos estocásticos", "Distribución estacionaria"): [
        "[BÁSICO]  P = [[0.9, 0.1], [0.5, 0.5]].\n0.9π₁ + 0.5π₂ = π₁ → 0.5π₂ = 0.1π₁ → π₂ = 0.2π₁.\nπ₁+π₂=1 → π = (5/6, 1/6) ≈ (0.833, 0.167).",
        "[INTERMEDIO]  P = [[0.7,0.3],[0.6,0.4]]. π = (2/3, 1/3).\nBalance detallado: π₁·P₁₂ = 0.2 = π₂·P₂₁. ✓\nLa cadena es reversible y π es estacionaria.",
        "[EXPERTO]  PageRank: 3 páginas con P = [[0, 0.5, 0.5],[1, 0, 0],[0.5, 0.5, 0]].\nIterando: v₀=(1/3, 1/3, 1/3) → v₂ ≈ (0.417, 0.333, 0.25) → π ≈ (0.4, 0.4, 0.2).\nEquivalente al autovector izquierdo de P con λ=1.",
    ],

    ("4.4  TensorFlow Probability", "Muestreo de Monte Carlo"): [
        "[BÁSICO]  E[X²] con X ~ N(0,1). Teórico: Var(X)=1.\nMuestras 10⁴ y media de x²: ≈ 1.003 ± 0.014.\nError estándar = σ/√n = √2/√10⁴ ≈ 0.0141. ✓",
        "[INTERMEDIO]  ∫₀¹ e^(−x²) dx por muestreo uniforme.\nu ~ Unif(0,1), estimador = mean(exp(-u²)).\nN=10⁵ ⇒ ≈ 0.7468 (real 0.7468).\nReducción de varianza con muestreo estratificado: σ se reduce √k.",
        "[EXPERTO]  Importance sampling: E_p[f(X)] usando q.\nw(x) = p(x)/q(x). Estimador = mean(f(x)·w).\nEjemplo: E_p[X] con p=N(3,1) y q=N(0,2). N=10⁴ → μ̂ ≈ 3.01.\nSi q se aleja mucho de p los pesos explotan (ESS pequeño).",
    ],

    ("🤖  Aplicaciones a IA (extensión)", "Regresión lineal y MSE"): [
        "[BÁSICO]  Datos (1,2), (2,3), (3,5). ŷ = w·x + b.\nw=1.5, b=0.5 → ŷ=(2, 3.5, 5). Errores: (0, 0.5, 0).\nMSE = 0.25/3 ≈ 0.0833.",
        "[INTERMEDIO]  Mínimos cuadrados exacto.\nx̄=2, ȳ=10/3. w = Σ(xᵢ−x̄)(yᵢ−ȳ) / Σ(xᵢ−x̄)² = 1.5.\nb = 10/3 − 3 = 1/3. MSE óptimo ≈ 0.0556.\nFórmula normal: w = (XᵀX)⁻¹Xᵀy.",
        "[EXPERTO]  GD para regresión: w ← w − η·∂L/∂w.\nη=0.1, w₀=b₀=0. Iter 1: w≈0.78, b≈0.27. Tras 1000 iters → (1.5, 0.333).\nη>0.5 diverge; η<10⁻⁴ ralentiza.\nL2: L = MSE + λ·w² ⇒ Ridge, reduce overfitting.",
    ],

    ("🤖  Aplicaciones a IA (extensión)", "PCA vía SVD"): [
        "[BÁSICO]  Datos centrados sobre y=x: {(1,1), (2,2), …}.\n1ª componente: v₁=(1/√2, 1/√2).\nLa varianza se concentra al 100% en la primera componente.",
        "[INTERMEDIO]  X (3×2) = [[1,0],[0,1],[−1,−1]].\nC = XᵀX/n = [[2/3, 1/3],[1/3, 2/3]]. λ = 1, 1/3.\nv₁ = (1/√2, 1/√2). Varianza explicada PC1 = 1/(1+1/3) = 75%.",
        "[EXPERTO]  SVD: X = U·Σ·Vᵀ. σᵢ² = n·λᵢ.\nPseudo: X_c = X − mean(X, 0); U, S, Vt = svd(X_c).\nX_reducido = X_c @ Vt[:k].T.\nVar acumulada = Σσᵢ² (i=1..k) / Σσⱼ². Más estable que diagonalizar la covarianza explícita.",
    ],

    # ======================================================================
    #  EJEMPLOS DE LAS SESIONES DE CLASE (Dra. Zoraida Sivoli Barrios)
    #  Extraídos de las diapositivas: Sesión 1 (lógica/conjuntos/Boole),
    #  Sesión 2 (Boole/funciones/puertas), Sesión 3 (predicados/inductiva/
    #  complejidad/conjuntos II), Sesión 4 (aplicaciones/combinatoria/grafos)
    #  y Sesión 5 (espacios vectoriales/matrices). Indexados por su categoría.
    # ======================================================================

    # ---------------- CAPÍTULO 1.1 — LÓGICA PROPOSICIONAL ----------------
    ("1.1  Lógica proposicional", "¿Qué es una proposición lógica?"): [
        "[BÁSICO]  (Sesión 1) Una proposición admite un único valor de verdad: 1 (verdadero) o 0 (falso).\n'2+2=4' → valor 1.\n'4>5' → valor 0.\n'La mesa de Antonio' NO es proposición: no afirma nada que sea V o F.\nRegla: si no puedes decir V/F sin discutir, no es proposición.",
        "[INTERMEDIO]  (Sesión 1) Caso límite visto en clase: la conjetura de Goldbach,\n'todo número par mayor que 2 es suma de dos primos'.\nES una proposición —tiene un valor de verdad— aunque hoy no sepamos cuál.\nTener un valor de verdad y saber demostrarlo son cosas distintas: la lógica solo exige que el valor exista.",
        "[EXPERTO]  (Sesión 1) Problema del explorador: los caníbales lo hierven si su frase es V y lo asan si es F. Dice: 'Yo seré asado'.\nSi fuese V → debería ser hervido → contradice la frase.\nSi fuese F → debería ser asado → la frase resulta V.\nEs autorreferencial: ni V ni F. En IA, las frases autorreferenciales rompen la inferencia clásica (raíz del teorema de incompletitud y de los límites de la verificación automática).",
    ],

    ("1.1  Lógica proposicional", "Tautología, contradicción y contingencia"): [
        "[BÁSICO]  (Sesión 1) Clasificación según su valor de verdad:\n• Tautología: SIEMPRE V. Ej.: p ∨ ¬p ('mañana salgo de casa o tal vez no').\n• Contradicción: SIEMPRE F. Ej.: 'la cantidad de números enteros es finita'.\n• Contingencia: depende. Ej.: 'hoy es jueves', 'si lanzo una moneda saldrá cara'.",
        "[INTERMEDIO]  (Sesión 1) Clasifica las fórmulas de la lista de clase:\n p + ¬p → tautología.\n p · ¬p → contradicción.\n p → p → tautología.\n p → ¬p → contingente.\n (p·q) → (p+q) → tautología (si el AND es 1, el OR también).\n (p+q) → (p·q) → contingente (p=1, q=0 la hace falsa).",
        "[EXPERTO]  (Sesión 1) En verificación de circuitos/IA, probar que una fórmula es TAUTOLOGÍA equivale a comprobar que una propiedad se cumple en TODAS las entradas (validez, co-SAT). Si una especificación de seguridad no es tautología, el SAT-solver devuelve el contraejemplo: la combinación exacta de entradas que la viola.",
    ],

    ("1.1  Lógica proposicional", "Conector Y (∧, AND, conjunción)"): [
        "[BÁSICO]  (Sesión 1) p ∧ q es V solo si AMBOS lo son; el conector ∧ se identifica con el producto ·.\nEjemplo de clase:\np: 'Valencia pertenece a la C. Valenciana' = V.\nq: 'Alicante pertenece a la C. Valenciana' = V.\nr: 'Alicante pertenece a la provincia de Valencia' = F.\np ∧ q = V·V = 1.   p ∧ r = V·F = 0.",
        "[INTERMEDIO]  (Sesión 1) Como ∧ = producto, una conjunción larga se evalúa multiplicando 0/1:\n(p₁ ∧ p₂ ∧ … ∧ pₙ) = p₁·p₂···pₙ.\nBasta UN solo 0 para anular todo el producto. Por eso una cadena de condiciones 'Y' falla en cuanto falla una.",
        "[EXPERTO]  (Sesión 1) En una máscara de NumPy, (cond1 & cond2 & cond3) es el producto elemento a elemento de tres arrays 0/1: una fila pasa el filtro solo si TODAS sus condiciones valen 1, justo p₁·p₂·p₃. El AND define la intersección de criterios sobre un dataset.",
    ],

    ("1.1  Lógica proposicional", "Conector O (∨, OR, disyunción)"): [
        "[BÁSICO]  (Sesión 1) p ∨ q es V si alguno (o ambos) lo es; el conector ∨ se identifica con la suma +.\np: 'Valencia ∈ C. Valenciana' = V; r: 'Alicante ∈ provincia de Valencia' = F.\np ∨ r = 1 + 0 = 1 (basta con p).\nSolo da 0 cuando ambos son 0.",
        "[INTERMEDIO]  (Sesión 1) Ojo: la 'o' del lenguaje a veces es EXCLUSIVA (o p o q, pero no ambos). Tabla de la sesión:\n 1 ⊻ 1 = 0, 1 ⊻ 0 = 1, 0 ⊻ 1 = 1, 0 ⊻ 0 = 0.\nLa ∨ inclusiva da 1 cuando ambos son 1; la exclusiva da 0 en ese caso.",
        "[EXPERTO]  (Sesión 1) La OR inclusiva es la unión de conjuntos (A∪B = {x : x∈A ∨ x∈B}) y la saturación a+b con tope en 1. La XOR es la suma módulo 2 y NO es linealmente separable: por eso necesitó el perceptrón multicapa.",
    ],

    ("1.1  Lógica proposicional", "Conector NO (¬, NOT, negación)"): [
        "[BÁSICO]  (Sesión 1) La negación invierte el valor de verdad:\n p=1 → ¬p=0 ;  p=0 → ¬p=1.\nNotaciones equivalentes: ¬p, ∼p, p̄.",
        "[INTERMEDIO]  (Sesión 1) Doble negación: p̄̄ = p. Y p → q equivale a ¬p ∨ q. Tabla:\n p=1,q=1: →=1, ¬p∨q=0∨1=1 ✔\n p=1,q=0: →=0, ¬p∨q=0∨0=0 ✔\n p=0,q=1: →=1, 1∨1=1 ✔\n p=0,q=0: →=1, 1∨0=1 ✔",
        "[EXPERTO]  (Sesión 1) Negar bien evita recomputar: 'NO (edad<18 Y renta<1000)' se vuelve por De Morgan '(edad≥18) O (renta≥1000)', sin negación global y en una sola pasada del array. La negación es además la base del complemento Aᶜ en conjuntos.",
    ],

    ("1.1  Lógica proposicional", "Bicondicional (↔, 'si y solo si')"): [
        "[BÁSICO]  (Sesión 1) p ↔ q es V cuando p y q tienen el MISMO valor:\n 1↔1=1, 1↔0=0, 0↔1=0, 0↔0=1.\nEjemplo de clase: P='4 es impar' (F), Q='1+1=3' (F). Ambas falsas → P↔Q = V.",
        "[INTERMEDIO]  (Sesión 1) Descomposición vista en clase: P ↔ Q ≡ (P→Q) ∧ (Q→P).\nUna equivalencia exige la implicación en ambos sentidos. En matemáticas es el 'si y sólo si': la tesis es a la vez necesaria Y suficiente para la hipótesis.",
        "[EXPERTO]  (Sesión 1) A ↔ B comprueba que dos circuitos/modelos son equivalentes: deben coincidir en TODA entrada. El XNOR es el bicondicional bit a bit (1 si las entradas son iguales) y se usa como detector de igualdad y como medida de coincidencia en redes lógicas binarizadas.",
    ],

    # ------------------- CAPÍTULO 1.2 — ÁLGEBRA DE BOOLE -------------------
    ("1.2  Álgebra de Boole", "¿Qué es un álgebra de Boole?"): [
        "[BÁSICO]  (Sesiones 1-2) Un álgebra de Boole es (B, ⊕, ⊙, ′) con al menos dos elementos 0 y 1 que cumple conmutativa, asociativa, distributiva, neutros (a⊕0=a, a⊙1=a) y complemento (a⊕a′=1, a⊙a′=0).\nEjemplo de clase: B={0,1} con + y · es la menor álgebra de Boole.",
        "[INTERMEDIO]  (Sesión 2) Ejemplo de clase: las partes de A={1,2,3}.\nP(A)={∅,{1},{2},{3},{1,2},{1,3},{2,3},{1,2,3}}.\nCon ⊕=∪, ⊙=∩: neutro de la suma 0=∅, neutro del producto 1=A, complemento X′=A∖X.\nSe cumple X∪X′=A y X∩X′=∅. Es un álgebra de Boole con 2³=8 elementos.",
        "[EXPERTO]  (Sesión 2) Producto de álgebras: B³={(x₁,x₂,x₃): xᵢ∈{0,1}} con operaciones componente a componente es otra álgebra de Boole (2³=8 elementos).\nEs el modelo de los registros de n bits y de los vectores de features binarios: cada operación lógica actúa en paralelo sobre las n coordenadas (bit-parallelism de la CPU y de las redes binarizadas).",
    ],

    ("1.2  Álgebra de Boole", "Elemento complementario"): [
        "[BÁSICO]  (Sesión 2) El complemento x′ cumple x ⊕ x′ = 1 y x ⊙ x′ = 0.\nEn B={0,1}: 0′=1 y 1′=0.",
        "[INTERMEDIO]  (Sesión 2) En el álgebra (P(A), ∪, ∩, ′) con A={1,2,3}, el complemento es X′=A∖X:\n ∅′={1,2,3},  {1}′={2,3},  {2}′={1,3},  {3}′={1,2},\n {1,2}′={3},  {1,3}′={2},  {2,3}′={1},  {1,2,3}′=∅.\nSiempre X∪X′=A y X∩X′=∅.",
        "[EXPERTO]  (Sesión 2) Propiedades de clase: doble complemento x=(x′)′ y De Morgan ¬(x∨y)=¬x∧¬y, ¬(x∧y)=¬x∨¬y.\nEn una red binaria, negar dos veces es identidad (se compila a 'nada'), y De Morgan permite reescribir una capa de NANDs como ANDs+NOTs según convenga al hardware.",
    ],

    # --------------- CAPÍTULO 1.3 — FUNCIONES BOOLEANAS Y PUERTAS ---------------
    ("1.3  Funciones booleanas y puertas", "¿Qué es una función booleana?"): [
        "[BÁSICO]  (Sesión 2) Una función booleana es f: Bⁿ → B.\nCon n=1 hay 4: identidad f(x)=x; cero f(x)=0; uno f(x)=1; complemento f(x)=x′.\nLa identidad cumple f(0)=0, f(1)=1.",
        "[INTERMEDIO]  (Sesión 2) Con n=2:\n f(x,y)=x+y actúa como ∨: f(0,0)=0, f(0,1)=1, f(1,0)=1, f(1,1)=1.\n f(x,y)=x·y actúa como ∧: solo f(1,1)=1.\nUna función booleana de n variables queda fijada por su tabla de 2ⁿ filas.",
        "[EXPERTO]  (Sesión 2) Hay 2^(2ⁿ) funciones booleanas de n variables (n=2 → 16). Cada neurona de umbral implementa una de ellas, pero NO todas son realizables por una sola neurona (las no separables como XOR no): ese límite motiva las capas ocultas.",
    ],

    ("1.3  Funciones booleanas y puertas", "Puerta AND  —  símbolo y comportamiento"): [
        "[BÁSICO]  (Sesión 2) Tabla de la puerta AND:\n AND | y=0  y=1\n x=0 |  0    0\n x=1 |  0    1\nFunción booleana f(x,y)=x·y. Sale 1 solo si ambas entradas son 1.",
        "[INTERMEDIO]  (Sesión 2) La sesión modela AND como dos interruptores en SERIE: la corriente pasa solo si ambos están cerrados.\nEncadenando: x·y·z = AND de tres entradas, 1 solo si las tres valen 1. Coincide con el operador · del álgebra de Boole sobre {0,1}.",
        "[EXPERTO]  (Sesión 2) El acarreo del semisumador es Carry = a AND b. En IA, el AND con una máscara 0/1 'apaga' posiciones (multiplica por 0): p.ej. el causal mask de un Transformer pone a 0 las posiciones futuras antes del softmax.",
    ],

    ("1.3  Funciones booleanas y puertas", "Puerta OR  —  símbolo y comportamiento"): [
        "[BÁSICO]  (Sesión 2) Tabla de la puerta OR:\n OR | y=0  y=1\n x=0 |  0    1\n x=1 |  1    1\nFunción booleana f(x,y)=x+y. Sale 0 solo si ambas entradas son 0.",
        "[INTERMEDIO]  (Sesión 2) La sesión modela OR como dos interruptores en PARALELO: basta con uno cerrado para que pase la corriente.\nEncadenando: x+y+z = 1 si AL MENOS una entrada es 1.",
        "[EXPERTO]  (Sesión 2) La OR es la unión de criterios (A∪B). En un sistema de reglas, varias reglas que disparan la misma conclusión forman un gran OR; en hardware, la línea 'wired-OR' deja que cualquier emisor active la señal.",
    ],

    ("1.3  Funciones booleanas y puertas", "Puerta NOT  —  símbolo y comportamiento"): [
        "[BÁSICO]  (Sesión 2) La puerta NOT invierte el bit:\n NOT: x=0 → 1 ;  x=1 → 0.\nFunción booleana f(x)=x̄ (elemento de F₁).",
        "[INTERMEDIO]  (Sesión 2) Combinando NOT con AND/OR salen las puertas 'invertidas':\n NOR = ¬(x+y): solo 1 cuando ambas son 0.\n NAND = ¬(x·y): solo 0 cuando ambas son 1.\n XNOR = ¬(x⊻y) = x·y + x̄·ȳ: 1 cuando las entradas coinciden.",
        "[EXPERTO]  (Sesión 2) Un NOT(a) puede fabricarse con un solo NAND: a NAND a. Como {NAND} es funcionalmente completo, toda la lógica de un chip se construye repitiendo una única puerta: base del diseño CMOS y de compilar redes binarizadas a hardware homogéneo.",
    ],

    ("1.3  Funciones booleanas y puertas", "Suma y producto de funciones booleanas"): [
        "[BÁSICO]  (Sesión 2) Sobre el conjunto Fₙ de funciones booleanas se define punto a punto:\n (f+g)(x) = f(x) + g(x),\n (f·g)(x) = f(x) · g(x).\nCon ellas, (Fₙ, +, ·) es a su vez un álgebra de Boole.",
        "[INTERMEDIO]  (Sesión 2) F₁ tiene 4 elementos: identidad Id, cero, uno y complemento h(x)=x′.\nNeutros: la constante 0 para +, la constante 1 para ·.\nComplemento de f: f′(x)=(f(x))′. Verifica f + f′ = 1 y f · f′ = 0 como funciones.",
        "[EXPERTO]  (Sesión 2) Que las funciones formen un álgebra de Boole legitima simplificar fórmulas ANTES de construir el circuito (Karnaugh, Quine-McCluskey): operamos con funciones como con valores, sin enumerar las 2ⁿ entradas.",
    ],

    ("1.3  Funciones booleanas y puertas", "Trazar un circuito paso a paso (Ejemplo 1 del manual)"): [
        "[BÁSICO]  (Sesión 2) Circuito de clase: una OR recibe x,y; su salida entra con z en una AND.\nFunción asociada: f(x,y,z) = (x+y)·z.\nEvalúa x=1, y=0, z=1: (1+0)·1 = 1·1 = 1.",
        "[INTERMEDIO]  (Sesión 2) Tabla de f(x,y,z)=(x+y)·z mirando z primero:\n z=0 → siempre 0 (la AND con 0 anula todo).\n z=1 → vale (x+y): 0 solo si x=y=0.\nAsí f=1 en (0,1,1), (1,0,1), (1,1,1) y 0 en el resto.",
        "[EXPERTO]  (Sesión 2) Trazar = evaluar en orden topológico (primero las puertas sin dependencias). Es el mismo recorrido que el forward pass de una red: cada nodo espera a sus entradas. El grafo del circuito es un DAG y su profundidad marca la latencia (camino crítico).",
    ],

    # ----------------- CAPÍTULO 1.4 — LÓGICA DE PREDICADOS -----------------
    ("1.4  Lógica de predicados", "¿Qué es un predicado?"): [
        "[BÁSICO]  (Sesión 3) Un predicado p(x) es una afirmación con variables; al sustituir por valores concretos se vuelve proposición con valor de verdad.\np(x)='x es un reptil': p(serpiente)=V, p(gato)=F.",
        "[INTERMEDIO]  (Sesión 3) Predicado de varias variables: p(x,y) = 'x+y=3'.\np(1,2)=V; p(1,1)=F.\nUn predicado NO tiene valor de verdad por sí mismo: lo adquiere al fijar sus argumentos o al cuantificarlo.",
        "[EXPERTO]  (Sesión 3) La lógica de primer orden (predicados + ∀/∃) es más expresiva que la proposicional: habla de relaciones entre objetos. Es la base de los Knowledge Graphs y de la lógica de descripción (OWL), donde p(x,y) modela aristas tipadas entre entidades.",
    ],

    ("1.4  Lógica de predicados", "Negación de cuantificadores (Morgan generalizado)"): [
        "[BÁSICO]  (Sesión 3) De Morgan generalizado:\n ¬[∀x, p(x)] ≡ ∃x: ¬p(x).\n ¬[∃x: p(x)] ≡ ∀x, ¬p(x).\nNegar un 'para todo' produce un 'existe un contraejemplo'.",
        "[INTERMEDIO]  (Sesión 3) Ejemplo de clase: 'no es cierto que todo entero sea a la vez par y positivo':\n ¬[∀x∈ℤ, (p(x) ∧ q(x))]\n ≡ ∃x∈ℤ: ¬(p(x) ∧ q(x))\n ≡ ∃x∈ℤ: ¬p(x) ∨ ¬q(x)\n= 'existe un entero que o bien es impar o bien no es positivo'.",
        "[EXPERTO]  (Sesión 3) Negación anidada: ∀x ¬[∃y: (p(x,y)→q(x))] se reescribe empujando la negación hacia dentro hasta ∀x ∀y [p(x,y) ∧ ¬q(x)].\nLos SAT/SMT-solvers normalizan así a forma prenex/NNF antes de buscar; cada cuantificador se invierte al cruzar la negación.",
    ],

    ("1.4  Lógica de predicados", "¡El ORDEN de los cuantificadores importa!"): [
        "[BÁSICO]  (Sesión 3) Los cuantificadores NO conmutan. En ℕ:\n ∀x ∃y: y>x  → V ('para cada natural hay otro mayor').\n ∃y ∀x: y>x  → F ('hay un natural mayor que todos').",
        "[INTERMEDIO]  (Sesión 3) La diferencia está en la dependencia: en ∀x ∃y, la y puede depender de x (eliges y=x+1). En ∃y ∀x, la misma y debe servir para TODOS los x: imposible en ℕ. Intercambiar ∀ y ∃ puede cambiar el valor de verdad.",
        "[EXPERTO]  (Sesión 3) Es la diferencia entre 'todo cliente tiene un plan' (∀∃) y 'hay un plan para todos' (∃∀). En la definición ε–δ de límite, ∀ε ∃δ: el δ depende de ε; invertirlo daría 'continuidad uniforme', una propiedad estrictamente más fuerte.",
    ],

    # ------------------- CAPÍTULO 1.5 — LÓGICA INDUCTIVA -------------------
    ("1.5  Lógica inductiva", "¿Qué es la lógica INDUCTIVA?"): [
        "[BÁSICO]  (Sesión 3) La lógica inductiva va de lo PARTICULAR a lo GENERAL y sus conclusiones no están garantizadas.\nEjemplo de clase: 'en todos los videojuegos jugados con orcos llevábamos espada' ⟹ 'en todo juego con orcos el personaje llevará espada'. Probable, no seguro.",
        "[INTERMEDIO]  (Sesión 3) Contraste: la DEDUCCIÓN conserva la verdad (si las premisas son ciertas, la conclusión lo es); la INDUCCIÓN solo la sugiere a partir de un patrón observado.\nUn solo contraejemplo (un juego con orcos sin espada) tumba la regla inducida.",
        "[EXPERTO]  (Sesión 3) El aprendizaje supervisado ES inducción: de un conjunto finito de ejemplos etiquetados se infiere una hipótesis general aplicable a datos nuevos. Por eso siempre hay riesgo de error de generalización; la regularización y la validación acotan ese salto inductivo.",
    ],

    ("1.5  Lógica inductiva", "Árbol de decisión (ejemplo del examen)"): [
        "[BÁSICO]  (Sesión 3) Reglas del ejemplo de clase:\n Si Dedicación=Alta → Aprobar.\n Si Dedicación=Media ∧ Dificultad=Media ∧ Tipo=Test → Aprobar.\n Si Dedicación=Media ∧ Dificultad=Alta → No aprobar.\nCada regla es una conjunción de pares atributo=valor.",
        "[INTERMEDIO]  (Sesión 3) El árbol pregunta primero por Dedicación. Si 'Alta' → Aprobado (hoja directa). Si 'Media' → mira Dificultad; si 'Media' baja a Tipo; si Tipo=Test → Aprobado, si no → Suspenso.\nCada camino raíz→hoja es una regla SI…ENTONCES.",
        "[EXPERTO]  (Sesión 3) Esto es un árbol de decisión de ML: los nodos internos parten por el atributo más informativo (mayor ganancia de información / menor índice Gini). La Programación Lógica Inductiva induce justo estas reglas legibles desde ejemplos, frente a una red neuronal opaca.",
    ],

    # --------------- CAPÍTULO 1.6 — COMPLEJIDAD COMPUTACIONAL ---------------
    ("1.6  Complejidad computacional", "Introducción a la complejidad"): [
        "[BÁSICO]  (Sesión 3) La complejidad cuenta operaciones elementales según el tamaño n de la entrada.\nProducto escalar u·v en ℝⁿ: n productos + (n−1) sumas = 2n−1 operaciones → coste lineal O(n).",
        "[INTERMEDIO]  (Sesión 3) De clase:\n Suma de matrices n×n: n² sumas → O(n²).\n Producto de matrices n×n: 2n³ operaciones → O(n³).\n Sistema triangular n×n: n² operaciones → O(n²).\nLa O(·) se obtiene como límite c(n)/nᵏ → constante finita cuando n→∞.",
        "[EXPERTO]  (Sesión 3) El determinante por cofactores cuesta ≈ 2·n! → O(n!), inviable; por eso en la práctica se usa eliminación (LU) en O(n³). Entrenar una capa densa es O(E·N·n·m): lineal con los datos, cuadrático al ensanchar capas.",
    ],

    # ------------------- CAPÍTULO 1.7 — TEORÍA DE GRAFOS -------------------
    ("1.7  Teoría de grafos", "¿Qué es un grafo? (V, E, ψ)"): [
        "[BÁSICO]  (Sesión 4) Un grafo es una terna G=(V, E, γ): V vértices, E aristas y γ la aplicación de incidencia que asigna a cada arista el par de vértices que une.\nEjemplo: V={v₁,v₂,v₃}, E={e₁,e₂} con γ(e₁)={v₁,v₂}, γ(e₂)={v₂,v₃}.",
        "[INTERMEDIO]  (Sesión 4) La sesión admite aristas múltiples (varias e con el mismo par) y bucles (γ(e)={v,v}).\nUn grafo es SIMPLE si γ es inyectiva (sin aristas repetidas) y no tiene bucles. En ese caso se omite γ y se nombra la arista por su par {vᵢ,vⱼ}.",
        "[EXPERTO]  (Sesión 5) Un grafo se codifica como matriz de adyacencia A: A(i,j)=1 si hay arista. Para grafos no dirigidos A es simétrica. Las GNN propagan información por esta A; la potencia Aᵏ cuenta los caminos de longitud k entre vértices.",
    ],

    ("1.7  Teoría de grafos", "Grafo dirigido vs no dirigido"): [
        "[BÁSICO]  (Sesión 4) En un grafo DIRIGIDO γ: E→V×V asigna a cada arista un par ORDENADO (origen, destino), dibujado con flecha.\nEjemplo: γ(e₁)=(v₁,v₂), γ(e₂)=(v₁,v₃), γ(e₃)=(v₂,v₃), γ(e₄)=(v₃,v₄).",
        "[INTERMEDIO]  (Sesiones 4-5) No dirigido: la arista {vᵢ,vⱼ} se recorre en ambos sentidos → matriz de adyacencia simétrica.\nDirigido: (vᵢ,vⱼ) ≠ (vⱼ,vᵢ) → la matriz NO tiene por qué ser simétrica. Un bucle (v,v) une un vértice consigo mismo.",
        "[EXPERTO]  (Sesión 4) Una red neuronal es un grafo dirigido y ponderado: aristas con peso ωᵢⱼ y dirección de la información (forward). El backprop recorre el MISMO grafo al revés. Un grafo de cómputo debe ser acíclico (DAG) para poder ordenarse topológicamente.",
    ],

    ("1.7  Teoría de grafos", "Caminos y conexión"): [
        "[BÁSICO]  (Sesión 4) Un grafo es CONEXO si entre cada par de vértices existe algún camino (sucesión de aristas adyacentes) que los une.\nEjemplo conexo: aristas {1,2},{1,3},{2,3},{3,4},{3,5},{4,5} sobre 5 vértices: desde cualquiera se llega a cualquiera.",
        "[INTERMEDIO]  (Sesión 4) Ejemplo NO conexo de clase: aristas {1,2},{1,3},{2,3},{4,5}.\n{1,2,3} forman una componente y {4,5} otra: no hay camino entre 3 y 4. El grafo se parte en componentes conexas.",
        "[EXPERTO]  (Sesión 4) La conexión se detecta con BFS/DFS en O(|V|+|E|). En la matriz A hay camino entre i y j si alguna potencia Aᵏ tiene entrada (i,j)>0. Las componentes conexas equivalen a los bloques de la clausura transitiva: clave para clustering de grafos y propagación en GNN.",
    ],

    ("1.7  Teoría de grafos", "Grafos y redes neuronales"): [
        "[BÁSICO]  (Sesión 4) Una red neuronal es un grafo dirigido (V,E) donde cada nodo i tiene estado aᵢ∈[0,1], cada arista (i,j) un peso ωᵢⱼ, cada nodo un sesgo bᵢ y una activación fᵢ.",
        "[INTERMEDIO]  (Sesión 4) Cada neurona calcula:\n aᵢ = fᵢ( Σⱼ ωⱼᵢ aⱼ + bᵢ ).\nEs la suma ponderada de las entradas más el sesgo, pasada por la activación. La estructura del grafo (qué nodo conecta con cuál) define la arquitectura.",
        "[EXPERTO]  (Sesión 4) Apilar estas ecuaciones por capas da el forward pass; como el grafo es un DAG, se evalúa en orden topológico. El backprop recorre las MISMAS aristas al revés con la regla de la cadena. Los pesos ωᵢⱼ son las entradas de la matriz de adyacencia ponderada.",
    ],

    # ------------------- CAPÍTULO 2.1 — TEORÍA DE CONJUNTOS -------------------
    ("2.1  Teoría de conjuntos", "Conjuntos: definición y pertenencia"): [
        "[BÁSICO]  (Sesión 1) Un conjunto es una colección de elementos; a∈A significa 'a pertenece a A'.\nEjemplos: planetas={Mercurio,…,Neptuno}; impares={1,3,5,…}={2n−1 | n∈ℕ}.\nLos elementos no se repiten: {a,b,c,c,d,a} se escribe {a,b,c,d}.",
        "[INTERMEDIO]  (Sesión 1) El cardinal |A| es el nº de elementos: |planetas|=8; |impares|=∞.\nEl conjunto vacío ∅ no tiene elementos (los satélites de Venus = ∅).\nUn conjunto puede darse por extensión {2,4,6} o por comprensión {x : x es par}.",
        "[EXPERTO]  (Sesión 1) En IA un conjunto modela el vocabulario, las clases o un dataset, sin orden ni repetición. La comprensión {x : P(x)} es exactamente un filtro booleano; el cardinal |·| da el soporte usado en probabilidad (Laplace) y en métricas como Jaccard = |A∩B|/|A∪B|.",
    ],

    ("2.1  Teoría de conjuntos", "Inclusión y subconjuntos (⊆, ⊊)"): [
        "[BÁSICO]  (Sesión 3) A⊆B si todo elemento de A está en B.\n{a,b,c} ⊆ {a,b,c,d} ✔; pero {a,b,c,d} ⊄ {a,b,c} porque d∉{a,b,c}.\nAdemás ∅ ⊆ A para todo conjunto A.",
        "[INTERMEDIO]  (Sesión 3) Puede no haber ninguna inclusión: A={1,3,4}, B={1,2,4}: 3∈A∉B y 2∈B∉A, así A⊄B y B⊄A.\nDos conjuntos son IGUALES si A⊆B y B⊆A; por eso {a,b,c}={b,c,a} (el orden no cuenta).",
        "[EXPERTO]  (Sesión 3) Probar A=B por doble inclusión (A⊆B y B⊆A) es la técnica estándar de demostración y de verificación de equivalencia de especificaciones. La inclusión define el orden parcial del retículo de subconjuntos, que es un álgebra de Boole.",
    ],

    ("2.1  Teoría de conjuntos", "Leyes de De Morgan en conjuntos"): [
        "[BÁSICO]  (Sesión 3) Con un universo U, el complemento Aᶜ={x∈U : x∉A}.\nLa diferencia B∖A son los elementos de B que no están en A.\nRelación de clase: B∖A = B ∩ Aᶜ.",
        "[INTERMEDIO]  (Sesión 3) De Morgan en conjuntos: (A∪B)ᶜ = Aᶜ∩Bᶜ y (A∩B)ᶜ = Aᶜ∪Bᶜ.\nEjemplo de clase: A={a,b,c,f}, B={b,c,e,f,g,j} → B∖A={e,g,j}.\nSi A∩B=∅ entonces B∖A=B (nada que quitar).",
        "[EXPERTO]  (Sesión 3) De Morgan en conjuntos es el espejo de De Morgan en lógica (∪↔∨, ∩↔∧, ᶜ↔¬). En máscaras de NumPy, ~(m1 | m2) == (~m1) & (~m2): elegir la forma con menos negaciones de array ahorra una pasada de memoria O(n).",
    ],

    # --------------- CAPÍTULO 2.2 — RELACIONES Y APLICACIONES ---------------
    ("2.2  Relaciones y aplicaciones", "Producto cartesiano A × B"): [
        "[BÁSICO]  (Sesión 3) A×B es el conjunto de pares ORDENADOS (a,b) con a∈A, b∈B.\nA={1,2,3}, B={α,β}:\nA×B={(1,α),(1,β),(2,α),(2,β),(3,α),(3,β)}.\n|A×B| = |A|·|B| = 3·2 = 6.",
        "[INTERMEDIO]  (Sesión 3) El orden importa: (1,α) ≠ (α,1), así que en general A×B ≠ B×A.\nUna relación binaria de A en B es cualquier subconjunto de A×B; una aplicación f:A→B es una relación especial: cada a∈A aparece en exactamente un par.",
        "[EXPERTO]  (Sesión 3) A×B es el espacio de combinaciones: en ML, el grid de hiperparámetros es un producto cartesiano (lr × batch × capas) y su cardinal explica la explosión del grid-search. Los pares ordenados también modelan las aristas dirigidas de un grafo (⊆ V×V).",
    ],

    ("2.2  Relaciones y aplicaciones", "Aplicaciones (funciones) entre conjuntos"): [
        "[BÁSICO]  (Sesiones 3-4) f:A→B es una aplicación si asigna a CADA a∈A un ÚNICO b∈B: ∀a∈A ∃!b∈B con f(a)=b.\nA={1,2,3}, B={1,3,5,8}, f(1)=3, f(2)=5, f(3)=3 es aplicación: Dom(f)={1,2,3}, Im(f)={3,5}.",
        "[INTERMEDIO]  (Sesiones 3-4) NO es aplicación si:\n • un elemento tiene dos imágenes: f(1)=1 y f(1)=3 a la vez, o\n • un elemento se queda sin imagen: no se define f(2).\nLa imagen inversa f⁻¹(C)={x∈A : f(x)∈C} recupera qué entradas caen en C.",
        "[EXPERTO]  (Sesión 4) La composición (g∘f)(a)=g(f(a)) es cómo se encadenan las capas de una red: cada capa es una aplicación y la red es f_L∘…∘f₁. Que dominio y codominio 'casen' es la condición de shape entre capas; la regla de la cadena deriva esta composición.",
    ],

    # --------------------- CAPÍTULO 2.3 — COMBINATORIA ---------------------
    ("2.3  Combinatoria", "Permutaciones Pₙ = n!"): [
        "[BÁSICO]  (Sesión 4) Una permutación sin repetición ordena n elementos distintos; hay Pₙ=n! ordenaciones.\nA={a,b,c,d}: P₄=4!=4·3·2·1=24 (abcd, bdca, dabc…).",
        "[INTERMEDIO]  (Sesión 4) Permutación CON repetición: reordenar la palabra 'aabbbc'.\nr=3 tipos: n₁=2 (a), n₂=3 (b), n₃=1 (c), total 6 letras.\nP = 6!/(2!·3!·1!) = 720/12 = 60 palabras distintas.",
        "[EXPERTO]  (Sesión 4) n! crece más rápido que cualquier exponencial: por eso recorrer todas las permutaciones (fuerza bruta del TSP) es O(n!) e inviable. El multinomial n!/(n₁!···nᵣ!) reaparece en la distribución multinomial y en el conteo de microestados (entropía).",
    ],

    ("2.3  Combinatoria", "Variaciones V(n,k)"): [
        "[BÁSICO]  (Sesión 4) Una variación sin repetición elige k de n con orden y sin repetir: V(n,k)=n!/(n−k)!.\nNúmeros de 2 cifras con {1,2,3,4}: V(4,2)=4!/2!=12.\nPalabras de 4 letras con {a,e,i,s,m,l,j}: V(7,4)=7!/3!=840.",
        "[INTERMEDIO]  (Sesión 4) Variación CON repetición: VR(n,k)=nᵏ.\nNúmeros de 2 cifras con {1,2,3,4} repitiendo: VR(4,2)=4²=16.\nResultados al lanzar un dado 4 veces: VR(6,4)=6⁴=1296.\nDiferencia con la combinación: en la variación el ORDEN importa.",
        "[EXPERTO]  (Sesión 4) VR(n,k)=nᵏ cuenta las secuencias de longitud k sobre un alfabeto de n símbolos: las cadenas posibles de un tokenizer, o las hojas de un árbol k-ario. Es el tamaño del espacio de salida en generación autorregresiva y explica por qué se usa búsqueda (beam) en vez de enumerar.",
    ],

    # ------------------ CAPÍTULO 2.4 — ESPACIOS VECTORIALES ------------------
    ("2.4  Espacios vectoriales", "Definición y axiomas"): [
        "[BÁSICO]  (Sesiones 4-5) Un vector de ℝⁿ es una lista ordenada (v₁,…,vₙ) de reales.\nSuma: v+w=(v₁+w₁,…,vₙ+wₙ). Producto por escalar: λ·v=(λv₁,…,λvₙ).\nEjemplo: v=(1,−2/3)∈ℝ², w=(√2,−1.2,π)∈ℝ³.",
        "[INTERMEDIO]  (Sesiones 4-5) Producto escalar: v·w = Σ vᵢwᵢ.\nv=(2,−1,0), w=(−3,−2,1): v·w = −6+2+0 = −4.\nNorma euclídea ‖v‖₂=√(Σvᵢ²). Un espacio vectorial (V,+,·) sobre ℝ cumple conmutativa, asociativa, vector 0, opuesto y compatibilidad con escalares.\nEjemplo de clase: V={(x,y,z)∈ℝ³ : 3x+4y+5z=0} es e.v.",
        "[EXPERTO]  (Sesiones 4-5) Ortogonalidad: u·v=‖u‖‖v‖cos(θ), y u⊥v ⟺ u·v=0. La proyección Projᵥ(u)=(u·v / v·v)·v es la base de mínimos cuadrados.\nEn ML el error se mide con una norma de (v̂−v): MSE = ‖v̂−v‖²/n. El producto escalar es la similitud (coseno) entre embeddings.",
    ],

    ("2.4  Espacios vectoriales", "Combinación lineal"): [
        "[BÁSICO]  (Sesiones 4-5) Una combinación lineal de v₁,…,v_k es a₁v₁+…+a_kv_k con escalares aᵢ.\nCon U=(1,3,−2), V=(5,1,0): W es combinación lineal de U,V si existen α,β con αU+βV=W.",
        "[INTERMEDIO]  (Sesiones 4-5) ¿Es W₁=(14,0,2) combinación lineal de U=(1,3,−2), V=(5,1,0)?\nResolver α+5β=14, 3α+β=0, −2α=2 → α=−1, β=3, y comprobar 3(−1)+3=0 ✔.\nSí: W₁=−U+3V. (En cambio W₂=(1,1,1) NO sale del sistema.)",
        "[EXPERTO]  (Sesiones 4-5) Toda capa lineal de una red calcula combinaciones lineales de sus entradas (Wx) antes de la activación. El conjunto de TODAS las combinaciones lineales de unos vectores es su 'span' (subespacio generado): '¿W es combinación lineal?' es '¿W está en el span?'.",
    ],

    ("2.4  Espacios vectoriales", "Sistemas generadores y bases"): [
        "[BÁSICO]  (Sesión 5) S={v₁,…,v_k} GENERA V si todo vector de V es combinación lineal de S.\nUna BASE es un sistema generador que además es linealmente independiente.",
        "[INTERMEDIO]  (Sesión 5) Ejemplo de clase: U=(1,3,−2), V=(5,1,0), W=(1,1,1) forman una BASE de ℝ³: son 3 vectores linealmente independientes (su único 0 es la combinación trivial) y generan todo ℝ³.\nEn una base, cada vector se escribe de forma ÚNICA como combinación de ella.",
        "[EXPERTO]  (Sesión 5) Una base son las 'coordenadas' del espacio. Cambiar de base = multiplicar por una matriz; PCA elige una base ortonormal (autovectores de la covarianza) que concentra la varianza, permitiendo truncar dimensiones con mínima pérdida.",
    ],

    ("2.4  Espacios vectoriales", "Dimensión y rango"): [
        "[BÁSICO]  (Sesión 5) El rango de A∈ℝ^{m×n} es el nº máximo de columnas linealmente independientes.\nLa dimensión de un espacio es el nº de vectores de cualquiera de sus bases.",
        "[INTERMEDIO]  (Sesión 5) Para A∈ℝ^{n×n} son equivalentes:\n A es regular (invertible) ⟺ det(A)≠0 ⟺ rank(A)=n.\nSi rank(A)<n, las columnas son dependientes y A no tiene inversa.\nRecuerda: el producto de matrices NO es conmutativo (en general AB≠BA).",
        "[EXPERTO]  (Sesión 5) El rango = nº de valores singulares no nulos (SVD). Una matriz de datos casi de rango bajo se comprime bien (PCA/SVD truncada). En regresión, XᵀX es invertible solo si X tiene rango completo de columnas; si no, hay colinealidad y se usa la pseudoinversa o Ridge.",
    ],

}

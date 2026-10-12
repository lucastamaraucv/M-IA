/* ──────────── Modo Maestro Matemáticas: temario de 02MIAR (VIU) ────────────
   Grupo A (núcleo de IA, se estudia primero) + Grupo B (fundamentos discretos).
   Cada tema: {sesion, name, theory, workedExample, aiWhy, question, type,
   options?, correct, decimals?, solution}. Preguntas extraídas VERBATIM de
   fuentes ya verificadas (examen de 17 preguntas, notebook de Lucas, foro de
   Markov, investigación de ILP/BLP) — no generadas desde cero, así que no
   requieren el checklist anti-alucinación de An et al. 2025.
   Gotcha: todo backslash de LaTeX va DOBLE (\\frac, \\lambda...) o el
   navegador lo rompe (mismo bug que en EX, ver memoria de escapes JS). */
const EX_MATH = [
{sesion:'S4–S6 · Álgebra lineal', name:'Vectores, matrices, determinantes y normas',
 theory:`Un vector $v\\in\\mathbb{R}^n$ es una $n$-tupla de números; el producto matricial se define
 elemento a elemento como $(AB)_{ij}=\\sum_k A_{ik}B_{kj}$; la norma euclídea de un vector es
 $\\|v\\|=\\sqrt{\\sum_i v_i^2}$. El determinante mide cómo una matriz "escala" volúmenes, y tiene
 tres propiedades clave para esta sesión: $\\det(cM)=c^n\\det(M)$ para $M$ de tamaño $n\\times n$,
 $\\det(A^{-1})=1/\\det(A)$, y si $B$ es diagonalizable, $\\det(B)$ es el producto de todos sus
 autovalores (con multiplicidad).`,
 workedExample:`Sea $A=\\begin{bmatrix}1&2\\\\0&3\\end{bmatrix}$, con $\\det(A)=3$. Al duplicar la matriz,
 $2A=\\begin{bmatrix}2&4\\\\0&6\\end{bmatrix}$, y su determinante es $12$. Comprueba la propiedad:
 $\\det(2A)=2^2\\cdot\\det(A)=4\\cdot 3=12$ ✓ — el exponente es el tamaño $n$ de la matriz (aquí $n=2$),
 no una constante fija. Esta es exactamente la propiedad que resuelve la pregunta de práctica,
 pero con $n=4$.`,
 aiWhy:`Cada capa de una red neuronal es literalmente un producto matricial ($Wx+b$); los
 embeddings de palabras, imágenes o usuarios son vectores en espacios de cientos o miles de
 dimensiones, y la norma (L2) se usa para regularizar pesos y para medir similitud (coseno) entre
 embeddings.`,
 question:`Sea $A\\in\\mathbb{R}^{4\\times4}$ una matriz tal que $\\det(A)=-9$ y $B\\in\\mathbb{R}^{4\\times4}$
 una matriz diagonalizable con polinomio característico $P_B(\\lambda)=(\\lambda^2-4)(\\lambda^2-1)$.
 Calcule $\\det(3A^{-1}B)$.`,
 type:'numeric', correct:-36, decimals:0,
 solution:`Los autovalores de $B$ son las raíces de $(\\lambda^2-4)(\\lambda^2-1)=(\\lambda-2)(\\lambda+2)(\\lambda-1)(\\lambda+1)$,
 es decir $\\lambda=2,-2,1,-1$ (4 raíces simples para una matriz $4\\times4$: son todos los autovalores).
 $\\det(B)=2\\cdot(-2)\\cdot1\\cdot(-1)=4$. Aplicando las tres propiedades:
 $\\det(3A^{-1}B)=3^4\\cdot\\det(A^{-1})\\cdot\\det(B)=81\\cdot\\frac{1}{-9}\\cdot4=81\\cdot\\left(-\\frac{4}{9}\\right)=-36$.`},

{sesion:'S7 · Diagonalización', name:'Diagonalización y matrices simétricas',
 theory:`Una matriz $A$ es diagonalizable si $A=PDP^{-1}$ con $D$ diagonal (los autovalores en la
 diagonal). Si $A$ es triangular (superior o inferior), sus autovalores son directamente los
 elementos de su diagonal principal. Cada autovalor $\\lambda$ tiene una multiplicidad algebraica
 $m_a(\\lambda)$ (veces que aparece como raíz del polinomio característico) y una multiplicidad
 geométrica $m_g(\\lambda)=\\dim(\\ker(A-\\lambda I))$. $A$ es diagonalizable si y solo si
 $m_g(\\lambda)=m_a(\\lambda)$ para todo autovalor.`,
 workedExample:`Sea $A=\\begin{bmatrix}2&1\\\\0&2\\end{bmatrix}$ (triangular, autovalor $2$ con $m_a=2$).
 $A-2I=\\begin{bmatrix}0&1\\\\0&0\\end{bmatrix}$ tiene rango $1$, así que $m_g(2)=2-1=1\\neq m_a(2)=2$
 — esta matriz NO es diagonalizable (es el ejemplo clásico de bloque de Jordan). Contrástalo con la
 pregunta de práctica, donde para $k=1$ sí se cumple la igualdad de multiplicidades.`,
 aiWhy:`PCA diagonaliza la matriz de covarianza de los datos — y como esa matriz siempre es
 simétrica, el teorema espectral GARANTIZA que siempre es diagonalizable (con autovectores
 ortogonales). SVD generaliza esta idea a matrices no cuadradas y es la base de la compresión de
 embeddings y de los sistemas de recomendación.`,
 question:`Sea $k\\in\\mathbb{R}$ y $A=\\begin{bmatrix}1&k^2-1&-1\\\\0&1&k\\\\0&0&2\\end{bmatrix}$. Entonces:`,
 type:'mc',
 options:['Los autovalores de A son 1 y 2; y si k=1, A no es diagonalizable.',
   'Los autovalores de A son 1 y 2; y si k=1, A es diagonalizable.',
   'Los autovalores de A son 1 y 2; y m_a(1)=1, m_a(2)=2.',
   'A tiene tres autovalores distintos.'],
 correct:1,
 solution:`$A$ es triangular superior: sus autovalores son $1,1,2$ → $m_a(1)=2$, $m_a(2)=1$ (descarta
 la opción c, que intercambia las multiplicidades, y la d, que dice "tres autovalores distintos").
 Con $k=1$: $A-I=\\begin{bmatrix}0&0&-1\\\\0&0&1\\\\0&0&1\\end{bmatrix}$ tiene rango $1$ (todas las filas
 no nulas son múltiplos de $(0,0,1)$), así que $m_g(1)=3-1=2=m_a(1)$. Para $\\lambda=2$ (con
 $m_a=1$) siempre $m_g=1$. Como ambas multiplicidades coinciden para los dos autovalores, $A$ es
 diagonalizable cuando $k=1$. Respuesta correcta: b).`},

{sesion:'S8–S9 · Cálculo diferencial', name:'Regla de la cadena (univariable y multivariable)',
 theory:`Para $f:\\mathbb{R}\\to\\mathbb{R}^2$ compuesta con $g:\\mathbb{R}^2\\to\\mathbb{R}$, la regla de la
 cadena da $(g\\circ f)'(t)=\\nabla g(f(t))\\cdot f'(t)$ — el producto escalar del gradiente de $g$ con
 el vector derivada de $f$. En general, para varias variables, cada derivada parcial de una
 composición es una SUMA de productos de derivadas parciales, una por cada "camino" en el grafo de
 dependencias.`,
 workedExample:`Caso simple univariable: $h(x)=\\sin(x^2)$ → $h'(x)=\\cos(x^2)\\cdot 2x$ (derivada de la
 función externa por la derivada de la interna). Caso multivariable resuelto: sean
 $g(s,t)=(se^t, se^{-t})$ y $f(x,y)=\\ln\\sqrt{x^2+y^2}$. $\\partial_s(f\\circ g)=\\partial_x f\\cdot\\partial_s g_1+\\partial_y f\\cdot\\partial_s g_2$.
 En $(s,t)=(1,0)$: $(x,y)=(1,1)$, $\\partial_x f=\\partial_y f=\\tfrac12$, $\\partial_s g_1=\\partial_s g_2=1$
 → $\\partial_s(f\\circ g)(1,0)=\\tfrac12\\cdot1+\\tfrac12\\cdot1=1$.`,
 aiWhy:`Backpropagation ES la regla de la cadena aplicada capa por capa: para entrenar una red se
 necesita $\\partial \\text{Loss}/\\partial w$ para cada peso, y eso se calcula acumulando productos de
 derivadas parciales desde la salida hacia la entrada (reverse-mode automatic differentiation). Sin
 la regla de la cadena no existe el entrenamiento de ningún modelo.`,
 question:`Sea $f:\\mathbb{R}\\to\\mathbb{R}^2$ de la forma $f(t)=(f_1(t),f_2(t))$ y $g:\\mathbb{R}^2\\to\\mathbb{R}$,
 tales que $f(0)=(1,0)$, $f_1'(0)=-2$, $f_2'(0)=1$, $\\partial g/\\partial x(1,0)=1$,
 $\\partial g/\\partial y(1,0)=4$. Calcule el valor de $(g\\circ f)'(0)$.`,
 type:'numeric', correct:2, decimals:0,
 solution:`$(g\\circ f)'(0)=\\nabla g(f(0))\\cdot f'(0)=\\partial_x g(1,0)\\cdot f_1'(0)+\\partial_y g(1,0)\\cdot f_2'(0)$.
 Como $f(0)=(1,0)$, las derivadas parciales de $g$ ya están evaluadas justo en ese punto.
 Sustituyendo: $(1)(-2)+(4)(1)=-2+4=2$.`},

{sesion:'S9 + investigación · Puntos críticos y Hessiana', name:'Puntos críticos, Hessiana y descenso de gradiente',
 theory:`Un punto crítico cumple $\\nabla f=0$. El Hessiano $H$ (matriz de segundas derivadas
 parciales) clasifica ese punto: definido positivo (todos los autovalores $>0$) → mínimo; definido
 negativo (todos $<0$) → máximo; indefinido (autovalores de signos opuestos) → punto de silla. El
 descenso de gradiente, $x_{k+1}=x_k-\\gamma\\nabla f(x_k)$, se DETIENE donde $\\nabla f=0$ — pero eso
 no le dice si ese punto es un mínimo, un máximo o una silla.`,
 workedExample:`Del notebook de ejercicios evaluables: $f(x)=3x^4+4x^3-12x^2+7$, con
 $f''(x)=36x^2+24x-24$. Puntos críticos: $x=-2$ ($f''=72>0$, mínimo global), $x=0$ ($f''=-24<0$,
 máximo local), $x=1$ ($f''=36>0$, mínimo local). Si el descenso de gradiente arranca exactamente en
 $x_0=0$, se queda atascado ahí en 0 iteraciones — aunque sea un MÁXIMO, no un mínimo, el método no
 lo distingue. Caso 2D: $g(x,y)=x^2+y^3+3xy+1$ tiene $P_1=(0,0)$ (silla, $\\det H=-9<0$) y
 $P_2=(-9/4,3/2)$ (mínimo, $\\det H=9>0$); arrancando en $(-1,1)$ el algoritmo converge a $P_2$ en
 3139 iteraciones (deseable), pero arrancando exactamente en $(0,0)$ se queda atascado en la silla.`,
 aiWhy:`El artículo de Schaeffer & McCalla (resumido en la investigación de Lucas sobre ILP/BLP,
 pregunta 15) demuestra que, con inicialización aleatoria uniforme, la probabilidad de que el
 descenso de gradiente converja a un punto de silla estricto es CERO — verificado con una
 simulación de Monte Carlo de 5000 inicializaciones (100% terminó en un mínimo, 0% en la silla). La
 pregunta 14 de esa misma investigación señala una trampa sutil: un máximo local estricto también
 tiene "al menos un autovalor negativo", así que una definición descuidada de "punto de silla" lo
 confundiría con un máximo — hay que mirar TODOS los autovalores, no solo si existe uno negativo.
 Calcular ese Hessiano completo es caro en redes grandes: el paper de tensores del foro (Laue et
 al. 2020) resuelve justo eso con notación de Einstein, con hasta 100.000x de mejora.`,
 question:`Sea $f:\\mathbb{R}^2\\to\\mathbb{R}$ dada por $f(x,y)=1-x^2-y^2$. Entonces:`,
 type:'mc',
 options:['f no tiene puntos críticos.',
   '(0,0) es un punto crítico de f y se trata de un mínimo relativo.',
   '(0,0) es un punto crítico de f y se trata de un máximo relativo.',
   '(0,0) es un punto crítico de f y se trata de un punto de silla.'],
 correct:2,
 solution:`$\\nabla f=(-2x,-2y)=0 \\Rightarrow (0,0)$ es el único punto crítico (descarta a). El
 Hessiano es $H=\\begin{bmatrix}-2&0\\\\0&-2\\end{bmatrix}$, con autovalores $-2,-2$: ambos negativos →
 definido negativo → $(0,0)$ es un máximo relativo (de hecho global, ya que
 $f(x,y)=1-x^2-y^2\\leq1=f(0,0)$ siempre). Respuesta correcta: c).`},

{sesion:'Probabilidad', name:'Bayes, independencia y valor esperado',
 theory:`Teorema de Bayes: $P(H|E)=\\dfrac{P(E|H)\\,P(H)}{P(E)}$, con $P(E)=\\sum_i P(E|H_i)P(H_i)$.
 Independencia: $A$ y $B$ son independientes si y solo si $P(A\\cap B)=P(A)\\cdot P(B)$. Valor
 esperado de una variable discreta: $E[X]=\\sum_x x\\cdot P(X=x)$.`,
 workedExample:`¿Cuánto debe restar una pregunta incorrecta en un examen tipo test con 5 respuestas
 posibles para que la puntuación esperada al azar sea 0? Con $P(\\text{acierto})=1/5$ y
 $P(\\text{fallo})=4/5$, y penalización $x$: $E=\\tfrac15(1)-\\tfrac45x=0 \\Rightarrow x=\\tfrac{1/5}{4/5}=\\tfrac14$.`,
 aiWhy:`El teorema de Bayes es el corazón de los clasificadores Naive Bayes y de las redes
 bayesianas — la investigación de Lucas sobre BLP/BILP (pregunta 6) demuestra computacionalmente
 que el POSTERIOR cambia con la evidencia (no solo el prior): con evidencia que solo una hipótesis
 explica, el ganador puede invertirse por completo. Cualquier sistema de IA que "actualiza
 creencias con evidencia" (filtros de spam, diagnóstico médico, ranking bayesiano) aplica
 exactamente esta fórmula.`,
 question:`En un grupo de personas, un 3% padece una enfermedad. Un test tiene 1% de falsos
 positivos y 3% de falsos negativos. ¿Cuál es la probabilidad de que alguien con test positivo
 padezca la enfermedad? (dos decimales, con coma)`,
 type:'numeric', correct:0.75, decimals:2,
 solution:`$P(\\text{Enf})=0{,}03$, $P(\\text{Sano})=0{,}97$. Sensibilidad: $P(+|\\text{Enf})=1-0{,}03=0{,}97$.
 Falso positivo: $P(+|\\text{Sano})=0{,}01$. Por Bayes:
 $P(\\text{Enf}|+)=\\dfrac{0{,}97\\times0{,}03}{0{,}97\\times0{,}03+0{,}01\\times0{,}97}=\\dfrac{0{,}0291}{0{,}0388}=0{,}75$.`},

{sesion:'Foro · Cadenas de Markov', name:'Cadenas de Markov y procesos estocásticos',
 theory:`Un proceso estocástico es una sucesión de variables aleatorias que evolucionan en el
 tiempo. Una cadena de Markov (tiempo y estados discretos) cumple la propiedad de Markov:
 $P(X_{n+1}=j\\mid X_n=i,X_{n-1},\\ldots)=P(X_{n+1}=j\\mid X_n=i)=p_{ij}$ — solo importa el presente,
 no la historia. Una matriz estocástica $P$ tiene filas $\\geq0$ que suman $1$. El vector de estado
 $v_n$ evoluciona como $v_{n+1}=v_n\\cdot P$. La distribución estacionaria $\\pi$ cumple
 $\\pi\\cdot P=\\pi$ con $\\sum_i\\pi_i=1$.`,
 workedExample:`Modelo del Clima (Soleado/Nublado/Lluvioso), con
 $P=\\begin{bmatrix}0{,}2&0{,}5&0{,}3\\\\0{,}1&0{,}6&0{,}3\\\\0{,}5&0{,}3&0{,}2\\end{bmatrix}$ y
 $v_0=(0{,}75,\\,0{,}20,\\,0{,}05)$. Entonces $v_1=v_0\\cdot P$: $P(S)=0{,}75(0{,}2)+0{,}20(0{,}1)+0{,}05(0{,}5)=0{,}195$;
 análogamente $P(N)=0{,}510$ y $P(L)=0{,}295$ → $v_1=(0{,}195,\\,0{,}510,\\,0{,}295)$. En solo 3 pasos
 más la distribución ya casi no depende de $v_0$ (converge al estado estacionario).`,
 aiWhy:`$\\pi\\cdot P=\\pi$ es literalmente la ecuación del PageRank de Google ($\\pi$ es el autovector
 principal de la matriz de transición de la web). Los MDP (Markov Decision Process) extienden esto
 con acciones y recompensas y son la base formal de Q-learning, DQN, PPO, AlphaGo/AlphaZero, y del
 RLHF que afina modelos como ChatGPT/Claude (la "acción" es el siguiente token, la "recompensa"
 viene de preferencias humanas).`,
 question:`Para la matriz $P$ del Modelo del Clima de arriba, calcula la primera componente
 (Soleado) del vector estacionario $\\pi$ que cumple $\\pi\\cdot P=\\pi$ y $\\sum\\pi_i=1$. (cuatro
 decimales, con coma)`,
 type:'numeric', correct:0.2323, decimals:4,
 solution:`Planteando $\\pi=(x,y,z)$: $0{,}2x+0{,}1y+0{,}5z=x$ y $0{,}5x+0{,}6y+0{,}3z=y$, junto con
 $x+y+z=1$. De la primera: $y=8x-5z$. Sustituyendo en la segunda: $-27x+23z=0 \\Rightarrow z=\\tfrac{27}{23}x$,
 y entonces $y=\\tfrac{49}{23}x$. Normalizando: $x\\left(1+\\tfrac{49}{23}+\\tfrac{27}{23}\\right)=1
 \\Rightarrow x=\\tfrac{23}{99}$. Por tanto $\\pi=\\left(\\tfrac{23}{99},\\tfrac{49}{99},\\tfrac{27}{99}\\right)\\approx(0{,}2323,\\,0{,}4949,\\,0{,}2727)$.
 A largo plazo: 23,2% Soleado, 49,5% Nublado, 27,3% Lluvioso — sin importar el clima de hoy.`},

{sesion:'Tensores', name:'Rango, dimensión y convenio de Einstein',
 theory:`El rango (u orden) de un tensor es el número de índices necesarios para referenciar sus
 componentes; la dimensión es el tamaño (número de valores posibles) de cada índice. El convenio de
 Einstein da por sumados implícitamente los índices repetidos en un término: $y_i=A_{ij}x_j$
 significa $y_i=\\sum_j A_{ij}x_j$ (el producto matriz-vector de siempre, sin escribir la suma).`,
 workedExample:`El producto matriz-vector $(Ax)_i=\\sum_j A_{ij}x_j$ se escribe en notación de
 Einstein simplemente como $y_i=A_{ij}x_j$ — el índice $j$ se repite (una vez arriba conceptualmente
 en $x_j$, una vez en $A_{ij}$) y por convenio se entiende sumado, sin necesidad del símbolo
 $\\sum$.`,
 aiWhy:`En TensorFlow/PyTorch/JAX calcular el gradiente (rango bajo respecto a la salida) es
 rápido, pero el Hessiano es mucho más caro — el paper de Laue, Mitterreiter y Giesen (2020,
 resumido en la investigación de Lucas) resuelve esto con un único operador de multiplicación
 tensorial en notación de Einstein que comprime el cálculo del Hessiano, logrando hasta 100.000x de
 mejora en factorización de matrices. La misma idea de "rango y dimensión" de esta sesión es la que
 hace posible ese resultado — y es directamente relevante para el tema de puntos críticos/Hessiana
 de más arriba.`,
 question:`Sea $A\\in\\mathbb{R}^{5\\times5\\times5\\times5}$ un array multidimensional definido por
 $A_{i,j,k,l}=i+j+k+l$, para $i,j,k,l\\in\\{1,2,3,4,5\\}$. Entonces A representa...`,
 type:'mc',
 options:['Un tensor de rango 5 y dimensión 4.',
   'Un tensor de rango 4 y dimensión 5.',
   'Un tensor de rango 5^4 y dimensión 4^5.',
   'Un tensor de rango 4^5 y dimensión 5^4.'],
 correct:1,
 solution:`El array se referencia con 4 índices ($i,j,k,l$) → rango 4. Cada índice recorre
 $\\{1,\\ldots,5\\}$, es decir 5 valores posibles → dimensión 5 (en cada modo). Las opciones c) y d)
 confunden esto con el número total de componentes ($5^4$), que no es ni el rango ni la dimensión
 en sentido tensorial. Respuesta correcta: b).`},

{sesion:'S8–S9 · Límites y continuidad', name:'Límites laterales y continuidad',
 theory:`Los límites laterales $\\lim_{x\\to x_0^-}f(x)$ y $\\lim_{x\\to x_0^+}f(x)$ deben EXISTIR y
 COINCIDIR para que exista $\\lim_{x\\to x_0}f(x)$. $f$ es continua en $x_0$ si además ese límite
 coincide con $f(x_0)$. La derivabilidad implica continuidad, pero no al revés — si $f$ no es
 continua en un punto, tampoco puede ser derivable ahí.`,
 workedExample:`$\\lim_{x\\to2}\\dfrac{x^2-4}{x-2}$: la función no está definida en $x=2$, pero
 factorizando, $\\dfrac{(x-2)(x+2)}{x-2}=x+2$ para $x\\neq2$, así que el límite lateral por ambos
 lados es $4$. El límite EXISTE aunque la función original ni siquiera esté definida en ese punto
 (discontinuidad evitable) — existencia del límite y continuidad son cosas distintas.`,
 aiWhy:`Muchas garantías de convergencia en optimización (incluida la del propio descenso de
 gradiente del tema de Puntos críticos) asumen funciones continuas y diferenciables. Entender
 dónde y por qué falla la continuidad es entender cuándo esas garantías dejan de aplicar.`,
 question:`Sea $f:\\mathbb{R}\\to\\mathbb{R}$ dada por $f(x)=\\sqrt{x^2+1}$ si $x<0$; $f(x)=0$ si $x=0$;
 $f(x)=\\ln(x+1)+e^x$ si $x>0$. Entonces:`,
 type:'mc',
 options:['lím(x→0) f(x) = 0','lím(x→0) f(x) = 1','f es continua en x=0.','f es derivable en x=0.'],
 correct:1,
 solution:`Límite por la izquierda: $\\lim_{x\\to0^-}\\sqrt{x^2+1}=\\sqrt1=1$. Límite por la derecha:
 $\\lim_{x\\to0^+}[\\ln(x+1)+e^x]=\\ln1+e^0=1$. Ambos coinciden en $1$ → el límite existe y vale $1$
 (confirma b, descarta a). Pero $f(0)=0\\neq1$, así que $f$ NO es continua en $0$ (descarta c), y
 como la derivabilidad exige continuidad, tampoco es derivable ahí (descarta d). Respuesta
 correcta: b).`},

{sesion:'S8–S9 · Integrales', name:'Integrales y sustitución',
 theory:`La integral definida $\\int_a^b f(x)\\,dx$ mide el área con signo bajo la curva. El método
 de sustitución cambia $u=g(x)$, $du=g'(x)dx$, y también los límites de integración. Un caso
 especial útil: si $f$ es una función IMPAR ($f(-x)=-f(x)$) y el intervalo es simétrico
 $[-a,a]$, la integral vale $0$ sin necesidad de calcular nada más.`,
 workedExample:`$\\int_{-1}^{1}x^3\\,dx=0$ directamente, porque $x^3$ es una función impar y el
 intervalo $[-1,1]$ es simétrico respecto al origen: el área positiva de un lado cancela
 exactamente el área negativa del otro.`,
 aiWhy:`Normalizar una distribución de probabilidad continua, calcular un valor esperado, o una
 divergencia KL/entropía cruzada en un modelo generativo, es resolver una integral — a menudo con
 el mismo truco de sustitución que aquí.`,
 question:`Encuentra el valor de la siguiente integral: $\\int_0^3 x\\cos(\\pi(1-x^2))\\,dx$`,
 type:'numeric', correct:0, decimals:0,
 solution:`Sustitución $u=1-x^2$, $du=-2x\\,dx$. Cuando $x=0$, $u=1$; cuando $x=3$, $u=-8$.
 $\\int_0^3 x\\cos(\\pi(1-x^2))dx=\\tfrac12\\int_{-8}^{1}\\cos(\\pi u)\\,du=\\tfrac{1}{2\\pi}[\\sin(\\pi u)]_{-8}^{1}
 =\\tfrac{1}{2\\pi}[\\sin(\\pi)-\\sin(-8\\pi)]$. Como $\\sin(n\\pi)=0$ para cualquier entero $n$, el
 resultado es $0$.`},

{sesion:'S1 · Lógica proposicional', name:'Tautología, contradicción y De Morgan',
 theory:`Una proposición es tautológica si es verdadera en TODA interpretación, contradictoria si
 es falsa en TODA interpretación, y contingente si depende de la interpretación. Leyes de De
 Morgan: $\\neg(p\\wedge q)\\equiv\\neg p\\vee\\neg q$ y $\\neg(p\\vee q)\\equiv\\neg p\\wedge\\neg q$.`,
 workedExample:`Si $p\\wedge q$ es contradictorio, entonces $\\neg(p\\wedge q)$ es tautológico. Por De
 Morgan, $\\neg(p\\wedge q)\\equiv\\neg p\\vee\\neg q$ — que esa disyunción sea siempre verdadera equivale
 exactamente a "en toda interpretación, p es falsa o q es falsa".`,
 aiWhy:`Los solvers SAT/SMT que verifican propiedades de sistemas de IA (y los circuitos lógicos de
 la Sesión 2) se basan exactamente en este tipo de equivalencias booleanas para simplificar
 fórmulas antes de buscar una solución.`,
 question:`Sean p, q proposiciones lógicas tales que p∧q es un enunciado contradictorio.
 Entonces:`,
 type:'mc',
 options:['p es falsa o bien q es falsa.','p∨q es contradictorio.','p→q es contingente.','¬p∧¬q es tautológico.'],
 correct:0,
 solution:`$p\\wedge q$ contradictorio $\\Rightarrow \\neg(p\\wedge q)$ tautológico $\\equiv \\neg p\\vee\\neg q$
 (De Morgan) tautológico, que es justo "p es falsa o q es falsa" (a). Contraejemplo para descartar
 el resto: $p=(s\\wedge\\neg s)$ (contradicción), $q=t$. Entonces $p\\vee q=t$ (contingente, no
 contradictorio → descarta b); $p\\to q$ es tautológico por antecedente falso (no contingente →
 descarta c); $\\neg p\\wedge\\neg q=\\neg t$ (contingente, no tautológico → descarta d). Respuesta
 correcta: a).`},

{sesion:'S3 + investigación · Lógica de predicados e inductiva', name:'Cuantificadores y el proceso inductivo (ILP)',
 theory:`Para que un predicado $\\forall y\\,P(x,y)$ se cumpla, debe ser verdadero para TODO $y$ —
 basta UN contraejemplo para refutarlo, pero confirmarlo exige un argumento general (aquí, que una
 expresión cuadrática en $y$ sea siempre $\\geq0$, lo que ocurre si y solo si su discriminante es
 $\\leq0$). En Programación Lógica Inductiva (ILP), "explicar" una hipótesis es cubrir lógicamente
 los ejemplos con el conocimiento previo (resultado fijo, sí/no); "justificarla" es evaluar su
 plausibilidad frente a otras hipótesis rivales (un número que cambia según la evidencia) — son
 procesos distintos, no equivalentes.`,
 workedExample:`Investigación de Lucas sobre ILP (pregunta 1): dos hipótesis para la relación
 "abuelo" pasaron igual la prueba deductiva formal sobre los mismos datos de entrenamiento — la
 deducción sola no bastó para elegir entre ellas. Solo al probarlas contra un caso NUEVO, una de
 las dos falló. "Justificar" una hipótesis en ILP es precisamente ESO: evaluar cuál es más
 plausible frente a otras, no demostrarla formalmente.`,
 aiWhy:`Esta distinción explica por qué ningún modelo de IA entrenado por inducción (de un árbol de
 decisión a una red neuronal) puede "demostrarse" verdadero como un teorema — solo puede
 justificarse como la hipótesis más plausible dados los datos vistos, y puede fallar ante un caso
 nuevo, exactamente como en el experimento de arriba.`,
 question:`Sea $p(x)$ el predicado $\\forall y\\in\\mathbb{R},\\ x\\cdot y\\leq y^2$. Entonces:`,
 type:'mc',
 options:['Se cumple p(-1)','Se cumple p(0)','Se cumple p(1)','El enunciado no se cumple para ningún x ∈ R.'],
 correct:1,
 solution:`Se necesita $y^2-xy\\geq0$ para todo $y$: una parábola hacia arriba en $y$, siempre
 $\\geq0$ si y solo si su discriminante $x^2\\leq0$, es decir $x=0$. Verificación directa: $p(0)$:
 $0\\leq y^2$, cierto siempre. $p(-1)$ falla en $y=-0{,}5$ ($-0{,}25<0$); $p(1)$ falla en $y=0{,}5$
 ($-0{,}25<0$). Respuesta correcta: b).`},

{sesion:'S2 · Álgebra de Boole', name:'Leyes de De Morgan en álgebra de Boole',
 theory:`En toda álgebra de Boole valen las leyes de De Morgan:
 $\\overline{A\\cap B}=\\bar A\\cup\\bar B$ y $\\overline{A\\cup B}=\\bar A\\cap\\bar B$, junto con la
 involución (doble complemento): $\\overline{\\bar X}=X$.`,
 workedExample:`Por el mismo razonamiento pero "al revés": $\\overline{\\bar A\\cup\\bar B}$. Por De
 Morgan, el complemento de una unión es la intersección de los complementos:
 $\\overline{\\bar A\\cup\\bar B}=\\overline{\\bar A}\\cap\\overline{\\bar B}=A\\cap B$ (no $A\\cup B$) — el
 caso dual del que resuelve la pregunta de práctica.`,
 question:`En toda álgebra de Boole B se cumple que A∪B es igual a:`,
 type:'mc',
 options:['complemento de (complemento(A) ∪ complemento(B))','complemento de (A∪B)',
   'complemento de (complemento(A) ∩ complemento(B))','complemento de (A∩B)'],
 correct:2,
 solution:`$\\overline{\\bar A\\cap\\bar B}=\\overline{\\bar A}\\cup\\overline{\\bar B}=A\\cup B$ (De Morgan +
 involución), que es justo lo pedido. La opción a) da $A\\cap B$ (caso dual, no A∪B); b) y d) son
 simplemente los complementos de A∪B y A∩B, que en general no son iguales a A∪B. Respuesta
 correcta: c).`},

{sesion:'S3 · Conjuntos y aplicaciones', name:'Inyectiva, sobreyectiva, biyectiva y el principio del palomar',
 theory:`$f:A\\to B$ es inyectiva si no repite imágenes, sobreyectiva si cubre todo $B$, y biyectiva
 si es ambas (solo posible si $|A|=|B|$ en conjuntos finitos). Principio del palomar: si
 $|A|>|B|$, ninguna función $f:A\\to B$ puede ser inyectiva — no hay suficientes elementos
 distintos en $B$ para asignar una imagen distinta a cada elemento de $A$.`,
 workedExample:`Con 5 palomas y 4 nidos, alguna pareja de palomas necesariamente comparte nido — no
 hay forma de evitarlo. Formalmente: si $|A|=5>|B|=4$, cualquier $f:A\\to B$ envía a al menos dos
 elementos de $A$ al mismo elemento de $B$, es decir, $f$ no puede ser inyectiva.`,
 aiWhy:`El principio del palomar aparece en pruebas de cotas inferiores de complejidad y en
 argumentos de colisión de funciones hash: una función hash no puede ser inyectiva si su espacio
 de salida (p. ej. un embedding comprimido) es más pequeño que su espacio de entrada.`,
 question:`Sean A, B conjuntos tales que |A| = 74, |B| = 47 y f : A → B una aplicación. Entonces:`,
 type:'mc',
 options:['f no puede ser inyectiva.','f no puede ser sobreyectiva.','f puede ser biyectiva.','f puede tener inversa.'],
 correct:0,
 solution:`Como $|A|=74>|B|=47$, por el principio del palomar $f$ necesariamente envía a al menos
 dos elementos distintos de $A$ al mismo valor de $B$: no puede ser inyectiva (a, verdadera). Sí
 puede ser sobreyectiva (descarta b); una biyección exige igual cardinalidad, $74\\neq47$ (descarta
 c); tener inversa exige biyectividad, ya descartada (descarta d). Respuesta correcta: a).`},

{sesion:'S3 · Combinatoria', name:'Combinaciones con repetición',
 theory:`Cuando el orden no importa pero SÍ se permite repetir elementos, se cuenta con
 combinaciones con repetición (o "multiconjuntos"): $CR(n,r)=\\binom{n+r-1}{r}$ — distinto de
 $\\binom{n}{r}$ (combinaciones simples, sin repetición) y de las permutaciones (donde el orden sí
 importa).`,
 workedExample:`Helados de 3 sabores (A, B, C), eligiendo 2 bolas con repetición permitida:
 $\\{AA,AB,AC,BB,BC,CC\\}=6$ combinaciones. La fórmula lo confirma:
 $CR(3,2)=\\binom{3+2-1}{2}=\\binom{4}{2}=6$.`,
 aiWhy:`Contar combinaciones con y sin repetición es la base para calcular el TAMAÑO de un espacio
 de búsqueda o de hipótesis en IA simbólica — la investigación de Lucas sobre ILP (pregunta 7)
 usa exactamente este tipo de conteo para mostrar que el espacio de hipótesis de cláusulas lógicas
 crece de 45 (longitud 1) a más de 16 billones (longitud 8).`,
 question:`Una floristería ofrece 7 variedades de flores. ¿De cuántas maneras diferentes se puede
 formar un ramo de 5 flores, si se pueden escoger varias flores de la misma variedad y el orden no
 importa?`,
 type:'numeric', correct:462, decimals:0,
 solution:`Combinaciones con repetición de 7 elementos tomados de 5 en 5:
 $CR(7,5)=\\binom{7+5-1}{5}=\\binom{11}{5}=\\dfrac{11!}{5!\\cdot6!}=\\dfrac{11\\cdot10\\cdot9\\cdot8\\cdot7}{5\\cdot4\\cdot3\\cdot2\\cdot1}=\\dfrac{55440}{120}=462$.`},

{sesion:'S3 + notebook · Complejidad computacional', name:'Notación O-grande y el coste real de un algoritmo',
 theory:`La notación $\\mathcal{O}$ se queda solo con el término de MAYOR grado y descarta
 constantes multiplicativas: $\\mathcal{O}(9n^{10})$ y $\\mathcal{O}(n^{10})$ son la MISMA cota
 asintótica. $\\mathcal{O}(n!)$ crece muchísimo más rápido que $\\mathcal{O}(n^k)$ para cualquier $k$
 fijo, sin importar cuán grande sea $k$.`,
 workedExample:`Del notebook de ejercicios evaluables de Lucas: calcular el determinante de una
 matriz $12\\times12$ por expansión de Laplace ($\\mathcal{O}(n!)$) tarda 877,02 segundos (casi 15
 minutos); por eliminación de Gauss ($\\mathcal{O}(n^3)$) tarda 0,000152 segundos — una diferencia
 de más de 5 millones de veces, para el MISMO resultado numérico.`,
 aiWhy:`Esa diferencia no es abstracta: separa un algoritmo que escala a producción de uno que solo
 funciona en la diapositiva de clase. Elegir mal la complejidad de un paso de un pipeline de IA (por
 ejemplo, calcular un determinante o un Hessiano de la forma "obvia") puede volver inviable un
 modelo que en teoría era correcto.`,
 question:`Sea un algoritmo cuyo coste computacional asociado es $c(n)=(3n^5-2n+1)^2$. Entonces su
 complejidad computacional es:`,
 type:'mc',
 options:['O(n^5).','O(9n^7)','O(9n^10)','O(n^10)'],
 correct:3,
 solution:`Al desarrollar el cuadrado, el término dominante viene de elevar al cuadrado $3n^5$:
 $(3n^5-2n+1)^2=9n^{10}-12n^6+6n^5+4n^2-4n+1$. El término que domina es $9n^{10}$ → grado 10
 (descarta a y b). Por definición, la notación O-grande descarta constantes multiplicativas:
 $\\mathcal{O}(9n^{10})=\\mathcal{O}(n^{10})$, y la forma estándar se escribe sin la constante.
 Respuesta correcta: d).`},
];


/* ──────────── Modo Maestro Matemáticas (02MIAR, VIU) ────────────
   Tercer temario guiado, con su propio progreso en localStorage. A diferencia
   de Python/AO no reutiliza el panel de ejecución (no hay código que correr):
   oculta .main por completo y muestra #mathPanel a ancho completo con
   teoría+ejemplo resuelto → pregunta real (MC o numérica) → feedback
   inmediato + solución paso a paso → autoexplicación opcional (colapsada) →
   siguiente tema. Metodología: ver plan piped-puzzling-giraffe.md §0/§2. */
const MASTER_MATH_KEY='pyvizMasterMathProgress';
let _mathOn=false, _mathPos=0, _mathDone=new Set(), _mathAnswered=false, _mathQuizShuffledCorrect=null;

function _loadMathProgress(){
  try{
    const raw=localStorage.getItem(MASTER_MATH_KEY);
    if(raw){ const d=JSON.parse(raw); _mathDone=new Set(d.done||[]); }
  }catch(e){ _mathDone=new Set(); }
}
function _saveMathProgress(){
  try{ localStorage.setItem(MASTER_MATH_KEY, JSON.stringify({done:[..._mathDone]})); }catch(e){}
}
function _mathFirstPending(){
  for(let i=0;i<EX_MATH.length;i++) if(!_mathDone.has(i)) return i;
  return EX_MATH.length-1;
}
function toggleMasterMath(){
  if(_mathOn){ exitMasterMath(); return; }
  if(_masterOn) exitMasterMode();
  if(_aoOn) exitMasterAo();
  if(_raOn) exitMasterRa();
  if(_asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn) exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn) exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn) exitMasterRf();
  if(_reviewOn) exitReviewMode();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  _mathOn=true;
  _loadMathProgress();
  document.querySelector('.main').style.display='none';
  document.getElementById('mathPanel').style.display='flex';
  document.getElementById('masterMathBar').style.display='flex';
  const b=document.getElementById('bMasterMath');
  if(b){ b.textContent='📐 Modo Maestro Matemáticas (activo)'; b.classList.add('btn-looping'); }
  _mathGoTo(_mathFirstPending());
}
function exitMasterMath(){
  _mathOn=false;
  document.getElementById('masterMathBar').style.display='none';
  document.getElementById('masterMathChecklist').style.display='none';
  document.getElementById('mathPanel').style.display='none';
  document.querySelector('.main').style.display='flex';
  const b=document.getElementById('bMasterMath');
  if(b){ b.textContent='📐 Modo Maestro Matemáticas'; b.classList.remove('btn-looping'); }
}
/* KaTeX auto-render sobre el panel entero tras cada repintado; throwOnError:false
   para que un typo de LaTeX no rompa el resto del panel, solo esa fórmula. */
function _mathRenderKatex(){
  if(window.renderMathInElement){
    renderMathInElement(document.getElementById('mathPanel'), {
      delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
      throwOnError:false
    });
  }
}
function _mathGoTo(idx){
  _mathPos=Math.max(0, Math.min(EX_MATH.length-1, idx));
  const t=EX_MATH[_mathPos];
  _mathAnswered=false;
  document.getElementById('mathSesionBadge').textContent=t.sesion;
  document.getElementById('mathTheoryBody').innerHTML=t.theory.replace(/\n/g,'<br>');
  document.getElementById('mathWorkedBody').innerHTML=t.workedExample.replace(/\n/g,'<br>');
  document.getElementById('mathQuestionBody').innerHTML=t.question.replace(/\n/g,'<br>');
  const optWrap=document.getElementById('mathOptions');
  const numWrap=document.getElementById('mathNumericWrap');
  if(t.type==='mc'){
    optWrap.style.display='grid';
    numWrap.style.display='none';
    const shuffled=_shuffleMcOptions(t);
    _mathQuizShuffledCorrect=shuffled.correct;
    optWrap.innerHTML=shuffled.options.map((o,i)=>
      `<button class="math-option" onclick="_mathCheckAnswer(${i})">${String.fromCharCode(97+i)}) ${o}</button>`).join('');
  } else {
    optWrap.style.display='none';
    numWrap.style.display='flex';
    const inp=document.getElementById('mathNumericInput');
    inp.value=''; inp.disabled=false;
    _mathQuizShuffledCorrect=null;
  }
  document.getElementById('mathFeedback').style.display='none';
  document.getElementById('mathAiWhyWrap').style.display='none';
  document.getElementById('mathSolutionBtn').style.display='none';
  const solBody=document.getElementById('mathSolutionBody');
  solBody.style.display='none'; solBody.innerHTML='';
  document.getElementById('mathNextBtn').style.display='none';
  document.getElementById('selfExplainInner').style.display='none';
  document.getElementById('selfExplainText').value='';
  document.getElementById('mathSelfExplain').style.display='none';
  _mathRenderBar();
  _mathRenderKatex();
  document.getElementById('mathPanel').scrollTop=0;
}
/* Núcleo del flujo (practice testing + feedback inmediato, ver plan §0): se
   llama con el índice elegido (MC) o sin argumento (numérico, lee el input).
   Reintentar tras fallar (cambiado 2026-08-09, a petición del usuario): solo
   se bloquea la pregunta al ACERTAR — un fallo deja el input/los botones
   habilitados para corregir un error o un typo e intentarlo de nuevo, en
   vez de quedar bloqueado hasta el siguiente tema. (Nota: esto relaja la
   idea original de "no ir probando hasta acertar" del testing effect —
   cada intento se sigue registrando en _recordAttempt, así que Leitner/
   fails-badge reflejan igualmente cuántos fallos hicieron falta.) */
function _mathCheckAnswer(selectedIdx){
  if(_mathAnswered) return;
  const t=EX_MATH[_mathPos];
  let ok=false;
  if(t.type==='mc'){
    ok = selectedIdx===_mathQuizShuffledCorrect;
    document.querySelectorAll('#mathOptions .math-option').forEach((btn,i)=>{
      btn.classList.remove('math-option-correct','math-option-wrong');
      if(ok){
        btn.disabled=true;
        if(i===_mathQuizShuffledCorrect) btn.classList.add('math-option-correct');
      } else if(i===selectedIdx){
        btn.classList.add('math-option-wrong');
      }
    });
  } else {
    const inp=document.getElementById('mathNumericInput');
    const val=parseFloat(inp.value.trim().replace(',','.'));
    const dec=t.decimals||0;
    const p=Math.pow(10,dec);
    ok = !isNaN(val) && Math.round(val*p)===Math.round(t.correct*p);
    inp.disabled=ok;
  }
  if(ok) _mathAnswered=true;
  _mathDone.add(_mathPos);
  _saveMathProgress();
  _recordAttempt('math', _mathPos, ok);
  const fb=document.getElementById('mathFeedback');
  fb.style.display='block';
  fb.className='math-feedback '+(ok?'math-feedback-ok':'math-feedback-bad');
  fb.textContent = ok ? '✅ ¡Correcto!' : '❌ No es correcto — puedes intentarlo de nuevo, o revisar la solución paso a paso.';
  if(t.aiWhy){
    document.getElementById('mathAiWhyBody').innerHTML=t.aiWhy.replace(/\n/g,'<br>');
    document.getElementById('mathAiWhyWrap').style.display='block';
  }
  document.getElementById('mathSolutionBtn').style.display='inline-block';
  document.getElementById('mathSelfExplain').style.display='block';
  const nextBtn=document.getElementById('mathNextBtn');
  nextBtn.style.display='inline-block';
  nextBtn.textContent = (_mathPos>=EX_MATH.length-1) ? '✅ Entendido, terminar' : 'Siguiente tema ▶';
  _mathRenderBar();
  _mathRenderKatex();
}
function _mathShowSolution(){
  const t=EX_MATH[_mathPos];
  const el=document.getElementById('mathSolutionBody');
  el.innerHTML=t.solution.replace(/\n/g,'<br>');
  el.style.display='block';
  _mathRenderKatex();
}
/* Autoexplicación (Hodds 2014, rebajada tras Dunlosky 2013 a un único prompt
   opcional y colapsado — ver plan piped-puzzling-giraffe.md §0/§2): un mismo
   toggle genérico, reutilizado por los 3 Modos Maestro (Py/AO/Matemáticas)
   en vez de una función distinta por modo. */
function _toggleSelfExplain(mode){
  const ids={py:'selfExplainPy', ao:'selfExplainAo', math:'selfExplainInner', ra:'selfExplainRa', as:'selfExplainAs',
    ns:'selfExplainNs', rn:'selfExplainRn', rf:'selfExplainRf'};
  const el=document.getElementById(ids[mode]);
  if(!el) return;
  el.style.display = el.style.display==='none' ? 'block' : 'none';
}
/* Guardado de "Autoexplícate" (AO/RA/AS solamente — Py no tiene `theory`
   por tema y Matemáticas queda fuera del alcance, ver conversación): el
   alumno escribe su explicación, dudas o sugerencias de mejora sobre el
   tema, y con "💾 Guardar nota" queda en SQLite (notes_store.py,
   student_notes.db) para poder revisarlo más adelante — sin ningún
   veredicto automático de la IA (se probó y se descartó a pedido
   explícito del usuario: quería la caja de texto de siempre, sin la
   llamada a Claude). */
function _selfExplainTopicData(mode){
  if(mode==='ao') return {name:EX_AO[_aoPos].name, theory:EX_AO[_aoPos].theory||'', code:EX_AO[_aoPos].code};
  if(mode==='ra') return {name:EX_RA[_raPos].name, theory:EX_RA[_raPos].theory||'', code:EX_RA[_raPos].code};
  if(mode==='as') return {name:EX_AS[_asPos].name, theory:EX_AS[_asPos].theory||'', code:EX_AS[_asPos].code};
  if(mode==='ns') return {name:EX_NS[_nsPos].name, theory:EX_NS[_nsPos].theory||'', code:EX_NS[_nsPos].code};
  if(mode==='rn') return {name:EX_RN[_rnPos].name, theory:EX_RN[_rnPos].theory||'', code:EX_RN[_rnPos].code};
  if(mode==='rf') return {name:EX_RF[_rfPos].name, theory:EX_RF[_rfPos].theory||'', code:EX_RF[_rfPos].code};
  return null;
}
function _selfExplainSaveNote(mode){
  const ids={ao:['selfExplainTextAo','selfExplainSavedAo'], ra:['selfExplainTextRa','selfExplainSavedRa'],
    as:['selfExplainTextAs','selfExplainSavedAs'], ns:['selfExplainTextNs','selfExplainSavedNs'],
    rn:['selfExplainTextRn','selfExplainSavedRn'], rf:['selfExplainTextRf','selfExplainSavedRf']};
  const pair=ids[mode];
  if(!pair) return;
  const ta=document.getElementById(pair[0]);
  const savedMsg=document.getElementById(pair[1]);
  const text=(ta.value||'').trim();
  if(!text){ if(savedMsg){ savedMsg.style.display='inline'; savedMsg.textContent='Escribe algo antes de guardar.'; } return; }
  const topic=_selfExplainTopicData(mode);
  if(!topic) return;
  const posMap={ao:_aoPos, ra:_raPos, as:_asPos, ns:_nsPos, rn:_rnPos, rf:_rfPos};
  fetch('/save_note',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({mode, topic_idx:posMap[mode], topic_name:topic.name, text, feedback:null})})
    .then(r=>r.json()).then(d=>{
      if(savedMsg){
        savedMsg.style.display='inline';
        savedMsg.textContent = (d && d.ok) ? '💾 Guardado' : '❌ No se pudo guardar';
        setTimeout(()=>{ if(savedMsg) savedMsg.style.display='none'; }, 2500);
      }
    }).catch(()=>{ if(savedMsg){ savedMsg.style.display='inline'; savedMsg.textContent='❌ No se pudo guardar'; } });
}
/* Peldaño "Transferencia" de la Escalera de Dominio (nivel 7 del plan de
   aprendizaje personal del usuario: "resolver un problema nuevo donde no
   aparece explícitamente el nombre del concepto" — la prueba real de
   dominio según su propio punto 24: "la mejor prueba es la capacidad de
   TRANSFERIR"). Reutiliza el mismo /save_note que _selfExplainSaveNote,
   con kind:'transfer' para poder distinguirlo después (ver notes_store.py)
   — mismo textarea propio, sin veredicto de IA, mismo motivo que la nota
   normal (el usuario ya rechazó ese enfoque una vez, ver
   feedback-modo-maestro-explicaciones-simples / conversación de notas). */
function _transferSaveQuestion(mode){
  const ids={ao:['transferTextAo','transferSavedAo'], ra:['transferTextRa','transferSavedRa'],
    as:['transferTextAs','transferSavedAs'], ns:['transferTextNs','transferSavedNs'],
    rn:['transferTextRn','transferSavedRn'], rf:['transferTextRf','transferSavedRf']};
  const pair=ids[mode];
  if(!pair) return;
  const ta=document.getElementById(pair[0]);
  const savedMsg=document.getElementById(pair[1]);
  const text=(ta.value||'').trim();
  if(!text){ if(savedMsg){ savedMsg.style.display='inline'; savedMsg.textContent='Escribe tu problema nuevo antes de guardar.'; } return; }
  const topic=_selfExplainTopicData(mode);
  if(!topic) return;
  const posMap={ao:_aoPos, ra:_raPos, as:_asPos, ns:_nsPos, rn:_rnPos, rf:_rfPos};
  fetch('/save_note',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({mode, topic_idx:posMap[mode], topic_name:topic.name, text, feedback:null, kind:'transfer'})})
    .then(r=>r.json()).then(d=>{
      if(savedMsg){
        savedMsg.style.display='inline';
        savedMsg.textContent = (d && d.ok) ? '🎯 Guardado — buen trabajo transfiriendo el concepto' : '❌ No se pudo guardar';
        setTimeout(()=>{ if(savedMsg) savedMsg.style.display='none'; }, 3000);
      }
    }).catch(()=>{ if(savedMsg){ savedMsg.style.display='inline'; savedMsg.textContent='❌ No se pudo guardar'; } });
}
function mathPrev(){ if(_mathPos>0) _mathGoTo(_mathPos-1); }
function _mathRestart(){ _mathGoTo(0); }
function mathNext(){
  if(_mathPos>=EX_MATH.length-1){
    _mathRenderBar();
    setSt('🎉 ¡Completaste el temario de Matemáticas para IA! Repasa cualquier tema desde ☰ Temario cuando quieras.');
    return;
  }
  _mathGoTo(_mathPos+1);
}
function _mathRenderBar(){
  const t=EX_MATH[_mathPos];
  const pct=Math.round((_mathDone.size/EX_MATH.length)*100);
  document.getElementById('masterMathTitle').textContent=
    `📐 Tema ${_mathPos+1}/${EX_MATH.length} · ${t.name}`;
  document.getElementById('masterMathFill').style.width=pct+'%';
  document.getElementById('masterMathPct').textContent=pct+'% del temario dominado';
  document.getElementById('mPrevMath').disabled=(_mathPos<=0);
  if(document.getElementById('masterMathChecklist').style.display!=='none') _mathRenderChecklist();
}
function _mathToggleChecklist(){
  const cl=document.getElementById('masterMathChecklist');
  const show=cl.style.display==='none';
  cl.style.display=show?'block':'none';
  if(show) _mathRenderChecklist();
}
function _mathRenderChecklist(){
  const cl=document.getElementById('masterMathChecklist');
  cl.innerHTML=EX_MATH.map((t,i)=>{
    const done=_mathDone.has(i);
    const cur=i===_mathPos;
    return `<div class="master-item${done?' master-item-done':''}${cur?' master-item-current':''}" onclick="_mathGoTo(${i})">`+
      `<span class="master-item-chk">${done?'✓':(i+1)}</span><span class="master-item-name">${esc(t.name)}</span>${_failsBadge('math',i)}</div>`;
  }).join('');
}


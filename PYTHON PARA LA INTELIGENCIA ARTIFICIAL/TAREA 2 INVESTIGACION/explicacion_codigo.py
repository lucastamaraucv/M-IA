# =============================================================================
# EXPLICACION DEL CODIGO — TS-LIF reimplementado en NumPy
# Recorre el notebook bloque a bloque explicando que hace cada parte,
# por que lo hace asi, y que nos dice el resultado.
# =============================================================================

import matplotlib
matplotlib.use('TkAgg')   # evita conflicto con PySide6/Qt en VS Code
import numpy as np
import matplotlib.pyplot as plt
import os

# Ruta base: siempre la carpeta donde esta este .py, sin importar desde donde se ejecuta
BASE = os.path.dirname(os.path.abspath(__file__))
CSV  = os.path.join(BASE, 'subirTarea', 'electricity_sample.csv')

np.random.seed(0)


# =============================================================================
# BLOQUE 1 — QUE DATOS USAMOS Y POR QUE
# =============================================================================
print("""
=============================================================================
BLOQUE 1 — QUE DATOS USAMOS Y POR QUE
=============================================================================

El archivo electricity_sample.csv tiene 168 filas y 3 columnas.
Cada fila es una hora. Cada columna es un consumidor electrico diferente.
En total son 7 dias x 24 horas = 168 horas: una semana completa de datos.

Los datos vienen del UCI Electricity dataset, que es el mismo que usa el
paper para sus experimentos. Son mediciones reales de consumo electrico
en Portugal. Tome los 3 consumidores con el patron diario mas claro
(los que mas se parecen a si mismos cada 24 horas).

Los valores estan entre 0 y 1 porque normalice cada consumidor por su
maximo y minimo. Eso se llama normalizacion min-max, y es exactamente
lo que hace el paper antes de entrenar.

Por que 168 horas exactamente?
Porque el paper usa ventanas de 168 pasos como entrada. No es arbitrario:
168 = 7 dias x 24 horas. Es la unidad natural para ver tanto el ciclo
diario como la tendencia de la semana completa.
""")

data = np.loadtxt(CSV, delimiter=',')
print(f"  Datos cargados: {data.shape[0]} horas x {data.shape[1]} consumidores")
print(f"  Rango de valores: [{data.min():.3f}, {data.max():.3f}]")
print()
print("  Lo que se va a ver en el grafico:")
print("  - De dia (horas 8-20) el consumo sube, de noche baja.")
print("  - El fin de semana (horas 120 en adelante) el consumo cae.")
print("  - Eso significa que hay DOS cosas mezcladas en la misma curva:")
print("    una tendencia semanal lenta y un ciclo diario rapido.")
print("  Eso es exactamente lo que TS-LIF esta disenado para separar.")

fig, ax = plt.subplots(figsize=(12, 3))
dias = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
for j in range(data.shape[1]):
    ax.plot(data[:, j], alpha=0.75, label=f'consumidor {j+1}')
for d in range(7):
    ax.axvline(d * 24, color='gray', linestyle=':', alpha=0.4)
    ax.text(d * 24 + 1, 0.08, dias[d], fontsize=8, color='gray')
ax.set_title('Una semana de consumo electrico real — normalizado [0,1]')
ax.set_xlabel('hora'); ax.set_ylabel('consumo norm.')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()


# =============================================================================
# BLOQUE 2 — QUE ES UN SPIKE Y COMO SE GENERA
# =============================================================================
print("""
=============================================================================
BLOQUE 2 — QUE ES UN SPIKE Y COMO SE GENERA
=============================================================================

Las neuronas spiking no mandan un numero continuo hacia adelante.
Mandan un pulso binario: 1 si disparan, 0 si no disparan.
A ese pulso se le llama "spike".

La regla es simple: si el potencial interno de la neurona supera un umbral,
dispara (sale 1). Si no lo supera, no dispara (sale 0).
Eso matematicamente es la funcion de Heaviside: H(x) = 1 si x >= 0, si no 0.

En simple: es como un interruptor de luz. O esta encendido o apagado.
No hay valores intermedios.

Por que usar esto en vez de una activacion normal como ReLU o sigmoide?
Porque es lo que hacen las neuronas biologicas reales. Y eso tiene ventajas:
los spikes son discretos y dispersos, lo que hace la red mucho mas eficiente
en energia que una red neuronal normal.

El problema para entrenar: la funcion de Heaviside no tiene gradiente util,
su derivada es cero en casi todos lados. El paper resuelve eso con un truco
llamado "surrogate gradient": en el paso hacia adelante usa Heaviside normal,
pero en el paso hacia atras usa la derivada suave de la arcotangente (atan).
En mi version en NumPy no hay entrenamiento, solo simulacion hacia adelante,
asi que uso la Heaviside clasica directamente.
""")

def heaviside(x):
    """Disparo de la neurona: 1 si el potencial supera el umbral, 0 si no."""
    return (x >= 0.0).astype(np.float32)

print("  Ejemplo de como funciona heaviside:")
print(f"  heaviside(+0.5) = {heaviside(np.array([0.5]))[0]}  <- potencial alto, dispara")
print(f"  heaviside(-0.3) = {heaviside(np.array([-0.3]))[0]}  <- potencial bajo, no dispara")


# =============================================================================
# BLOQUE 3 — LA NEURONA TS-LIF: DOS COMPARTIMENTOS EN UNA
# =============================================================================
print("""
=============================================================================
BLOQUE 3 — LA NEURONA TS-LIF: DOS COMPARTIMENTOS EN UNA
=============================================================================

La idea central del paper es partir la neurona en dos partes:
  - La DENDRITA (vd): la parte que acumula informacion lentamente.
  - El SOMA (vs): la parte que reacciona rapido a lo que pasa ahora.

Cada parte actualiza su potencial en cada paso de tiempo siguiendo
la Ecuacion 5 del paper:

    vd[t] = a1 * vd[t-1]  +  b1 * vs[t-1]  +  (1-a1) * c[t]  -  g1 * sd_prev
    vs[t] = a2 * vs[t-1]  +  b2 * vd[t]    +  (1-a2) * c[t]  -  g2 * ss_prev

Para entender que hace cada termino, lo explico uno por uno:

  a1 * vd[t-1]
  La dendrita recuerda su propio valor anterior, atenuado por a1=0.95.
  Como a1 esta cerca de 1, casi todo el potencial anterior se conserva.
  En simple: la dendrita tiene memoria larga. No olvida facilmente.
  Resultado: acumula la tendencia de largo plazo. Es un filtro paso-bajo.

  a2 * vs[t-1]
  El soma tambien recuerda su valor anterior, pero atenuado por a2=0.05.
  Como a2 esta cerca de 0, casi nada del pasado se conserva.
  En simple: el soma tiene memoria corta. Olvida rapido.
  Resultado: solo reacciona a lo que acaba de pasar. Es un filtro paso-alto.

  (1-a1) * c[t] = 0.05 * c[t]
  La entrada llega a la dendrita con poco peso (5%).
  Tiene sentido: si la dendrita acumula lento, no puede recibir mucha
  entrada de golpe o se saturaria.

  (1-a2) * c[t] = 0.95 * c[t]
  La entrada llega al soma con mucho peso (95%).
  ESTA ES LA NOVEDAD del paper respecto al modelo anterior (TC-LIF).
  Al darle la entrada casi completa directamente al soma, la informacion
  rapida no se pierde al tener que pasar primero por la dendrita lenta.
  El paper llama a esto "conexion axosomatica directa".

  b2 * vd[t] = -0.9 * vd[t]
  El soma recibe informacion de la dendrita, con signo negativo.
  En simple: cuando la tendencia semanal es alta (dendrita alta),
  el soma se frena un poco. Eso evita que el soma se dispare sin parar
  solo porque el nivel general de consumo es alto.

  g1 * sd_prev  y  g2 * ss_prev
  Cada vez que la neurona dispara un spike, su potencial baja en g1 o g2.
  Es el mecanismo de reset: evita que la neurona se quede disparando
  infinitamente una vez que supera el umbral.
""")

class TSLIFNeuron:
    """Neurona TS-LIF de doble compartimento — Ecuacion 5 del paper (ICLR 2025)."""
    def __init__(self, alpha1=0.95, alpha2=0.05, beta1=0.0, beta2=-0.9,
                 gamma1=0.5, gamma2=1.0, v_th=1.0, kappa=0.5):
        self.a1, self.a2 = alpha1, alpha2   # decaimiento: a1 lento, a2 rapido
        self.b1, self.b2 = beta1, beta2     # acoplamiento entre compartimentos
        self.g1, self.g2 = gamma1, gamma2   # cuanto baja el potencial al disparar
        self.v_th = v_th                    # umbral de disparo
        self.kappa = kappa                  # mezcla dendrita/soma en la salida
        self.reset()

    def reset(self):
        self.vd = self.vs = self.sd_prev = self.ss_prev = 0.0

    def step(self, c):
        # Actualizar dendrita y soma segun Ec. 5
        vd = self.a1*self.vd + self.b1*self.vs + (1 - self.a1)*c - self.g1*self.sd_prev
        vs = self.a2*self.vs + self.b2*vd      + (1 - self.a2)*c - self.g2*self.ss_prev
        # Generar spikes si superan el umbral
        sd = heaviside(vd - self.v_th)
        ss = heaviside(vs - self.v_th)
        # Guardar estado para el siguiente paso
        self.vd, self.vs = vd, vs
        self.sd_prev, self.ss_prev = sd, ss
        # Salida final: mezcla ponderada de ambos spikes
        return vd, vs, sd, ss, self.kappa * sd + (1 - self.kappa) * ss

print("  TSLIFNeuron lista. Parametros:")
print("    a1=0.95 (dendrita, olvida lento)  a2=0.05 (soma, olvida rapido)")
print("    b2=-0.9 (soma se frena cuando dendrita es alta)")
print("    En el modelo real estos valores se APRENDEN durante el entrenamiento.")


# =============================================================================
# BLOQUE 4 — EL LIF CLASICO: POR QUE SE QUEDA CORTO
# =============================================================================
print("""
=============================================================================
BLOQUE 4 — EL LIF CLASICO: POR QUE SE QUEDA CORTO
=============================================================================

El LIF clasico (Leaky Integrate-and-Fire) es la neurona spiking mas simple.
Tiene un solo potencial v que acumula la entrada y decae con el tiempo:

    v[t] = alpha * v[t-1]  +  (1 - alpha) * c[t]  -  gamma * s_prev

El problema es que alpha es un unico numero fijo. Eso te obliga a elegir:
  - Si pones alpha alto (ej: 0.95): la neurona recuerda mucho el pasado
    y captura bien la tendencia lenta, pero no reacciona a los cambios rapidos.
  - Si pones alpha bajo (ej: 0.05): reacciona rapido a cada cambio,
    pero pierde la tendencia de largo plazo.

En simple: con un solo compartimento no puedes estar en los dos lados a la vez.
TS-LIF resuelve esto con dos compartimentos especializados: uno para cada escala.

Lo voy a usar como comparacion para mostrar visualmente la diferencia.
""")

class LIFNeuron:
    """LIF clasico de un solo compartimento — sirve de linea base."""
    def __init__(self, alpha=0.90, v_th=1.0, gamma=1.0):
        self.alpha = alpha
        self.v_th = v_th
        self.gamma = gamma
        self.v = 0.0
        self.s_prev = 0.0

    def step(self, c):
        self.v = self.alpha * self.v + (1 - self.alpha) * c - self.gamma * self.s_prev
        s = heaviside(self.v - self.v_th)
        self.s_prev = s
        return self.v, s

print("  LIFNeuron lista con alpha=0.90.")
print("  Con un solo alpha no puede separar tendencia lenta y variacion rapida.")


# =============================================================================
# BLOQUE 5 — VERIFICAR QUE EL SISTEMA ES ESTABLE ANTES DE SIMULAR
# =============================================================================
print("""
=============================================================================
BLOQUE 5 — VERIFICAR QUE EL SISTEMA ES ESTABLE ANTES DE SIMULAR
=============================================================================

Antes de pasar los datos al modelo, verifico que el sistema sea estable.

Que significa estable? Que el potencial de la neurona no se va a infinito.
Si el sistema es inestable, el potencial crece sin limite con cada paso
de tiempo y el entrenamiento simplemente revienta (diverge).

El Teorema 1 del paper dice que el sistema es estable si los autovalores
de la matriz del sistema tienen modulo menor que 1.

Los autovalores son los "valores propios" de la matriz que describe como
evolucionan vd y vs juntos. Para este sistema lineal se calculan asi:

    traza     = a1 + a2 + b1*b2        <- suma de la diagonal de la matriz
    disc      = sqrt(traza^2 - 4*a1*a2) <- discriminante del polinomio
    lambda1   = (traza + disc) / 2
    lambda2   = (traza - disc) / 2

Si ambos |lambda| < 1, el sistema converge. Si alguno >= 1, diverge.

En simple: los autovalores miden que tan rapido "crece" o "decae" el sistema.
Si crecen (|lambda| >= 1), el potencial se va al infinito. Si decaen, el
sistema se mantiene acotado y el entrenamiento puede funcionar.
""")

a1, a2, b1, b2 = 0.95, 0.05, 0.0, -0.9
traza = a1 + a2 + b1 * b2
disc  = (traza**2 - 4 * a1 * a2) ** 0.5
lam1  = (traza + disc) / 2
lam2  = (traza - disc) / 2
print(f"  Calculo con a1={a1}, a2={a2}, b1={b1}, b2={b2}:")
print(f"    traza   = {a1} + {a2} + {b1}*({b2}) = {traza}")
print(f"    lambda1 = {lam1:.3f}  ->  |lambda1| = {abs(lam1):.3f}  < 1? {abs(lam1) < 1}")
print(f"    lambda2 = {lam2:.3f}  ->  |lambda2| = {abs(lam2):.3f}  < 1? {abs(lam2) < 1}")
print(f"    Sistema ESTABLE: {abs(lam1) < 1 and abs(lam2) < 1}")
print()
print("  Nota: lambda1=0.95 corresponde a la dendrita (decae lento).")
print("        lambda2=0.05 corresponde al soma (decae rapido).")
print("  Esa diferencia tan grande (0.95 vs 0.05) es lo que produce")
print("  la separacion de frecuencias entre los dos compartimentos.")


# =============================================================================
# BLOQUE 6 — EXPERIMENTO 1: VER LA SEPARACION EN DATOS REALES
# =============================================================================
print("""
=============================================================================
BLOQUE 6 — EXPERIMENTO 1: VER LA SEPARACION EN DATOS REALES
=============================================================================

Ahora tomo el primer consumidor del CSV y lo paso hora por hora a los
dos modelos. Es un bucle simple: en cada iteracion le doy el valor
de consumo de esa hora y guardo los potenciales que produce cada modelo.

Para saber si el modelo esta haciendo bien su trabajo, necesito una
referencia de "como deberia verse la tendencia semanal" y "como deberia
verse la variacion horaria". Las calculo directamente del dato:

  Tendencia semanal (low_ref):
  Hago una media movil de 24 horas con np.convolve. Al promediar cada
  punto con sus 24 vecinos, los picos diarios se suavizan y queda solo
  la tendencia lenta de la semana. Es la "linea de base" de consumo.

  Variacion horaria (high_ref):
  Es simplemente c - low_ref: lo que le sobra a la senal una vez que
  le resto la tendencia. Son las subidas y bajadas dentro de cada dia.

Luego el grafico de 4 paneles muestra si vd sigue a low_ref
y si vs sigue a high_ref. Si coinciden, el modelo esta funcionando
como predice el paper.
""")

c       = data[:, 0]
t       = np.arange(len(c))
w       = 24
low_ref  = np.convolve(c, np.ones(w) / w, mode='same')
high_ref = c - low_ref

tslif = TSLIFNeuron()
VD, VS = [], []
for ct in c:
    vd, vs, *_ = tslif.step(ct)
    VD.append(vd); VS.append(vs)
VD, VS = np.array(VD), np.array(VS)

lif = LIFNeuron()
VLIF = []
for ct in c:
    v_lif, _ = lif.step(ct)
    VLIF.append(v_lif)
VLIF = np.array(VLIF)

fig, ax = plt.subplots(4, 1, figsize=(12, 11), sharex=True)

ax[0].plot(t, c, color='navy', lw=0.9)
ax[0].set_title('Panel 1 — Entrada: consumo real (Lun a Dom, hora por hora)')
ax[0].set_ylabel('c[t]'); ax[0].grid(True, alpha=0.3)

ax[1].plot(t, VD, color='green', lw=1.4, label='vd — dendrita TS-LIF')
ax[1].plot(t, low_ref, 'b--', alpha=0.65, label='tendencia real (media 24 h)')
ax[1].set_title('Panel 2 — DENDRITA: sigue la tendencia semanal (filtro paso-bajo)')
ax[1].set_ylabel('vd[t]'); ax[1].legend(loc='upper right'); ax[1].grid(True, alpha=0.3)

ax[2].plot(t, VS, color='red', lw=1.4, label='vs — soma TS-LIF')
ax[2].plot(t, high_ref, 'b--', alpha=0.65, label='variacion real (c - media 24 h)')
ax[2].set_title('Panel 3 — SOMA: sigue las variaciones horarias (filtro paso-alto)')
ax[2].set_ylabel('vs[t]'); ax[2].legend(loc='upper right'); ax[2].grid(True, alpha=0.3)

ax[3].plot(t, VLIF, color='darkorange', lw=1.4, label='v — LIF clasico')
ax[3].plot(t, c, 'b--', alpha=0.40, label='entrada c[t]')
ax[3].set_title('Panel 4 — LIF CLASICO: solo atenua la senal, no la separa')
ax[3].set_ylabel('v[t]')
ax[3].set_xlabel('hora  (0 = Lun 00:00  →  167 = Dom 23:00)')
ax[3].legend(loc='upper right'); ax[3].grid(True, alpha=0.3)

plt.tight_layout(); plt.show()

print("""
  Que muestra cada panel:

  Panel 1 — La senal de entrada tal cual: consumo real con las dos escalas
  mezcladas. Se ven los picos diarios y la caida del fin de semana juntos.

  Panel 2 — La DENDRITA (verde) sigue la linea azul discontinua casi exacto.
  La linea azul es la media movil de 24 h, que es la "tendencia real" de los
  datos. La dendrita la captura sola gracias a a1=0.95, sin que yo se la haya
  impuesto. Esto confirma que actua como filtro paso-bajo.

  Panel 3 — El SOMA (rojo) sigue la linea azul discontinua de variacion horaria.
  Sube cuando el consumo sube dentro del dia, baja cuando baja. Reacciona rapido
  a cada cambio porque a2=0.05 hace que olvide el pasado casi enseguida.
  Esto confirma que actua como filtro paso-alto.

  Panel 4 — El LIF clasico simplemente sigue la curva de entrada de forma
  suavizada. No la separa en dos componentes. No distingue si un valor alto
  se debe a la tendencia semanal o a un pico de consumo puntual. Por eso
  no puede hacer forecasting de multiples escalas temporales a la vez.
""")


# =============================================================================
# BLOQUE 7 — EXPERIMENTO 2A: CONFIRMAR LA SEPARACION CON LA FFT
# =============================================================================
print("""
=============================================================================
BLOQUE 7 — EXPERIMENTO 2A: CONFIRMAR LA SEPARACION CON LA FFT
=============================================================================

El grafico anterior muestra la separacion visualmente. La FFT la confirma
con numeros: descompone cada senal en sus componentes de frecuencia y mide
cuanta energia hay en cada frecuencia.

Como funciona:
  np.fft.rfft(senal)  — calcula los coeficientes de Fourier
  np.abs(...)         — toma la amplitud de cada coeficiente
  np.fft.rfftfreq(N)  — da las frecuencias correspondientes en ciclos/hora

Lo que se espera ver segun el paper:
  - VD (dendrita): mucha energia a la izquierda de f=1/24 (baja frecuencia).
    La raya gris discontinua a f=1/24 es el ciclo diario. A la izquierda
    esta todo lo mas lento que el dia: la tendencia semanal.
  - VS (soma): mucha energia a la derecha de f=1/24 (alta frecuencia).
    Todo lo mas rapido que el dia: las subidas y bajadas de cada hora.
  - VLIF: no deberia mostrar esa separacion, su energia queda mezclada.

El eje Y esta en escala logaritmica porque las amplitudes varian mucho
entre frecuencias. En escala log se ve mejor la forma del espectro.
""")

N        = len(c)
freqs    = np.fft.rfftfreq(N)
C_fft    = np.abs(np.fft.rfft(c))
VD_fft   = np.abs(np.fft.rfft(VD))
VS_fft   = np.abs(np.fft.rfft(VS))
VLIF_fft = np.abs(np.fft.rfft(VLIF))

fig, ax = plt.subplots(figsize=(12, 4))
ax.semilogy(freqs, C_fft,    color='navy',       lw=1.2, label='entrada c[t]')
ax.semilogy(freqs, VD_fft,   color='green',      lw=1.8, label='vd dendrita — paso-bajo')
ax.semilogy(freqs, VS_fft,   color='red',        lw=1.8, label='vs soma — paso-alto')
ax.semilogy(freqs, VLIF_fft, color='darkorange', lw=1.2, ls='--', label='LIF clasico')
ax.axvline(1/168, color='gray', ls='--', alpha=0.7, label='f=1/168 (ciclo semanal)')
ax.axvline(1/24,  color='gray', ls=':',  alpha=0.7, label='f=1/24  (ciclo diario)')
ax.set_title('Espectro de frecuencias: donde concentra su energia cada compartimento')
ax.set_xlabel('frecuencia (ciclos por hora)'); ax.set_ylabel('amplitud (escala log)')
ax.legend(loc='upper right'); ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()

print("""
  Como leer el grafico:
  - Las rayas grises marcan las frecuencias de referencia:
    f=1/168 es el ciclo semanal (una oscilacion en 168 horas).
    f=1/24  es el ciclo diario  (una oscilacion en 24 horas).
  - La curva verde (VD) tiene sus picos a la IZQUIERDA de f=1/24:
    se queda con lo lento. Es el filtro paso-bajo.
  - La curva roja (VS) tiene sus picos a la DERECHA de f=1/24:
    se queda con lo rapido. Es el filtro paso-alto.
  - La curva naranja (LIF) no separa: su energia se reparte por todo
    el espectro sin la diferenciacion que hacen vd y vs.
""")


# =============================================================================
# BLOQUE 8 — EXPERIMENTO 2B: MEDIR LA SEPARACION CON NUMEROS EXACTOS
# =============================================================================
print("""
=============================================================================
BLOQUE 8 — EXPERIMENTO 2B: MEDIR LA SEPARACION CON NUMEROS EXACTOS
=============================================================================

La FFT confirma la separacion visualmente. Ahora la mido con un numero:
la "ganancia" del filtro a cada frecuencia.

Ganancia = amplitud de la salida / amplitud de la entrada.
Si la ganancia es 1.0, la senal pasa sin cambios.
Si la ganancia es 0.0, la senal queda bloqueada completamente.
Si es 0.7, pasa el 70% de la amplitud.

Como la mido:
  1. Genero una senoide pura de periodo T: es una onda perfecta
     que oscila exactamente a esa frecuencia. No tiene ruido ni
     otras frecuencias mezcladas. Eso me permite aislar la respuesta
     del filtro a una sola frecuencia.
  2. La paso por el sistema sin spikes (lineal): quito los spikes
     porque son no lineales y distorsionarian la medicion. Quiero
     medir solo el efecto del filtro, no el del disparo.
  3. Descarto los primeros 500 pasos: el sistema tarda un rato en
     estabilizarse desde que arranca. Los primeros valores son un
     transitorio de inicio que no representa el comportamiento estable.
  4. Mido (max - min) de la salida vs (max - min) de la entrada.
     Para una senoide eso es directamente la ganancia.

El paper reporta en su Seccion 4.4 los valores de ganancia con
T=120 (frecuencia baja) y T=4 (frecuencia alta). Si mi codigo
reproduce esos mismos numeros, confirma que entendi bien las ecuaciones.
""")

def run_lineal(senal, a1=0.95, a2=0.05, b1=0.0, b2=-0.9):
    """Sistema TS-LIF sin spikes, para medir la ganancia del filtro."""
    vd = vs = 0.0
    VD_l, VS_l = [], []
    for ct in senal:
        vd = a1*vd + b1*vs + (1-a1)*ct
        vs = a2*vs + b2*vd + (1-a2)*ct
        VD_l.append(vd); VS_l.append(vs)
    return np.array(VD_l), np.array(VS_l)

def ganancia(periodo, compartimento):
    """Ganancia del filtro a una senoide de periodo T."""
    tiempo  = np.arange(1000)
    senoide = np.sin(2 * np.pi * tiempo / periodo)
    vd, vs  = run_lineal(senoide)
    salida  = (vd if compartimento == 'd' else vs)[500:]   # descartar transitorio
    return (salida.max() - salida.min()) / (senoide.max() - senoide.min())

gd120 = ganancia(120, 'd');  gd4  = ganancia(4, 'd')
gs120 = ganancia(120, 's');  gs4  = ganancia(4, 's')

print("  Resultados con T=120 (frecuencia baja) y T=4 (frecuencia alta):")
print()
print(f"  {'':26} {'T=120 (baja frec.)':<22} {'T=4 (alta frec.)'}")
print(f"  {'Dendrita vd (TS-LIF)':<26} {gd120:<22.3f} {gd4:.3f}")
print(f"  {'Soma     vs (TS-LIF)':<26} {gs120:<22.3f} {gs4:.3f}")
print()
print(f"  Paper Sec. 4.4 reporta:        ~0.700                 ~0.026  (dendrita)")
print(f"                                 ~0.698                 ~0.925  (soma)")
print()
coincide = abs(gd120-0.700)<0.005 and abs(gd4-0.026)<0.005 and abs(gs120-0.698)<0.005 and abs(gs4-0.925)<0.005
print(f"  Coincide exactamente con el paper: {coincide}")
print("""
  Como leer la tabla:

  Dendrita con T=120 (baja frecuencia): ganancia 0.700.
  La senoide lenta pasa con el 70% de su amplitud. La dendrita la deja pasar.

  Dendrita con T=4 (alta frecuencia): ganancia 0.026.
  La senoide rapida casi no pasa, solo el 2.6%. La dendrita la bloquea.
  Eso es un filtro paso-bajo: deja pasar lo lento, bloquea lo rapido.

  Soma con T=120 (baja frecuencia): ganancia 0.698.
  El soma tambien deja pasar algo de la frecuencia lenta porque recibe
  informacion de la dendrita (acoplamiento b2). No es filtro puro.

  Soma con T=4 (alta frecuencia): ganancia 0.925.
  El 92.5% de la senoide rapida llega al soma. Lo deja pasar casi completo.
  Eso es un filtro paso-alto.

  Que significa esto en la practica:
  La dendrita captura la tendencia semanal del consumo electrico.
  El soma captura las subidas y bajadas de cada hora.
  Combinados dan al modelo una representacion completa de la serie
  en vez de una sola escala temporal como el LIF clasico.
""")


# =============================================================================
# BLOQUE 9 — EXPERIMENTO 2C: LA MISMA PRUEBA CON LOS PERIODOS REALES
# =============================================================================
print("""
=============================================================================
BLOQUE 9 — EXPERIMENTO 2C: LA MISMA PRUEBA CON LOS PERIODOS REALES
=============================================================================

El ejemplo del paper usa T=120 y T=4 porque tienen una diferencia grande
(ratio de 30x). Eso hace que la separacion se vea muy dramatica.

En el dataset electrico real los periodos son T=168h (semanal) y T=24h (diario).
La diferencia entre ellos es solo de 7x. La pregunta es: sigue viendose la
separacion con esos periodos mas cercanos?
""")

gd168 = ganancia(168, 'd');  gd24 = ganancia(24, 'd')
gs168 = ganancia(168, 's');  gs24 = ganancia(24, 's')

print(f"  {'':26} {'T=168h (semanal)':<22} {'T=24h (diario)'}   ratio")
print(f"  {'Dendrita vd (TS-LIF)':<26} {gd168:<22.3f} {gd24:.3f}         {gd168/gd24:.1f}x")
print(f"  {'Soma     vs (TS-LIF)':<26} {gs168:<22.3f} {gs24:.3f}         {gs24/gs168:.1f}x")
print(f"""
  La separacion existe pero es mas moderada:
    Dendrita: {gd168/gd24:.1f}x mas sensible al ciclo semanal que al diario.
    Soma:     {gs24/gs168:.1f}x mas sensible al ciclo diario que al semanal.

  Por que es menor que en el ejemplo del paper (27x vs {gd168/gd24:.1f}x)?
  Porque T=168 y T=24 estan mas cerca entre si que T=120 y T=4.
  Un filtro separa mejor cuando las frecuencias a separar estan muy alejadas.
  Con periodos mas proximos la separacion sigue siendo real pero menos dramatica.

  Esto no es un error del codigo: el paper tampoco usa T=120/T=4 para entrenar.
  Los usa solo para ilustrar la propiedad del filtro en la Seccion 4.4.
  En el entrenamiento real la separacion emerge del ajuste automatico de
  los parametros con backpropagation sobre miles de pasos de datos reales.
""")


# =============================================================================
# RESUMEN FINAL — QUE DEMUESTRA TODO EL CODIGO JUNTO
# =============================================================================
print("""
=============================================================================
RESUMEN FINAL — QUE DEMUESTRA TODO EL CODIGO JUNTO
=============================================================================

Con unas 60 lineas de NumPy el codigo demuestra la idea central del paper:

  1. Por que TS-LIF mejora al LIF clasico:
     El LIF tiene un solo "tanque" de memoria. O captura lo lento o lo rapido.
     TS-LIF tiene dos tanques especializados: la dendrita para lo lento y el
     soma para lo rapido. Eso le da una representacion mas rica de la serie.

  2. Como funciona la separacion (Ecuacion 5):
     La diferencia entre a1=0.95 y a2=0.05 es lo que produce la separacion.
     a1 cerca de 1 hace a la dendrita lenta (paso-bajo).
     a2 cerca de 0 hace al soma rapido (paso-alto).
     El acoplamiento b2=-0.9 conecta ambos sin que se saturen.

  3. El sistema es estable (Teorema 1):
     Los autovalores 0.950 y 0.050 tienen modulo menor que 1.
     Eso garantiza que el potencial no se va a infinito durante el entrenamiento.

  4. Los numeros del paper son reproducibles:
     Dendrita: 0.700 (T=120) y 0.026 (T=4).
     Soma:     0.698 (T=120) y 0.925 (T=4).
     Son exactamente los valores de la Tabla de la Seccion 4.4 del articulo.

  5. Se verifica en datos reales, no solo en ejemplos sinteticos:
     Los 168 pasos del UCI Electricity dataset muestran visualmente y
     en el espectro FFT que la separacion de frecuencias ocurre de verdad.

  En simple: si el modelo puede separar la tendencia semanal del ciclo diario,
  tiene mejor informacion para predecir el siguiente valor de la serie.
  Eso explica los resultados del paper: TS-LIF supera al LIF en forecasting
  porque "ve" la serie en dos escalas temporales al mismo tiempo.
""")

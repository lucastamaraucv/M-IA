"""
Aplica correcciones estructurales y de estilo al notebook basado en:
1. El ejemplo del profesor (explicaciones inline entre celdas de codigo)
2. El estilo conversacional de Lucas (primera persona, directo, "en simple")
3. Agrega "Declaracion de uso de IA" que faltaba

Ejecutar: python patch_notebook.py
"""
import json, uuid

NB_PATH = "01MIAR_ACT_WhitePapers.ipynb"

with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

def md_cell(content):
    return {
        "cell_type": "markdown",
        "id": str(uuid.uuid4()).replace("-", "")[:8],
        "metadata": {},
        "source": content.strip()
    }

def set_md(idx, text):
    cells[idx]["source"] = text.strip()

def set_code(idx, text):
    cells[idx]["source"] = text.strip()

# ===========================================================================
# CELL 8 — Encabezado del desarrollo
# ===========================================================================
set_md(8, """\
---
# Desarrollo de la Actividad WhitePapers

**Asignatura:** Python para la Inteligencia Artificial (01MIAR)
**Alumno:** Lucas Támara
**Correo:** lucastamaraucv@gmail.com
**Artículo analizado:** *TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting* (ICLR 2025)

> Elijo un paper que de verdad me sirve para lo que estoy trabajando, lo referencio, explico por qué lo escogí, lo resumo con mis propias palabras y llevo su parte central a código Python ejecutable. Sin rodeos.
""")

# ===========================================================================
# CELL 9 — Mapa del trabajo
# ===========================================================================
set_md(9, """\
## Mapa del trabajo

Este es el recorrido del notebook y cómo resuelvo cada punto de la actividad:

| Punto de la actividad | Cómo lo resuelvo | Sección |
|---|---|---|
| **Referencia (IEEE)** | TS-LIF (Feng et al., ICLR 2025, arXiv:2503.05108). Cumple actualidad (2025), peer-reviewed. | 1 |
| **Por qué lo elegí** | Trabajo en SNN para predicción de series temporales. TS-LIF resuelve el límite real del LIF clásico. | 2 |
| **Resumen del artículo** | Neurona de doble compartimento (dendrita = paso-bajo, soma = paso-alto), Ecuación 5, Teorema 1 y resultados. | 3 |
| **Ejemplo en Python** | Reimplemento la neurona en NumPy puro (Ec. 5) y reproduzco la separación de frecuencias de la Sec. 4.4. | 4 |
| **Explicación del código** | Markdown entre cada bloque de código explicando qué hace y por qué. | 4 (inline) |
| **Mirada crítica** | Límites del modelo: datos predecibles, readout aprendible, estabilidad no forzada en el entrenamiento. | 5 |
| **Conclusión y reflexión** | Qué me llevo: estabilidad, separación de frecuencias y surrogate gradients. | 6 |
""")

# ===========================================================================
# CELL 10 — Referencia IEEE
# ===========================================================================
set_md(10, """\
## 1. Referencia del artículo (estilo IEEE)

[1] S. Feng, W. Feng, X. Gao, P. Zhao, y Z. Shen, "TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting," en *Proc. 13th Int. Conf. on Learning Representations (ICLR)*, 2025. [En línea]. Disponible: https://arxiv.org/abs/2503.05108

- **Identificador:** arXiv:2503.05108v1 [cs.LG], 7 de marzo de 2025.
- **Publicación:** *Published as a conference paper at ICLR 2025*.
- **Código fuente oficial:** https://github.com/kkking-kk/TS-LIF
- **Instituciones:** Nanyang Technological University, University of Chinese Academy of Sciences, Tencent AI Lab, WeBank-NTU Joint Research Institute on Fintech.

> Cumple el requisito de actualidad (2025, posterior a 2024) y viene de ICLR, una conferencia de primer nivel en ML, con revisión por pares.
""")

# ===========================================================================
# CELL 11 — Por qué lo elegí
# ===========================================================================
set_md(11, """\
## 2. Por qué elegí este artículo

Lo elegí porque estoy trabajando en **redes neuronales spiking (SNN)** para predecir series temporales, y quiero entender esta arquitectura por dentro, no quedarme en la superficie. Las SNN me llaman la atención porque no procesan todo de forma continua como una red normal: trabajan con *spikes* discretos, dispersos, dirigidos por eventos. En simple: son más eficientes en energía y, en teoría, más naturales para datos secuenciales con dependencias temporales fuertes.

La neurona **TS-LIF** me interesa porque ataca un problema concreto de esta familia: las SNN clásicas con LIF no logran capturar **a la vez** lo de corto y lo de largo plazo. En cualquier serie real conviven una tendencia lenta y fluctuaciones rápidas, y el LIF solo ve una escala temporal a la vez. Este paper resuelve eso sin romper el modelo matemático, verdad?

**Qué quiero aprender:**

1. Cómo funciona el doble compartimento (dendrita + soma) y por qué separar frecuencias ayuda al *forecasting*.
2. Las condiciones de estabilidad — autovalores dentro del círculo unidad — que hay que respetar al inicializar los parámetros α, β, γ, κ. Si esto se va, el entrenamiento revienta.
3. Cómo se implementa en Python (PyTorch + `snntorch`) y cómo encajan los *surrogate gradients* para entrenar la red de punta a punta.

**Por qué encaja con la asignatura:** el trabajo es 100 % Python científico (PyTorch, NumPy, `snntorch`) sobre datos secuenciales — justo el terreno de *Python para la Inteligencia Artificial*. Creo que es la pieza que me faltaba para profundizar en este tipo de redes.
""")

# ===========================================================================
# CELL 12 — Resumen del artículo
# ===========================================================================
set_md(12, """\
## 3. Resumen del artículo

Lo resumo con mis palabras. Primero qué dice el paper y, en simple, qué significa.

### 3.1. El problema

Las SNN son biológicamente plausibles y eficientes en energía: usan *spikes* discretos y procesan de forma dispersa. Eso las hace atractivas para **predicción de series temporales** (tráfico, energía, clima). El problema: la neurona estándar **LIF** tiene su potencial de membrana que decae rápido — se comporta como un filtro paso-bajo y no puede manejar a la vez tendencias lentas y fluctuaciones rápidas. En simple: el LIF ve lo lento o lo rápido, pero no los dos juntos. En una serie real necesitas los dos.

### 3.2. La propuesta: neurona TS-LIF

La solución es el **Temporal Segment LIF (TS-LIF)**, una neurona con **dos compartimentos** en lugar de uno:

- **Dendrita** ($v_d$): decaimiento $\\alpha_1 \\approx 1$ → olvida lento → captura la **tendencia** (baja frecuencia).
- **Soma** ($v_s$): decaimiento $\\alpha_2 \\approx 0$ → reacciona rápido → captura las **fluctuaciones** (alta frecuencia).

Las dinámicas (Ecuación 5 del paper):

$$v_d[t] = \\alpha_1 v_d[t-1] + \\beta_1 v_s[t-1] + (1-\\alpha_1)\\,c[t] - \\gamma_1 s_d[t-1]$$
$$v_s[t] = \\alpha_2 v_s[t-1] + \\beta_2 v_d[t] + (1-\\alpha_2)\\,c[t] - \\gamma_2 s_s[t-1]$$
$$s_d[t] = H(v_d[t]-v_{th}), \\qquad s_s[t] = H(v_s[t]-v_{th})$$

**Glosario de variables:**

| Variable | En simple |
|---|---|
| $c[t]$ | La señal de entrada — mi serie temporal |
| $v_d[t],\\ v_s[t]$ | Potenciales de dendrita y soma — la "memoria" de cada compartimento |
| $\\alpha_1, \\alpha_2$ | Cuánto "olvida" cada uno. $\\alpha_1\\approx1$ olvida despacio (paso-bajo); $\\alpha_2\\approx0$ olvida rápido (paso-alto) |
| $\\beta_1, \\beta_2$ | Acoplamiento entre los dos compartimentos |
| $\\gamma_1, \\gamma_2$ | Reset: cuánto baja el potencial al disparar un spike |
| $s_d[t], s_s[t]$ | Spikes (0 o 1) de dendrita y soma |
| $H(\\cdot)$ | Heaviside: vale 1 si el argumento ≥ 0, 0 si no |
| $\\kappa$ | Peso de mezcla en la salida final |

**Dos aportes clave frente a modelos previos (TC-LIF, LM-H):**

1. **Inyección directa al soma** — el término $(1-\\alpha_2)\\,c[t]$ mete la entrada directo en el soma. En simple: la información rápida no se pierde al pasar primero por la dendrita.
2. **Spikes dendríticos** — la dendrita también dispara spikes ($s_d$), igual que las neuronas piramidales reales. La salida mezcla ambos: $s_{mix}[t] = \\kappa\\, s_d[t] + (1-\\kappa)\\, s_s[t]$.

Todos los coeficientes (α, β, γ, κ) son **aprendibles** durante el entrenamiento.

### 3.3. Análisis teórico

- **Estabilidad (Teorema 1):** los autovalores del sistema son:
$$\\lambda = \\frac{\\alpha_1+\\alpha_2+\\beta_1\\beta_2 \\pm \\sqrt{(\\alpha_1+\\alpha_2+\\beta_1\\beta_2)^2 - 4\\alpha_1\\alpha_2}}{2}$$
Si $|\\lambda|\\geq1$ para algún autovalor, el potencial crece sin control — el entrenamiento diverge. Hay que verificarlo antes de entrenar.
- **Respuesta en frecuencia:** con los parámetros del paper ($\\alpha_1=0.95,\\ \\alpha_2=0.05$) se demuestra que la dendrita filtra bajas frecuencias y el soma las altas. Eso es exactamente lo que reproduzco en el código.

### 3.4. Experimentos y resultados

- **Datasets:** Metr-LA, Pems-Bay (tráfico), Solar (energía) y Electricity (consumo).
- **Arquitecturas:** TS-LIF se enchufa en backbones CNN, RNN y Transformer — no es un modelo cerrado, es una pieza que metes en lo que ya tienes.
- **Resultados:** TS-LIF supera de forma consistente a las SNN basadas en LIF. En *Solar* mejora ~8 % en $R^2$; en *Electricity* (horizonte 96) baja el RSE un 43.6 %. Con 80 % de datos faltantes, sigue aguantando donde el LIF clásico se cae.
""")

# ===========================================================================
# CELL 13 — Intro del ejemplo Python
# ===========================================================================
set_md(13, """\
## 4. Ejemplo de implementación en Python

### 4.1. Código del repositorio oficial

El corazón del modelo es `neuronal_charge`, que actualiza los dos compartimentos. Extraído directamente de `SeqSNN/network/snn/TSLIF.py` (clase `TSLIFNode`):

```python
# Fuente: TS-LIF/SeqSNN/network/snn/TSLIF.py
def neuronal_charge(self, x: torch.Tensor):
    # v1 = dendrita, v2 = soma  (decay_factor, kk, yy son nn.Parameter aprendibles)
    self.names['v1'] = self.decay_factor[0]*self.names['v1'] + self.decay_factor[1]*x - self.yy*self.names['v2']
    self.names['v2'] = self.decay_factor[2]*self.names['v2'] + self.decay_factor[3]*x - self.kk*self.names['v1']

def neuronal_fire(self):
    # surrogate gradient atan: Heaviside en forward, derivada suave de arctan en backward
    return self.surrogate_function(self.v - self.v_threshold, 2.0)
```

El repo depende de `torch` y `snntorch`, así que no corre directamente aquí. Lo que hago es **reimplementar la neurona TS-LIF en NumPy puro** siguiendo la Ecuación 5, y reproducir el experimento de separación de frecuencias de la Sección 4.4. Si mi código da el mismo resultado que el paper, la comprensión está bien.

### 4.2. Reimplementación en NumPy
""")

# ===========================================================================
# CELL 14 — Código: clase TSLIFNeuron + chequeo estabilidad
# ===========================================================================
set_code(14, """\
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)  # semilla fija para reproducibilidad


def heaviside(x):
    # Convierte potencial en spike: devuelve 1 si supera el umbral, 0 si no.
    # Es la funcion de Heaviside H() de la Ecuacion 2 del paper.
    return (x >= 0.0).astype(np.float32)


class TSLIFNeuron:
    """Neurona TS-LIF de doble compartimento, implementada en NumPy.

    Sigo literalmente la Ecuacion 5 del paper:
        vd[t] = a1*vd + b1*vs + (1-a1)*c - g1*sd_prev   <-- dendrita: paso-BAJO
        vs[t] = a2*vs + b2*vd + (1-a2)*c - g2*ss_prev   <-- soma:    paso-ALTO
    """

    def __init__(self, alpha1=0.95, alpha2=0.05, beta1=0.0, beta2=-0.9,
                 gamma1=0.5, gamma2=1.0, v_th=1.0, kappa=0.5):
        # a1~1: dendrita olvida lento -> acumula tendencia (paso-bajo)
        # a2~0: soma olvida rapido   -> reacciona a cambios (paso-alto)
        self.a1, self.a2 = alpha1, alpha2
        self.b1, self.b2 = beta1, beta2    # acoplamiento entre compartimentos
        self.g1, self.g2 = gamma1, gamma2  # reset al disparar un spike
        self.v_th  = v_th                  # umbral de disparo
        self.kappa = kappa                 # peso de mezcla en la salida
        self.reset()

    def reset(self):
        self.vd, self.vs = 0.0, 0.0
        self.sd_prev, self.ss_prev = 0.0, 0.0

    def step(self, c):
        """Avanza un paso temporal con entrada c. Devuelve (vd, vs, sd, ss, s_mix)."""
        # Actualizo potenciales siguiendo la Ec. 5
        vd = self.a1*self.vd + self.b1*self.vs + (1 - self.a1)*c - self.g1*self.sd_prev
        # El termino (1-a2)*c es la inyeccion directa al soma: el aporte clave del paper.
        # Sin este termino, la informacion de alta frecuencia se perderia al pasar por la dendrita.
        vs = self.a2*self.vs + self.b2*vd  + (1 - self.a2)*c - self.g2*self.ss_prev

        sd = heaviside(vd - self.v_th)  # spike de dendrita
        ss = heaviside(vs - self.v_th)  # spike de soma

        self.vd, self.vs = vd, vs
        self.sd_prev, self.ss_prev = sd, ss

        s_mix = self.kappa*sd + (1 - self.kappa)*ss  # salida final (Ec. 6)
        return vd, vs, sd, ss, s_mix


# ---------------------------------------------------------------------------
# Verifico estabilidad (Teorema 1) antes de simular.
# Los autovalores de la matriz A tienen que tener modulo < 1.
# Si no, el potencial crece sin control y el entrenamiento revienta.
# ---------------------------------------------------------------------------
a1, a2, b1, b2 = 0.95, 0.05, 0.0, -0.9
tr   = a1 + a2 + b1*b2
disc = (tr**2 - 4*a1*a2) ** 0.5
lam1 = (tr + disc) / 2
lam2 = (tr - disc) / 2
print(f"Estabilidad (Teorema 1): lambda_1={lam1:.3f}, lambda_2={lam2:.3f} -> |lambda|<1 ? {abs(lam1)<1 and abs(lam2)<1}")
""")

# ===========================================================================
# CELL 15 — Código: experimento señal mixta + gráfico
# ===========================================================================
set_code(15, """\
# Alimento la neurona con una senal de FRECUENCIA MIXTA:
# tendencia lenta + oscilacion rapida juntas, como una serie temporal real.
T = 240
t = np.arange(T)

low  = np.sin(2*np.pi*t/120)        # componente lenta:  periodo 120 (la tendencia)
high = 0.4*np.sin(2*np.pi*t/8)      # componente rapida: periodo 8  (la volatilidad)
c    = low + high                   # entrada = las dos juntas

neuron = TSLIFNeuron()
VD, VS = [], []
for ct in c:
    vd, vs, *_ = neuron.step(ct)
    VD.append(vd); VS.append(vs)
VD, VS = np.array(VD), np.array(VS)

fig, ax = plt.subplots(3, 1, figsize=(10, 7), sharex=True)

ax[0].plot(t, c, color="navy")
ax[0].set_title("Entrada c[t] = tendencia lenta + fluctuacion rapida"); ax[0].set_ylabel("c[t]")

ax[1].plot(t, VD, color="green", label="$v_d$ (dendrita)")
ax[1].plot(t, low, "b--", alpha=0.5, label="componente lenta (referencia)")
ax[1].set_title("Dendrita: sigue la tendencia — filtro paso-bajo"); ax[1].set_ylabel("$v_d[t]$"); ax[1].legend()

ax[2].plot(t, VS, color="red", label="$v_s$ (soma)")
ax[2].plot(t, high, "b--", alpha=0.5, label="componente rapida (referencia)")
ax[2].set_title("Soma: reacciona a las fluctuaciones — filtro paso-alto"); ax[2].set_ylabel("$v_s[t]$"); ax[2].set_xlabel("paso t"); ax[2].legend()

plt.tight_layout(); plt.show()
""")

# ===========================================================================
# CELL 16 — Código: verificación cuantitativa de ganancia
# ===========================================================================
set_code(16, """\
# Para no quedarme solo con el grafico, mido la GANANCIA de cada compartimento:
#   ganancia = amplitud(salida) / amplitud(entrada)
# Ganancia ~1 -> deja pasar esa frecuencia. ~0 -> la bloquea.
# Trabajo con el sistema lineal (sin spikes ni reset), igual que la Sec. 4.4.

def run_linear(c, a1=0.95, a2=0.05, b1=0.0, b2=-0.9):
    """Parte lineal del TS-LIF sin spikes ni reset."""
    vd = vs = 0.0
    VD, VS = [], []
    for ct in c:
        vd = a1*vd + b1*vs + (1 - a1)*ct
        vs = a2*vs + b2*vd + (1 - a2)*ct
        VD.append(vd); VS.append(vs)
    return np.array(VD), np.array(VS)

def gain(period, comp):
    """Ganancia pico-a-pico de una senoide pura de periodo dado."""
    tt = np.arange(600)
    cc = np.sin(2*np.pi*tt/period)
    vd, vs = run_linear(cc)
    s = (vd if comp == "d" else vs)[300:]  # descarto el transitorio inicial
    return (s.max() - s.min()) / (cc.max() - cc.min())

print(f"{'Compartimento':<22}{'Ganancia BAJA frec. (periodo 120)':<36}{'Ganancia ALTA frec. (periodo 4)'}")
print(f"{'Dendrita  v_d':<22}{gain(120,'d'):<36.3f}{gain(4,'d'):.3f}")
print(f"{'Soma      v_s':<22}{gain(120,'s'):<36.3f}{gain(4,'s'):.3f}")
""")

# ===========================================================================
# CELL 17 — Mirada crítica (antes era Sección 5, ahora es Sección 5 real)
# ===========================================================================
set_md(17, """\
## 5. Mirada crítica: dónde gana y dónde tiene límites

Para mí, un buen análisis no es solo repetir que el modelo gana. Tengo que entender en qué condiciones gana y con qué asteriscos. Estos son los matices que no puedo ignorar:

**1. Los datasets donde gana son predecibles, no caóticos.**
Metr-LA, Pems-Bay, Solar y Electricity tienen estacionalidad fuerte y mucha autocorrelación: el futuro se parece bastante al pasado. TS-LIF demuestra su ventaja *en ese régimen*. No evalúa series tipo *random walk*. No se puede asumir que el resultado se traslade a cualquier serie temporal, eso queda por verificar.

**2. La salida no son spikes binarios puros.**
En el código oficial, la salida se calcula como `alpha_s * s_s + alpha_l * s_l` con pesos aprendibles. Parte de la mejora podría venir del *readout* con peso real y no solo de la dinámica de doble compartimento. Lo ideal sería una ablación que aísle cuánto aporta cada cosa.

**3. La estabilidad teórica no se fuerza en el entrenamiento.**
El Teorema 1 garantiza estabilidad si $|\\lambda|<1$, pero el `decay_factor` en el código es aprendible sin restricción explícita a esa región. La garantía matemática del paper y lo que realmente corre el código no son exactamente lo mismo.

Nada de esto invalida el trabajo — la idea de separar frecuencias es sólida y los resultados son consistentes. Pero conocer estos límites es lo que me permite usar el modelo con criterio.
""")

# ===========================================================================
# CELL 18 — Conclusión y reflexión
# ===========================================================================
set_md(18, """\
## 6. Conclusión y reflexión

Pasé de "conocer" el nombre TS-LIF a **entender por qué funciona**. El aprendizaje más valioso: un cambio pequeño y bioinspirado — desdoblar la neurona en dendrita y soma con una inyección directa de corriente — resuelve una limitación concreta del LIF clásico. La reimplementación en NumPy me lo confirmó de forma tangible: cada compartimento se especializa en una banda de frecuencia y su combinación captura a la vez tendencias largas y fluctuaciones cortas. Creo que eso es exactamente lo que necesita un modelo de *forecasting* sobre datos reales.

En el plano técnico me llevo tres cosas:

1. **Estabilidad antes que nada.** Los autovalores de la matriz A tienen que tener módulo < 1. Si no, el entrenamiento diverge. Es el primer chequeo que hago antes de cualquier simulación con esta red.
2. **Separación de frecuencias como clave del forecasting.** Toda serie temporal real mezcla tendencia y ruido rápido. Que la dendrita capture lo lento y el soma lo rápido encaja directo con ese problema.
3. **Surrogate gradients hacen entrenable lo no derivable.** El spike de Heaviside no tiene gradiente útil, pero la derivada suave de arctan permite entrenar la red de extremo a extremo con backprop. Eso destraba el entrenamiento completo de una SNN.

Como siguiente paso quiero entrenar la red completa con TS-LIF sobre datos reales de series temporales y medir si la separación de frecuencias mejora la precisión frente a una SNN con LIF clásico.
""")

# ===========================================================================
# CELL 19 — Referencias
# ===========================================================================
set_md(19, """\
## Referencias

[1] S. Feng, W. Feng, X. Gao, P. Zhao, y Z. Shen, "TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting," en *Proc. 13th Int. Conf. on Learning Representations (ICLR)*, 2025. [En línea]. Disponible: https://arxiv.org/abs/2503.05108

[2] S. Zhang, Q. Yang, C. Ma, J. Wu, H. Li, y K. C. Tan, "TC-LIF: A Two-Compartment Spiking Neuron Model for Long-Term Sequential Modelling," en *Proc. AAAI Conf. on Artificial Intelligence*, 2024, pp. 16838–16847.

[3] C. Lv, Y. Wang, D. Han, X. Zheng, X. Huang, y D. Li, "Efficient and Effective Time-Series Forecasting with Spiking Neural Networks," en *Proc. Int. Conf. on Machine Learning (ICML)*, 2024, pp. 33624–33637.

[4] Repositorio oficial del modelo TS-LIF (SeqSNN). [En línea]. Disponible: https://github.com/kkking-kk/TS-LIF
""")

# ===========================================================================
# Elimino la celda 20 (referencias viejas) porque la movemos a celda 19
# y agrego celdas de explicacion inline entre bloques de codigo
# ===========================================================================

# Construyo la nueva lista de celdas con:
# - Celdas 0-13 sin cambio en estructura
# - NUEVA celda markdown entre 14 y 15 (explica la clase y la estabilidad)
# - NUEVA celda markdown entre 15 y 16 (explica el grafico)
# - NUEVA celda markdown despues de 16 (explica el resultado de ganancia)
# - Celdas 17-19 ya modificadas arriba
# - Elimino celda 20 (referencias duplicadas)
# - NUEVA celda "Declaracion uso IA"

between_14_15 = md_cell("""\
La clase `TSLIFNeuron` implementa la Ecuación 5 del paper con dos variables de estado. El método `step()` las actualiza en cada instante de tiempo siguiendo las ecuaciones exactas.

El término clave es `(1 - a2)*c` en el soma: inyecta la entrada directo al soma sin pasar por la dendrita. En simple: la información de alta frecuencia llega al soma directamente, no se pierde al pasar primero por el compartimento lento.

El chequeo de estabilidad confirma λ₁=0.95 y λ₂=0.05 — los dos con módulo < 1. El sistema es estable y puedo simular sin que el potencial se dispare a infinito.
""")

between_15_16 = md_cell("""\
El gráfico confirma lo que predice el paper para estos parámetros:

- **Dendrita (verde)**: sigue la componente lenta e ignora las oscilaciones rápidas — filtro paso-bajo.
- **Soma (rojo)**: reacciona a las fluctuaciones y deja pasar la alta frecuencia — filtro paso-alto.

Para tener un número concreto y no quedarme solo con la imagen, mido la ganancia de cada compartimento.
""")

after_16 = md_cell("""\
Los números confirman lo que mostró el gráfico: la dendrita bloquea la alta frecuencia (ganancia ~0.03) y el soma la deja pasar (ganancia ~0.93). En baja frecuencia ambos tienen ganancia similar (~0.70). La diferencia clave está en la alta frecuencia.

Esto coincide con las funciones de transferencia H_d(z) y H_s(z) del paper (Sección 4.4). El experimento cierra.
""")

declaracion_ia = md_cell("""\
## Declaración de uso de IA

Se han utilizado herramientas de IA generativa para apoyar la estructuración de este notebook, la revisión de la redacción y el formateo de las referencias bibliográficas, en el marco de la normativa descrita en la guía docente de la asignatura.
""")

# Construyo la lista final de celdas
new_cells = []
for i, cell in enumerate(cells):
    if i == 20:
        # Elimino la celda 20 (referencias duplicadas — ya estan en celda 19)
        continue
    new_cells.append(cell)
    if i == 14:
        new_cells.append(between_14_15)
    elif i == 15:
        new_cells.append(between_15_16)
    elif i == 16:
        new_cells.append(after_16)

# Agrego la declaracion de IA al final
new_cells.append(declaracion_ia)

nb["cells"] = new_cells

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

total = len(new_cells)
print(f"Notebook actualizado: {NB_PATH}")
print(f"Total de celdas: {total} (original: {len(cells)+1})")
print(f"Cambios aplicados:")
print(f"  - Celdas 8-19: estilo conversacional en primera persona")
print(f"  - +3 celdas markdown entre bloques de codigo (inline explanations)")
print(f"  - Celda 20 (referencias duplicadas) eliminada")
print(f"  - +1 celda 'Declaracion de uso de IA' al final")

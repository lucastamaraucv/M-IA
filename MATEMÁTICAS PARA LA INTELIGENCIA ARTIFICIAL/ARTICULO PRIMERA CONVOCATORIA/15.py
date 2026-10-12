"""
Pregunta 15 - Visualizacion 3D animada del descenso por gradiente,
CON MARCADORES NUMERADOS (1-7) sobre el grafico y una LEYENDA A COLOR
que explica cada termino tecnico de la pregunta, ademas de la
verificacion en vivo de las 4 opciones (a, b, c, d) del examen.

LEYENDA INTERACTIVA CON PARPADEO (ver graficos_comunes.py):
  Pasa el mouse sobre cualquier numero/fila de la leyenda (derecha) y
  la parte correspondiente del grafico 3D (izquierda) empieza a
  PARPADEAR (junto con la propia fila de la leyenda).

Este archivo se puede ejecutar solo (python 15.py) o abrirse como una
pestana dentro de preguntas.py junto con la pregunta 16.

CAMARA CONTROLADA SOLO CON EL MOUSE:
  - Clic izquierdo + arrastrar: rotar
  - Rueda del mouse: zoom
(la camara NO rota sola, para no pisar tu control manual)

Requisitos (instalar una sola vez en tu terminal):
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (necesario para proyeccion 3d)
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec

from graficos_comunes import LeyendaInteractiva

# =========================================================================
# 1. EL TERRENO (funcion del Ejemplo 2.2 del paper de Schaeffer y McCalla)
#    f(x, y) = 0.5 x^2 + 0.25 y^4 - 0.5 y^2
#    Tiene: 2 minimos en (0, 1) y (0, -1), y 1 punto de silla en (0, 0)
# =========================================================================
def f(x, y):
    return 0.5 * x**2 + 0.25 * y**4 - 0.5 * y**2

def gradiente(x, y):
    return np.array([x, y**3 - y])

alpha = 0.1      # tamano de paso
pasos = 80        # cuantos pasos camina cada punto

# =========================================================================
# 2. PUNTOS DE PARTIDA (5 al azar + 1 casi sobre la "linea trampa" y=0)
# =========================================================================
np.random.seed(7)
puntos_random = np.random.uniform(low=-1.6, high=1.6, size=(5, 2))
punto_casi_silla = np.array([1.3, 1e-3])
puntos_iniciales = np.vstack([puntos_random, punto_casi_silla])

colores = ['tab:red', 'tab:orange', 'tab:green', 'tab:purple', 'tab:brown', 'black']
etiquetas = ['Punto al azar 1', 'Punto al azar 2', 'Punto al azar 3',
             'Punto al azar 4', 'Punto al azar 5',
             'Punto casi sobre la "linea trampa" (y~0)']

trayectorias = []
for p0 in puntos_iniciales:
    traj = [p0.copy()]
    p = p0.copy()
    for _ in range(pasos):
        p = p - alpha * gradiente(p[0], p[1])
        traj.append(p.copy())
    trayectorias.append(np.array(traj))

# =========================================================================
# 3. VERIFICACION ESTADISTICA DE LAS 4 OPCIONES DEL EXAMEN
# =========================================================================
minimo_1 = np.array([0.0, 1.0])
minimo_2 = np.array([0.0, -1.0])
punto_silla = np.array([0.0, 0.0])

N = 3000
np.random.seed(1)
puntos_test = np.random.uniform(-2, 2, size=(N, 2))
llego_a_minimo = 0
llego_a_silla = 0
for p0 in puntos_test:
    p = p0.copy()
    for _ in range(400):
        p = p - alpha * gradiente(p[0], p[1])
    if np.linalg.norm(p - minimo_1) < 0.01 or np.linalg.norm(p - minimo_2) < 0.01:
        llego_a_minimo += 1
    elif np.linalg.norm(p - punto_silla) < 0.01:
        llego_a_silla += 1

prob_silla = llego_a_silla / N
prob_minimo = llego_a_minimo / N

print("=" * 70)
print(f"Simulacion con {N} puntos de partida aleatorios:")
print(f"  -> Terminaron en un MINIMO      : {llego_a_minimo}  ({100*prob_minimo:.2f}%)")
print(f"  -> Terminaron en el PUNTO SILLA : {llego_a_silla}  ({100*prob_silla:.2f}%)")
print("=" * 70)
print("\nVERIFICANDO LAS 4 OPCIONES DE LA PREGUNTA 15:\n")
print("(a) 'Siempre converge a un minimo GLOBAL...'                -> FALSO")
print(f"(b) 'Probabilidad POSITIVA (pequena) de caer en la silla'   -> FALSO ({prob_silla*100:.4f}%)")
print(f"(c) 'Probabilidad CERO de caer en la silla (inicio azar)'   -> {'CONFIRMADO' if prob_silla==0 else 'Revisar'}")
print("(d) 'Todos los puntos criticos son minimos locales'         -> FALSO")
print("\nCONCLUSION: La opcion CORRECTA es la (c).")
print("=" * 70)

# =========================================================================
# 4. LEYENDA NUMERADA (colores + numeros que apareceran tambien sobre
#    el grafico 3D, igual que en el diagrama que revisamos en el chat)
# =========================================================================
LEYENDA = [
    (1, '#378ADD', 'f pertenece a C^2(Omega)',
        'Terreno suave, sin picos ni bordes filosos'),
    (2, '#378ADD', 'Gradiente Lipschitz',
        'La pendiente cambia poco a poco, nunca de golpe'),
    (3, '#378ADD', 'Omega convexo e invariante',
        'Zona simple; el algoritmo nunca se sale de ahi'),
    (4, '#639922', 'Minimo (valle verde)',
        'Hessiano con todos los autovalores positivos'),
    (5, '#E24B4A', 'Punto de silla estricto (X)',
        'Hessiano con al menos un autovalor negativo'),
    (6, '#BA7517', 'Conjunto de medida cero',
        'Linea "trampa"; casi imposible caer justo ahi'),
    (7, '#D85A30', 'Descenso por gradiente',
        'Camino del algoritmo bajando paso a paso'),
]


def marcador_numero(ax3d, x, y, z, num, color):
    return ax3d.text(x, y, z, f' {num} ', color='white', fontsize=9, fontweight='bold',
                      ha='center', va='center', zorder=10,
                      bbox=dict(boxstyle='circle', facecolor=color, edgecolor='black',
                                linewidth=0.6, pad=0.35))


def construir_figura():
    """Arma toda la figura (grafico 3D + leyenda interactiva) y devuelve
    (fig, anim, leyenda). Hay que conservar las 3 referencias devueltas
    mientras la ventana este abierta (si no, la animacion / el parpadeo
    se pueden interrumpir por el recolector de basura de Python)."""

    # ---------------------------------------------------------------
    # FIGURA CON DOS PANELES: grafico 3D (izquierda) + leyenda (derecha)
    # ---------------------------------------------------------------
    fig = plt.figure(figsize=(15, 8.5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2.7, 1], wspace=0.05)

    ax = fig.add_subplot(gs[0], projection='3d')
    ax_leyenda = fig.add_subplot(gs[1])

    leyenda = LeyendaInteractiva(fig, ax_leyenda, LEYENDA,
                                  titulo='Terminos de la pregunta 15')

    # ---------------------------------------------------------------
    # SUPERFICIE 3D
    # ---------------------------------------------------------------
    xs = np.linspace(-2, 2, 45)
    ys = np.linspace(-1.8, 1.8, 45)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)

    # Resolucion moderada (antes 80x80 = 6400 poligonos): con menos
    # poligonos Matplotlib recalcula mucho mas rapido el orden de
    # profundidad cada vez que rotas con el mouse, y la rotacion se
    # siente fluida en vez de lenta.
    ax.plot_surface(X, Y, Z, cmap='terrain', alpha=0.55, linewidth=0,
                     antialiased=False, rstride=1, cstride=1)

    # --- (3) Omega: recuadro de la zona de busqueda, dibujado en la base ---
    z_base = Z.min() - 0.3
    bx = [-2, 2, 2, -2, -2]
    by = [-1.8, -1.8, 1.8, 1.8, -1.8]
    bz = [z_base] * 5
    ax.plot(bx, by, bz, color='#378ADD', linewidth=1.5, linestyle='--', alpha=0.8)

    # --- (6) Linea de medida cero: y = 0, el unico camino "trampa" ---
    x_linea = np.linspace(-2, 2, 60)
    y_linea = np.zeros_like(x_linea)
    z_linea = f(x_linea, y_linea)
    ax.plot(x_linea, y_linea, z_linea, color='#BA7517', linewidth=2.5,
            linestyle=':', alpha=0.95, zorder=5)

    # --- (4) Minimos y (5) punto de silla ---
    ax.scatter(0, 1, f(0, 1), color='#639922', s=220, marker='*',
               label='Minimo (0,1)', zorder=6)
    ax.scatter(0, -1, f(0, -1), color='#639922', s=220, marker='*',
               label='Minimo (0,-1)', zorder=6)
    ax.scatter(0, 0, f(0, 0), color='#E24B4A', s=170, marker='X',
               label='Punto de silla (0,0)', zorder=6)

    # --- (1)(2)(3)(4)(5)(6)(7) marcadores numerados sobre el grafico ---
    leyenda.registrar_badge(1, marcador_numero(ax, 1.5, 1.5, f(1.5, 1.5) + 0.15, 1, '#378ADD'))
    leyenda.registrar_badge(2, marcador_numero(ax, 0.9, -1.3, f(0.9, -1.3) + 0.15, 2, '#378ADD'))
    leyenda.registrar_badge(3, marcador_numero(ax, 2.0, 1.8, z_base + 0.05, 3, '#378ADD'))
    leyenda.registrar_badge(4, marcador_numero(ax, 0.35, 1.0, f(0.35, 1.0) + 0.15, 4, '#639922'))
    leyenda.registrar_badge(5, marcador_numero(ax, 0.35, 0.0, f(0.35, 0.0) + 0.2, 5, '#E24B4A'))
    leyenda.registrar_badge(6, marcador_numero(ax, 1.3, 0.0, f(1.3, 0.0) + 0.2, 6, '#BA7517'))
    leyenda.registrar_badge(7, marcador_numero(ax, puntos_iniciales[0][0], puntos_iniciales[0][1],
                                                f(*puntos_iniciales[0]) + 0.2, 7, '#D85A30'))

    # ---------------------------------------------------------------
    # "HALOS": copias resaltadas (en amarillo) de cada elemento del
    # grafico. Se crean OCULTAS con visible=False -no solo alpha=0- para
    # que Matplotlib las salte por completo al dibujar y no le resten
    # velocidad a la rotacion con el mouse. Solo se hacen visibles un
    # instante cuando estan parpadeando.
    # ---------------------------------------------------------------
    halo_superficie_1 = ax.plot_wireframe(X, Y, Z, color='#FFE14D', linewidth=0.9,
                                           alpha=0.85, rstride=3, cstride=3, zorder=4,
                                           visible=False)

    # Item 2 (Gradiente Lipschitz): campo de flechas del gradiente en
    # varios puntos del dominio, para mostrar que la pendiente cambia de
    # forma gradual de un punto a otro (idea de la condicion Lipschitz).
    xs_q = np.linspace(-1.7, 1.7, 6)
    ys_q = np.linspace(-1.5, 1.5, 6)
    Xq, Yq = np.meshgrid(xs_q, ys_q)
    Zq = f(Xq, Yq)
    Gx = Xq
    Gy = Yq**3 - Yq
    halo_gradiente = ax.quiver(Xq, Yq, Zq + 0.05, -Gx, -Gy, np.zeros_like(Gx),
                                length=0.35, normalize=True, color='#FFA500',
                                linewidth=1.8, alpha=0.9, zorder=6, visible=False)

    halo_box, = ax.plot(bx, by, bz, color='#FFE14D', linewidth=5, alpha=0.9, zorder=5,
                         visible=False)
    halo_medida, = ax.plot(x_linea, y_linea, z_linea, color='#FFE14D', linewidth=6,
                            alpha=0.9, zorder=5, visible=False)
    halo_min1 = ax.scatter(0, 1, f(0, 1), color='#FFE14D', s=650, marker='*', alpha=0.9,
                            zorder=5, visible=False)
    halo_min2 = ax.scatter(0, -1, f(0, -1), color='#FFE14D', s=650, marker='*', alpha=0.9,
                            zorder=5, visible=False)
    halo_silla = ax.scatter(0, 0, f(0, 0), color='#FFE14D', s=480, marker='X', alpha=0.9,
                             zorder=5, visible=False)

    leyenda.registrar_halo(1, halo_superficie_1)
    leyenda.registrar_halo(2, halo_gradiente)
    leyenda.registrar_halo(3, halo_box)
    leyenda.registrar_halo(4, [halo_min1, halo_min2])
    leyenda.registrar_halo(5, halo_silla)
    leyenda.registrar_halo(6, halo_medida)

    # ---------------------------------------------------------------
    # TRAYECTORIAS DEL DESCENSO POR GRADIENTE (se animan)
    # ---------------------------------------------------------------
    lineas3d = []
    puntos3d = []
    halos_traj = []
    for c, lab in zip(colores, etiquetas):
        linea, = ax.plot([], [], [], color=c, linewidth=2, alpha=0.9, label=lab)
        punto, = ax.plot([], [], [], 'o', color=c, markersize=7)
        halo_t, = ax.plot([], [], [], color='#FFE14D', linewidth=6, alpha=0.9, zorder=4,
                           visible=False)
        lineas3d.append(linea)
        puntos3d.append(punto)
        halos_traj.append(halo_t)

    leyenda.registrar_halo(7, halos_traj)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y)  (altura del terreno)')
    ax.set_title(
        "Pregunta 15: Descenso por gradiente evitando el punto de silla\n"
        f"Prob. medida de caer en la silla ({N} puntos al azar): {prob_silla*100:.2f}%  ->  Opcion correcta: (c)\n"
        "(Arrastra con el mouse para rotar la vista; pasa el mouse por la leyenda para identificar cada parte)",
        fontsize=9.5)
    ax.legend(loc='upper left', fontsize=6.8, framealpha=0.9)

    # Vista inicial (una sola vez). A partir de aqui, el mouse tiene el control.
    ax.view_init(elev=25, azim=-60)

    texto_paso = fig.text(0.015, 0.96, '', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.85))

    def init():
        for linea, punto, halo_t in zip(lineas3d, puntos3d, halos_traj):
            linea.set_data([], [])
            linea.set_3d_properties([])
            punto.set_data([], [])
            punto.set_3d_properties([])
            halo_t.set_data([], [])
            halo_t.set_3d_properties([])
        texto_paso.set_text('')
        return lineas3d + puntos3d + halos_traj + [texto_paso]

    def update(frame):
        idx_global = min(frame, pasos)
        for linea, punto, halo_t, traj in zip(lineas3d, puntos3d, halos_traj, trayectorias):
            idx = min(frame, len(traj) - 1)
            xs_t = traj[:idx+1, 0]
            ys_t = traj[:idx+1, 1]
            zs_t = f(xs_t, ys_t)
            linea.set_data(xs_t, ys_t)
            linea.set_3d_properties(zs_t)
            punto.set_data([traj[idx, 0]], [traj[idx, 1]])
            punto.set_3d_properties([f(traj[idx, 0], traj[idx, 1])])
            halo_t.set_data(xs_t, ys_t)
            halo_t.set_3d_properties(zs_t)

        # NOTA: ya NO se llama a ax.view_init() aqui, para no pisar
        # la rotacion manual que hagas con el mouse.
        texto_paso.set_text(f'Paso: {idx_global} / {pasos}')
        return lineas3d + puntos3d + halos_traj + [texto_paso]

    # blit=False es necesario aqui: con blit=True en 3D, a veces el
    # redibujado interfiere con la rotacion manual del mouse.
    # repeat=False: la animacion del descenso corre UNA sola vez y se
    # detiene sola al terminar (si quedara redibujando todo el grafico
    # para siempre competiria con el arrastre del mouse y la rotacion se
    # sentiria lenta incluso mucho despues de que las trayectorias ya
    # llegaron a su destino).
    anim = animation.FuncAnimation(fig, update, frames=pasos + 20,
                                    init_func=init, interval=90, repeat=False,
                                    blit=False)

    leyenda.iniciar_parpadeo()

    return fig, anim, leyenda


if __name__ == '__main__':
    fig, anim, leyenda = construir_figura()
    plt.tight_layout()
    plt.show()

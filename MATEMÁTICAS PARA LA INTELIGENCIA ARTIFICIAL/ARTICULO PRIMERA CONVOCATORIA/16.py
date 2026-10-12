"""
Pregunta 16 - Visualizacion 3D interactiva de ell(x), los autovalores del
Hessiano y la constante L_+ = sup_x ell(x), sobre el MISMO terreno de la
pregunta 15: f(x, y) = 0.5 x^2 + 0.25 y^4 - 0.5 y^2.

    ell(x) = max_{1<=j<=d} max(lambda_j(x), 0)      (la mayor curvatura
                                                       POSITIVA en x)
    L_+    = sup_{x en Omega} ell(x)                (constante Lipschitz
                                                       de esa curvatura)

Como el Hessiano de f es diagonal (f_xy = 0), sus autovalores son
directamente las entradas de la diagonal:
    lambda_1(x,y) = f_xx = 1                 (SIEMPRE positivo, constante)
    lambda_2(x,y) = f_yy = 3 y^2 - 1         (negativo cerca de y=0,
                                               positivo lejos de y=0)

La superficie se colorea segun ell(x,y) (mapa de calor), y la superficie
misma sigue siendo f(x,y) para poder comparar directamente con la
pregunta 15.

LEYENDA INTERACTIVA CON PARPADEO (ver graficos_comunes.py): pasa el mouse
sobre una fila de la leyenda y la parte del grafico 3D correspondiente
empieza a parpadear.

Este archivo se puede ejecutar solo (python 16.py) o abrirse como una
pestana dentro de preguntas.py junto con la pregunta 15.

CAMARA CONTROLADA SOLO CON EL MOUSE (igual que en la pregunta 15).

Requisitos:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (necesario para proyeccion 3d)
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from graficos_comunes import LeyendaInteractiva

# =========================================================================
# 1. MISMO TERRENO DE LA PREGUNTA 15
# =========================================================================
def f(x, y):
    return 0.5 * x**2 + 0.25 * y**4 - 0.5 * y**2

def autovalores_hessiano(x, y):
    """Hessiano de f es diagonal (f_xy = 0): los autovalores son las
    propias entradas de la diagonal, f_xx y f_yy."""
    lam1 = np.ones_like(np.asarray(y, dtype=float))
    lam2 = 3 * y**2 - 1
    return lam1, lam2

def ele(x, y):
    """ell(x) = max_j max(lambda_j(x), 0)."""
    lam1, lam2 = autovalores_hessiano(x, y)
    return np.maximum(np.maximum(lam1, 0), np.maximum(lam2, 0))

# =========================================================================
# 2. DOMINIO Omega (el mismo recuadro que en la pregunta 15) y L_+
# =========================================================================
xs = np.linspace(-2, 2, 45)
ys = np.linspace(-1.8, 1.8, 45)
X, Y = np.meshgrid(xs, ys)
Z = f(X, Y)
L_campo = ele(X, Y)

L_plus = float(L_campo.max())
iy_max, ix_max = np.unravel_index(np.argmax(L_campo), L_campo.shape)
punto_Lplus = (float(X[iy_max, ix_max]), float(Y[iy_max, ix_max]), float(Z[iy_max, ix_max]))

lam1_silla, lam2_silla = autovalores_hessiano(0.0, 0.0)
lam1_min, lam2_min = autovalores_hessiano(0.0, 1.0)

# =========================================================================
# 3. VERIFICACION NUMERICA DE LAS 4 OPCIONES DEL EXAMEN
# =========================================================================
print("=" * 70)
print(f"L_+ = sup_x ell(x) sobre Omega = {L_plus:.3f}  "
      f"(se alcanza en el borde, y = {punto_Lplus[1]:.2f})")
print(f"En el punto de silla (0,0): lambda_1={float(lam1_silla):.2f}, "
      f"lambda_2={float(lam2_silla):.2f}  ->  ell(0,0) = {float(ele(0.0, 0.0)):.2f}")
print(f"En un minimo (0,1):        lambda_1={float(lam1_min):.2f}, "
      f"lambda_2={float(lam2_min):.2f}  ->  ell(0,1) = {float(ele(0.0, 1.0)):.2f}")
print(f"lambda_1 (curvatura en x) en TODO Omega = 1.00  (constante y SIEMPRE positiva)")
print("=" * 70)
print("\nVERIFICANDO LAS 4 OPCIONES DE LA PREGUNTA 16:\n")
print("(a) 'Controlar L_+ basta para converger a MINIMOS GLOBALES'        -> FALSO")
print("    (L_+ solo se usa para fijar el paso y evitar sillas; no dice nada de cual minimo)")
print("(b) 'Controlar L_+ evita sillas estrictas, pero no asegura minimo' -> CORRECTO")
print("(c) 'Si L_+ es finito, el Hessiano es negativo definido en Omega'  -> FALSO")
print("    (lambda_1 = 1 > 0 en TODO punto: el Hessiano nunca es negativo definido)")
print("(d) 'L_+ controla solo las direcciones de curvatura negativa'     -> FALSO")
print("    (ell(x) toma el maximo entre TODOS los autovalores positivos, no solo los negativos)")
print("\nCONCLUSION: La opcion CORRECTA es la (b).")
print("=" * 70)

# =========================================================================
# 4. LEYENDA NUMERADA
# =========================================================================
LEYENDA = [
    (1, '#378ADD', 'lambda_1(x) = f_xx = 1',
        'Curvatura en x: CONSTANTE y siempre positiva en todo Omega'),
    (2, '#2FA7A0', 'lambda_2(x) = f_yy = 3y^2 - 1',
        'Curvatura en y: negativa cerca de y=0, positiva lejos'),
    (3, '#7A4FBF', 'ell(x) = max_j max(lambda_j(x), 0)',
        'La mayor curvatura POSITIVA del Hessiano en cada punto'),
    (4, '#D85A30', 'L_+ = sup_x ell(x)',
        f'Cota Lipschitz de esa curvatura en Omega (aqui = {L_plus:.2f})'),
    (5, '#E24B4A', 'Punto de silla (0,0)',
        'lambda_2 < 0 alli, pero ell(0,0)=1 (lo impone lambda_1)'),
    (6, '#639922', 'Minimos (0,1) y (0,-1)',
        'Alli los DOS autovalores son positivos'),
    (7, '#BA7517', 'Paso alpha < 1/L_+',
        'Condicion del teorema para evitar sillas (NO garantiza minimo global)'),
]


def marcador_numero(ax3d, x, y, z, num, color):
    return ax3d.text(x, y, z, f' {num} ', color='white', fontsize=9, fontweight='bold',
                      ha='center', va='center', zorder=10,
                      bbox=dict(boxstyle='circle', facecolor=color, edgecolor='black',
                                linewidth=0.6, pad=0.35))


def construir_figura():
    """Arma toda la figura (grafico 3D + leyenda interactiva) y devuelve
    (fig, anim, leyenda). anim es None aqui (no hay animacion de
    trayectorias en esta pregunta), se devuelve para mantener la misma
    forma de resultado que construir_figura() de la pregunta 15."""

    fig = plt.figure(figsize=(15, 8.5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2.7, 1], wspace=0.05)

    ax = fig.add_subplot(gs[0], projection='3d')
    ax_leyenda = fig.add_subplot(gs[1])

    leyenda = LeyendaInteractiva(fig, ax_leyenda, LEYENDA,
                                  titulo='Terminos de la pregunta 16')

    # ---------------------------------------------------------------
    # SUPERFICIE 3D coloreada segun ell(x, y) (mapa de calor de la
    # curvatura positiva), en vez del cmap de altura de la pregunta 15.
    # ---------------------------------------------------------------
    norm = mcolors.Normalize(vmin=L_campo.min(), vmax=L_campo.max())
    mapa_color = plt.get_cmap('inferno')
    facecolors = mapa_color(norm(L_campo))
    ax.plot_surface(X, Y, Z, facecolors=facecolors, linewidth=0,
                     antialiased=False, shade=False, alpha=0.9,
                     rstride=1, cstride=1)

    mappable = cm.ScalarMappable(norm=norm, cmap=mapa_color)
    mappable.set_array(L_campo)
    fig.colorbar(mappable, ax=ax, shrink=0.55, pad=0.02, label='ell(x, y)')

    # --- Omega: mismo recuadro que en la pregunta 15, solo de contexto ---
    z_base = Z.min() - 0.3
    bx = [-2, 2, 2, -2, -2]
    by = [-1.8, -1.8, 1.8, 1.8, -1.8]
    bz = [z_base] * 5
    ax.plot(bx, by, bz, color='dimgray', linewidth=1.2, linestyle='--', alpha=0.6)

    # --- Minimos y punto de silla, marcados igual que en la pregunta 15 ---
    ax.scatter(0, 1, f(0, 1), color='#639922', s=220, marker='*',
               label='Minimo (0,1)', zorder=6)
    ax.scatter(0, -1, f(0, -1), color='#639922', s=220, marker='*',
               label='Minimo (0,-1)', zorder=6)
    ax.scatter(0, 0, f(0, 0), color='#E24B4A', s=170, marker='X',
               label='Punto de silla (0,0)', zorder=6)

    # --- badges numerados 1-7 sobre el grafico ---
    leyenda.registrar_badge(1, marcador_numero(ax, 1.5, 0.0, f(1.5, 0.0) + 0.2, 1, '#378ADD'))
    leyenda.registrar_badge(2, marcador_numero(ax, 0.0, 1.5, f(0.0, 1.5) + 0.2, 2, '#2FA7A0'))
    leyenda.registrar_badge(3, marcador_numero(ax, -1.4, -1.1, f(-1.4, -1.1) + 0.2, 3, '#7A4FBF'))
    leyenda.registrar_badge(4, marcador_numero(ax, *punto_Lplus[:2],
                                                punto_Lplus[2] + 0.35, 4, '#D85A30'))
    leyenda.registrar_badge(5, marcador_numero(ax, 0.35, 0.0, f(0.35, 0.0) + 0.2, 5, '#E24B4A'))
    leyenda.registrar_badge(6, marcador_numero(ax, 0.35, 1.0, f(0.35, 1.0) + 0.15, 6, '#639922'))
    leyenda.registrar_badge(7, marcador_numero(ax, 2.0, 1.8, z_base + 0.05, 7, '#BA7517'))

    # ---------------------------------------------------------------
    # HALOS: se crean OCULTOS (visible=False) y solo se muestran un
    # instante al parpadear, para no restarle velocidad a la rotacion.
    # ---------------------------------------------------------------
    # (1) lambda_1 constante: 3 cortes del terreno a lo largo de x, en
    #     distintos valores de y. Los 3 tienen exactamente la MISMA
    #     forma de curvatura (solo cambia la altura), mostrando que
    #     lambda_1 no depende de y.
    halos_lam1 = []
    for yf in (-1.5, 0.0, 1.5):
        xs_l = xs
        ys_l = np.full_like(xs_l, yf)
        zs_l = f(xs_l, yf)
        linea, = ax.plot(xs_l, ys_l, zs_l, color='#FFE14D', linewidth=4.5,
                          alpha=0.95, zorder=6, visible=False)
        halos_lam1.append(linea)

    # (2) lambda_2 variable: 3 cortes a lo largo de y, en distintos
    #     valores de x. Los 3 muestran la forma de "doble pozo" (W) cuya
    #     curvatura SI cambia de signo segun donde estes en y.
    halos_lam2 = []
    for xf in (-1.5, 0.0, 1.5):
        ys_l = ys
        xs_l = np.full_like(ys_l, xf)
        zs_l = f(xf, ys_l)
        linea, = ax.plot(xs_l, ys_l, zs_l, color='#2FE0D6', linewidth=4.5,
                          alpha=0.95, zorder=6, visible=False)
        halos_lam2.append(linea)

    # (3) ell(x,y): resaltar toda la superficie (ya coloreada segun ell)
    halo_ell = ax.plot_wireframe(X, Y, Z, color='#7A4FBF', linewidth=0.9,
                                  alpha=0.85, rstride=3, cstride=3, zorder=4,
                                  visible=False)

    # (4) L_+: el borde y=+-1.8 completo (ahi se alcanza el supremo, para
    #     CUALQUIER x, porque ell no depende de x) + un rombo en el punto
    #     exacto donde se calculo el maximo.
    halos_Lplus = []
    for y_borde in (ys.max(), ys.min()):
        zs_b = f(xs, y_borde)
        ys_b = np.full_like(xs, y_borde)
        linea, = ax.plot(xs, ys_b, zs_b, color='#FFE14D', linewidth=6,
                          alpha=0.95, zorder=6, visible=False)
        halos_Lplus.append(linea)
    halo_Lplus_punto = ax.scatter(*punto_Lplus, color='#FFE14D', s=550, marker='D',
                                   alpha=0.95, zorder=7, visible=False)
    halos_Lplus.append(halo_Lplus_punto)

    # (5) punto de silla
    halo_silla = ax.scatter(0, 0, f(0, 0), color='#FFE14D', s=480, marker='X',
                             alpha=0.9, zorder=5, visible=False)

    # (6) minimos
    halo_min1 = ax.scatter(0, 1, f(0, 1), color='#FFE14D', s=650, marker='*',
                            alpha=0.9, zorder=5, visible=False)
    halo_min2 = ax.scatter(0, -1, f(0, -1), color='#FFE14D', s=650, marker='*',
                            alpha=0.9, zorder=5, visible=False)

    # (7) condicion del paso: un cartel de texto con la desigualdad
    halo_paso = fig.text(0.32, 0.93,
                          f'  alpha < 1 / L_+  =  1 / {L_plus:.2f}  ~  {1/L_plus:.3f}  ',
                          fontsize=11, fontweight='bold', color='black',
                          ha='left', va='center', visible=False,
                          bbox=dict(boxstyle='round', facecolor='#FFE14D',
                                    edgecolor='black', linewidth=1.2, alpha=0.95))

    leyenda.registrar_halo(1, halos_lam1)
    leyenda.registrar_halo(2, halos_lam2)
    leyenda.registrar_halo(3, halo_ell)
    leyenda.registrar_halo(4, halos_Lplus)
    leyenda.registrar_halo(5, halo_silla)
    leyenda.registrar_halo(6, [halo_min1, halo_min2])
    leyenda.registrar_halo(7, halo_paso)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y)')
    ax.set_title(
        "Pregunta 16: ell(x), autovalores del Hessiano y L_+ = sup ell(x)\n"
        f"L_+ = {L_plus:.2f}  ->  la respuesta correcta es la (b)\n"
        "(Arrastra con el mouse para rotar la vista; pasa el mouse por la leyenda para identificar cada parte)",
        fontsize=9.5)
    ax.legend(loc='upper left', fontsize=6.8, framealpha=0.9)
    ax.view_init(elev=25, azim=-60)

    leyenda.iniciar_parpadeo()

    return fig, None, leyenda


if __name__ == '__main__':
    fig, anim, leyenda = construir_figura()
    plt.tight_layout()
    plt.show()

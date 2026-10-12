import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle
import matplotlib.transforms as mtransforms

def plot_planes(A, b, sol=None, title="", caso=1):
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Configuración de la malla (optimizada para rendimiento)
    x = np.linspace(-2, 4, 10)
    y = np.linspace(-2, 4, 10)
    X, Y = np.meshgrid(x, y)
    
    # Paleta de colores más didáctica
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Azul, Naranja, Verde
    alphas = [0.35, 0.35, 0.35]
    
    # Dibujar planos
    for i in range(3):
        a = A[i, :]
        b_i = b[i]
        Z = (b_i - a[0]*X - a[1]*Y) / a[2]
        ax.plot_surface(X, Y, Z, alpha=alphas[i], color=colors[i], 
                        edgecolor='none', label=f'Plano {i+1}')
    
    # Configuración visual general
    ax.set_xlabel('X', fontsize=12, labelpad=10)
    ax.set_ylabel('Y', fontsize=12, labelpad=10)
    ax.set_zlabel('Z', fontsize=12, labelpad=10)
    ax.set_title(title, fontsize=14, pad=20, fontweight='bold')
    ax.view_init(elev=25, azim=-60)
    
    # ======================
    # CASO 1: DATOS CON RELACIÓN
    # ======================
    if caso == 1 and sol is not None:
        # Punto de solución destacado con efecto 3D
        ax.scatter(*sol, color='#d62728', s=400, marker='*', 
                  edgecolor='black', linewidth=2, label='Punto de solución')
        
        # Etiqueta con coordenadas y verificación
        ax.text(sol[0]+0.3, sol[1]+0.3, sol[2]+0.3, 
                f'({sol[0]:.1f}, {sol[1]:.1f}, {sol[2]:.1f})', 
                color='darkred', fontsize=14, weight='bold')
        
        # Verificación visual de cada ecuación
        verifications = [
            f"Plano 1: {sol[0]:.1f} + {sol[1]:.1f} + {sol[2]:.1f} = 3 ✓",
            f"Plano 2: {sol[0]:.1f} - {sol[1]:.1f} + 2×{sol[2]:.1f} = 2 ✓",
            f"Plano 3: {sol[1]:.1f} + {sol[2]:.1f} = 2 ✓"
        ]
        
        # Dibujar líneas desde el punto a cada plano
        for i, color in enumerate(colors):
            # Calcular punto en el plano (proyección)
            Z_plane = (b[i] - A[i,0]*sol[0] - A[i,1]*sol[1]) / A[i,2]
            ax.plot([sol[0], sol[0]], [sol[1], sol[1]], [sol[2], Z_plane], 
                    color='darkgray', linestyle='--', linewidth=1.5)
            
            # Añadir etiqueta de verificación
            offset = -0.5 if i == 1 else 0.3
            ax.text(sol[0]+offset, sol[1]+offset, Z_plane-0.2, 
                    verifications[i], color=color, fontsize=11, 
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor=color, boxstyle='round'))
        
        # Añadir panel informativo en la figura
        fig.text(0.15, 0.02, 
                 "CASO 1: DATOS CON RELACIÓN\n"
                 "✓ Los tres planos convergen en un único punto\n"
                 "✓ Existe una solución exacta: (1, 1, 1)\n"
                 "✓ Las ecuaciones son coherentes entre sí\n"
                 "✓ En Machine Learning: Los datos tienen un patrón real y consistente",
                 fontsize=12, 
                 bbox=dict(facecolor='#e6f7ff', alpha=0.7, edgecolor='#1f77b4', boxstyle='round,pad=0.5'),
                 ha='left', va='bottom')
        
        # Añadir icono de ML
        fig.text(0.15, 0.02, "🤖", fontsize=20, ha='left', va='bottom', transform=fig.transFigure)
    
    # ======================
    # CASO 2: DATOS SIN RELACIÓN
    # ======================
    elif caso == 2:
        # Línea de intersección entre plano 1 y 2
        dir_vec = np.cross(A[0], A[1])
        M = np.array([[A[0,0], A[0,1]], [A[1,0], A[1,1]]])
        
        try:
            base_pt = np.linalg.solve(M, [b[0], b[1]])
            point = np.array([base_pt[0], base_pt[1], 0])
        except:
            point = np.array([0, 0, b[0]/A[0,2]])
        
        t = np.linspace(-3, 3, 100)
        line_x = point[0] + t * dir_vec[0]
        line_y = point[1] + t * dir_vec[1]
        line_z = point[2] + t * dir_vec[2]
        
        # Dibujar línea de intersección
        ax.plot(line_x, line_y, line_z, color='black', linewidth=3, 
                label='Línea de intersección\nPlano1 & Plano2')
        
        # Verificar paralelismo con tercer plano
        parallel = np.isclose(np.dot(dir_vec, A[2]), 0)
        if parallel:
            dist = np.abs(np.dot(point, A[2]) - b[2]) / np.linalg.norm(A[2])
            closest_pt = point - (np.dot(point, A[2]) - b[2]) / np.dot(A[2], A[2]) * A[2]
            
            # Flecha de separación
            ax.quiver(point[0], point[1], point[2], 
                      closest_pt[0]-point[0], closest_pt[1]-point[1], closest_pt[2]-point[2],
                      color='red', arrow_length_ratio=0.1, linewidth=2.5)
            
            # Etiqueta explicativa
            ax.text2D(0.05, 0.85, f"¡Contradicción!\nPlano1 + Plano2 = 5\nPero Plano3 = 1", 
                      transform=ax.transAxes, fontsize=14, fontweight='bold',
                      bbox=dict(facecolor='yellow', alpha=0.8, edgecolor='red', boxstyle='round'))
            
            # Añadir explicación visual de la contradicción
            ax.text2D(0.05, 0.75, 
                      "Plano1: x + y + z = 3\n"
                      "Plano2: x - y + 2z = 2\n"
                      "Suma: 2x + 0y + 3z = 5\n\n"
                      "Pero Plano3: 2x + 0y + 3z = 1\n"
                      "¡Imposible!",
                      transform=ax.transAxes, fontsize=12,
                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='red', boxstyle='round'))
            
            # Añadir panel informativo en la figura
            fig.text(0.15, 0.02, 
                     "CASO 2: DATOS SIN RELACIÓN\n"
                     "✗ Los tres planos NO tienen un punto común\n"
                     "✗ Plano3 contradice la suma de Plano1 + Plano2\n"
                     "✗ En Machine Learning: Los datos no tienen un patrón consistente\n"
                     "   (ruido, variables irrelevantes o relaciones contradictorias)",
                     fontsize=12, 
                     bbox=dict(facecolor='#fff7e6', alpha=0.7, edgecolor='#ff7f0e', boxstyle='round,pad=0.5'),
                     ha='left', va='bottom')
            
            # Añadir icono de ML
            fig.text(0.15, 0.02, "⚠️", fontsize=20, ha='left', va='bottom', transform=fig.transFigure)
    
    # Añadir cuadro de leyenda con mejor ubicación
    ax.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # Espacio para el panel informativo
    plt.show()

# ======================
# EJECUCIÓN DE LOS CASOS
# ======================

# CASO 1: DATOS CON RELACIÓN
print("\n" + "="*60)
print("CASO 1: VISUALIZACIÓN DE DATOS CON RELACIÓN (SISTEMA CONSISTENTE)")
print("="*60)
A1 = np.array([[1, 1, 1],
               [1,-1, 2],
               [0, 1, 1]], dtype=float)
b1 = np.array([3, 2, 2], dtype=float)
sol1 = np.linalg.solve(A1, b1)
plot_planes(A1, b1, sol=sol1, 
           title="Caso 1: Datos con Relación - Solución Única en (1.0, 1.0, 1.0)", 
           caso=1)

# CASO 2: DATOS SIN RELACIÓN
print("\n" + "="*60)
print("CASO 2: VISUALIZACIÓN DE DATOS SIN RELACIÓN (SISTEMA INCONSISTENTE)")
print("="*60)
A2 = np.array([[1, 1, 1],
               [1,-1, 2],
               [2, 0, 3]], dtype=float)
b2 = np.array([3, 2, 1], dtype=float)
plot_planes(A2, b2, 
           title="Caso 2: Datos sin Relación - Contradicción en las Ecuaciones", 
           caso=2)
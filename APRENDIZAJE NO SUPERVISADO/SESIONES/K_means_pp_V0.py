# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 18:11:50 2026

@author: jmesc
"""

"""
Generación de tres datasets sintéticos y análisis con K-Means.

Para cada dataset se representa en una única figura con tres subgráficas:

1. Arriba izquierda:
   Datos originales.

2. Arriba derecha:
   Método del codo + coeficiente de silueta.

3. Abajo:
   Resultado final de K-Means con un número de clusters fijado manualmente.
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib.gridspec import GridSpec


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

N_CLUSTERS_REALES = 4      # Número real de clusters generados
N_SAMPLES = 1200           # Número total de muestras
SEPARACION = 8.0           # Separación aproximada entre clusters
RANDOM_STATE = 42

# Rango de K para analizar método del codo y silhouette
K_MIN = 2
K_MAX = 20

# Número de clusters del modelo K-Means
# ESTE VALOR LO ELIGES TÚ MANUALMENTE
K_MODELO = 4


# ============================================================
# 2. FUNCIÓN PARA GENERAR LOS CENTROS
# ============================================================

def generar_centros(n_clusters, separacion):

    if n_clusters == 1:
        return np.array([[0.0, 0.0]])

    radio = separacion / (2 * np.sin(np.pi / n_clusters))

    angulos = np.linspace(
        0,
        2 * np.pi,
        n_clusters,
        endpoint=False
    )

    centros = np.column_stack([
        radio * np.cos(angulos),
        radio * np.sin(angulos)
    ])

    return centros


# ============================================================
# 3. REPARTIR MUESTRAS ENTRE CLUSTERS
# ============================================================

def repartir_muestras(n_samples, n_clusters):

    cantidades = np.full(
        n_clusters,
        n_samples // n_clusters,
        dtype=int
    )

    resto = n_samples % n_clusters
    cantidades[:resto] += 1

    return cantidades


# ============================================================
# 4. DATASET 1 - CLUSTERS CIRCULARES
# ============================================================

def dataset_clusters_redondos(
        n_clusters,
        n_samples,
        separacion,
        random_state):

    centros = generar_centros(
        n_clusters,
        separacion
    )

    X, y = make_blobs(
        n_samples=n_samples,
        centers=centros,
        cluster_std=1.0,
        random_state=random_state
    )

    return X, y


# ============================================================
# 5. DATASET 2 - DIFERENTES FORMAS
# ============================================================

def dataset_diferentes_formas(
        n_clusters,
        n_samples,
        separacion,
        random_state):

    rng = np.random.default_rng(random_state)

    cantidades = repartir_muestras(
        n_samples,
        n_clusters
    )

    centros = generar_centros(
        n_clusters,
        separacion
    )

    X_total = []
    y_total = []

    for k in range(n_clusters):

        n = cantidades[k]
        tipo = k % 4

        # Cluster circular
        if tipo == 0:

            puntos = rng.normal(
                0,
                0.9,
                size=(n, 2)
            )

        # Cluster elíptico
        elif tipo == 1:

            puntos = rng.normal(
                0,
                1,
                size=(n, 2)
            )

            puntos[:, 0] *= 2.8
            puntos[:, 1] *= 0.45

            angulo = np.pi / 4

            R = np.array([
                [np.cos(angulo), -np.sin(angulo)],
                [np.sin(angulo),  np.cos(angulo)]
            ])

            puntos = puntos @ R.T

        # Cluster en anillo
        elif tipo == 2:

            theta = rng.uniform(
                0,
                2 * np.pi,
                n
            )

            radio = rng.normal(
                2.0,
                0.15,
                n
            )

            x = radio * np.cos(theta)
            y = radio * np.sin(theta)

            puntos = np.column_stack([x, y])

        # Cluster parabólico
        else:

            t = rng.uniform(
                -2,
                2,
                n
            )

            x = t
            y = 0.7 * t**2 + rng.normal(0, 0.20, n)

            y -= np.mean(y)

            puntos = np.column_stack([x, y])

        puntos += centros[k]

        X_total.append(puntos)
        y_total.append(np.full(n, k))

    X = np.vstack(X_total)
    y = np.concatenate(y_total)

    return X, y


# ============================================================
# 6. DATASET 3 - DIFERENTES DISTRIBUCIONES Y DENSIDADES
# ============================================================

def dataset_diferentes_distribuciones(
        n_clusters,
        n_samples,
        separacion,
        random_state):

    rng = np.random.default_rng(random_state)

    cantidades = repartir_muestras(
        n_samples,
        n_clusters
    )

    centros = generar_centros(
        n_clusters,
        separacion
    )

    escalas = np.linspace(
        0.35,
        1.60,
        n_clusters
    )

    X_total = []
    y_total = []

    for k in range(n_clusters):

        n = cantidades[k]
        escala = escalas[k]
        tipo = k % 4

        # Normal
        if tipo == 0:

            puntos = rng.normal(
                0,
                escala,
                size=(n, 2)
            )

        # Laplace
        elif tipo == 1:

            puntos = rng.laplace(
                0,
                escala,
                size=(n, 2)
            )

        # t-Student
        elif tipo == 2:

            puntos = rng.standard_t(
                df=3,
                size=(n, 2)
            )

            puntos *= escala

        # Uniforme
        else:

            puntos = rng.uniform(
                -2 * escala,
                2 * escala,
                size=(n, 2)
            )

        puntos += centros[k]

        X_total.append(puntos)
        y_total.append(np.full(n, k))

    X = np.vstack(X_total)
    y = np.concatenate(y_total)

    return X, y


# ============================================================
# 7. FUNCIÓN PRINCIPAL DE ANÁLISIS Y REPRESENTACIÓN
# ============================================================

def analizar_kmeans_y_representar(
        X,
        y_real,
        titulo,
        k_modelo,
        k_min,
        k_max):

    valores_k = list(range(k_min, k_max + 1))

    inercias = []
    siluetas = []

    # --------------------------------------------------------
    # Análisis para varios K
    # --------------------------------------------------------

    for k in valores_k:

        modelo = KMeans(
            n_clusters=k,
            init="k-means++",
            n_init=20,
            random_state=RANDOM_STATE
        )

        labels = modelo.fit_predict(X)

        inercias.append(modelo.inertia_)
        siluetas.append(silhouette_score(X, labels))

    # --------------------------------------------------------
    # Entrenamiento final con el K fijado manualmente
    # --------------------------------------------------------

    modelo_final = KMeans(
        n_clusters=k_modelo,
        init="k-means++",
        n_init=20,
        random_state=RANDOM_STATE
    )

    labels_final = modelo_final.fit_predict(X)
    centroides = modelo_final.cluster_centers_

    # --------------------------------------------------------
    # Mostrar por consola
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)
    print("K utilizado en el modelo:", k_modelo)
    print("Inercia final:", round(modelo_final.inertia_, 4))
    print("Silhouette final:", round(silhouette_score(X, labels_final), 4))

    # --------------------------------------------------------
    # Figura con 3 subgráficas
    # --------------------------------------------------------

    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 1.15])

    ax1 = fig.add_subplot(gs[0, 0])   # arriba izquierda
    ax2 = fig.add_subplot(gs[0, 1])   # arriba derecha
    ax3 = fig.add_subplot(gs[1, :])   # abajo ocupa todo el ancho

    # ========================================================
    # SUBGRÁFICA 1: DATASET ORIGINAL
    # ========================================================

    ax1.scatter(
        X[:, 0],
        X[:, 1],
        c=y_real,
        cmap="tab10",
        s=20,
        alpha=0.7
    )

    ax1.set_title("Datos originales")
    ax1.set_xlabel("Variable X1")
    ax1.set_ylabel("Variable X2")
    ax1.grid(alpha=0.3)
    ax1.axis("equal")

    # ========================================================
    # SUBGRÁFICA 2: CODO + SILUETA
    # ========================================================

    ax2.plot(
        valores_k,
        siluetas,
        "o-",
        linewidth=2,
        label="Coeficiente de Silueta"
    )

    ax2.set_xlabel("Número de clusters K")
    ax2.set_ylabel("Coeficiente de Silueta")
    ax2.set_xticks(valores_k)
    ax2.grid(alpha=0.3)

    # marcar K elegido manualmente
    ax2.axvline(
        k_modelo,
        linestyle=":",
        linewidth=1.8,
        label=f"K elegido = {k_modelo}"
    )

    ax2b = ax2.twinx()

    ax2b.plot(
        valores_k,
        inercias,
        "s--",
        linewidth=2,
        label="Inercia"
    )

    ax2b.set_ylabel("Inercia")

    lineas1, etiquetas1 = ax2.get_legend_handles_labels()
    lineas2, etiquetas2 = ax2b.get_legend_handles_labels()

    ax2.legend(
        lineas1 + lineas2,
        etiquetas1 + etiquetas2,
        loc="best"
    )

    ax2.set_title("Método del codo y coeficiente de silueta")

    # ========================================================
    # SUBGRÁFICA 3: RESULTADO FINAL DE K-MEANS
    # ========================================================

    ax3.scatter(
        X[:, 0],
        X[:, 1],
        c=labels_final,
        cmap="tab10",
        s=25,
        alpha=0.70
    )

    ax3.scatter(
        centroides[:, 0],
        centroides[:, 1],
        marker="X",
        s=280,
        edgecolors="black",
        linewidths=1.5,
        label="Centroides"
    )

    for i, centro in enumerate(centroides):
        ax3.text(
            centro[0],
            centro[1],
            f"  C{i+1}",
            fontsize=11,
            fontweight="bold"
        )

    ax3.set_title(
        f"Resultado final de K-Means con K = {k_modelo}"
    )

    ax3.set_xlabel("Variable X1")
    ax3.set_ylabel("Variable X2")
    ax3.grid(alpha=0.3)
    ax3.axis("equal")
    ax3.legend()

    # ========================================================
    # TÍTULO GENERAL
    # ========================================================

    fig.suptitle(
        titulo,
        fontsize=15,
        fontweight="bold"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()


# ============================================================
# 8. GENERACIÓN DE LOS TRES DATASETS
# ============================================================

X1, y1 = dataset_clusters_redondos(
    N_CLUSTERS_REALES,
    N_SAMPLES,
    SEPARACION,
    RANDOM_STATE
)

X2, y2 = dataset_diferentes_formas(
    N_CLUSTERS_REALES,
    N_SAMPLES,
    SEPARACION,
    RANDOM_STATE
)

X3, y3 = dataset_diferentes_distribuciones(
    N_CLUSTERS_REALES,
    N_SAMPLES,
    SEPARACION,
    RANDOM_STATE
)


# ============================================================
# 9. REPRESENTACIÓN FINAL DE LOS TRES DATASETS
# ============================================================

analizar_kmeans_y_representar(
    X1,
    y1,
    "Dataset 1 - Clusters circulares",
    K_MODELO,
    K_MIN,
    K_MAX
)

analizar_kmeans_y_representar(
    X2,
    y2,
    "Dataset 2 - Diferentes formas",
    K_MODELO,
    K_MIN,
    K_MAX
)

analizar_kmeans_y_representar(
    X3,
    y3,
    "Dataset 3 - Diferentes distribuciones y densidades",
    K_MODELO,
    K_MIN,
    K_MAX
)
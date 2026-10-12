# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:37:33 2026

@author: jmesc
"""


"""
Generación de tres datasets sintéticos para clustering.

Dataset 1:
    Clusters esféricos.

Dataset 2:
    Clusters con diferentes formas geométricas.

Dataset 3:
    Clusters con diferentes distribuciones y densidades.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

N_CLUSTERS = 4          # Número de clusters
N_SAMPLES = 1200        # Número total aproximado de datos
RANDOM_STATE = 42

rng = np.random.default_rng(RANDOM_STATE)


# ============================================================
# FUNCIÓN AUXILIAR PARA REPRESENTAR EN 3D
# ============================================================

def plot_dataset_3d(X, y, title):

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    scatter = ax.scatter(
        X[:, 0],
        X[:, 1],
        X[:, 2],
        c=y,
        s=20,
        alpha=0.7
    )

    ax.set_xlabel("Variable X1")
    ax.set_ylabel("Variable X2")
    ax.set_zlabel("Variable X3")

    ax.set_title(title)

    plt.tight_layout()
    plt.show()


# ============================================================
# DATASET 1
# CLUSTERS ESFÉRICOS / REDONDOS
# ============================================================

def dataset_clusters_redondos(
        n_clusters=4,
        n_samples=1200,
        random_state=42):

    X, y = make_blobs(
        n_samples=n_samples,
        centers=n_clusters,
        n_features=3,
        cluster_std=0.8,
        center_box=(-8, 8),
        random_state=random_state
    )

    return X, y


# ============================================================
# DATASET 2
# CLUSTERS CON DIFERENTES FORMAS
# ============================================================

def dataset_diferentes_formas(
        n_clusters=4,
        n_samples=1200,
        random_state=42):

    rng = np.random.default_rng(random_state)

    puntos_cluster = n_samples // n_clusters

    X_total = []
    y_total = []

    # Posiciones de los clusters
    centros = rng.uniform(
        low=-10,
        high=10,
        size=(n_clusters, 3)
    )

    for k in range(n_clusters):

        n = puntos_cluster

        # Se van repitiendo 5 tipos diferentes de geometría
        tipo = k % 5

        # ----------------------------------------------------
        # TIPO 0: ESFERA
        # ----------------------------------------------------
        if tipo == 0:

            puntos = rng.normal(
                loc=0,
                scale=1,
                size=(n, 3)
            )

        # ----------------------------------------------------
        # TIPO 1: ELIPSOIDE
        # ----------------------------------------------------
        elif tipo == 1:

            puntos = rng.normal(
                size=(n, 3)
            )

            # Escalado diferente en cada eje
            puntos[:, 0] *= 3.0
            puntos[:, 1] *= 0.5
            puntos[:, 2] *= 1.0

        # ----------------------------------------------------
        # TIPO 2: HÉLICE
        # ----------------------------------------------------
        elif tipo == 2:

            t = rng.uniform(
                0,
                4 * np.pi,
                n
            )

            x = 2.0 * np.cos(t)
            y = 2.0 * np.sin(t)
            z = 0.4 * t

            puntos = np.column_stack(
                [x, y, z]
            )

            puntos += rng.normal(
                scale=0.20,
                size=(n, 3)
            )

        # ----------------------------------------------------
        # TIPO 3: ANILLO 3D
        # ----------------------------------------------------
        elif tipo == 3:

            theta = rng.uniform(
                0,
                2 * np.pi,
                n
            )

            radio = rng.normal(
                loc=3,
                scale=0.2,
                size=n
            )

            x = radio * np.cos(theta)
            y = radio * np.sin(theta)
            z = rng.normal(
                scale=0.3,
                size=n
            )

            puntos = np.column_stack(
                [x, y, z]
            )

        # ----------------------------------------------------
        # TIPO 4: PLANO / DISCO
        # ----------------------------------------------------
        else:

            x = rng.uniform(-3, 3, n)
            y = rng.uniform(-3, 3, n)

            z = (
                0.4 * x
                + 0.2 * y
                + rng.normal(scale=0.15, size=n)
            )

            puntos = np.column_stack(
                [x, y, z]
            )

        # Desplazar el cluster a su posición
        puntos += centros[k]

        X_total.append(puntos)

        y_total.append(
            np.full(
                n,
                k
            )
        )

    X = np.vstack(X_total)
    y = np.concatenate(y_total)

    return X, y


# ============================================================
# DATASET 3
# DIFERENTES DISTRIBUCIONES Y DENSIDADES
# ============================================================

def dataset_diferentes_distribuciones(
        n_clusters=4,
        n_samples=1200,
        random_state=42):

    rng = np.random.default_rng(random_state)

    puntos_cluster = n_samples // n_clusters

    X_total = []
    y_total = []

    centros = rng.uniform(
        low=-10,
        high=10,
        size=(n_clusters, 3)
    )

    for k in range(n_clusters):

        n = puntos_cluster

        tipo = k % 4

        # La dispersión cambia según el cluster.
        # Esto produce distintas densidades.
        escala = 0.3 + 0.5 * k

        # ----------------------------------------------------
        # DISTRIBUCIÓN NORMAL
        # ----------------------------------------------------
        if tipo == 0:

            puntos = rng.normal(
                loc=0,
                scale=escala,
                size=(n, 3)
            )

        # ----------------------------------------------------
        # DISTRIBUCIÓN LAPLACE
        # ----------------------------------------------------
        elif tipo == 1:

            puntos = rng.laplace(
                loc=0,
                scale=escala,
                size=(n, 3)
            )

        # ----------------------------------------------------
        # DISTRIBUCIÓN t-STUDENT
        # ----------------------------------------------------
        elif tipo == 2:

            puntos = rng.standard_t(
                df=3,
                size=(n, 3)
            )

            puntos *= escala

        # ----------------------------------------------------
        # DISTRIBUCIÓN UNIFORME
        # ----------------------------------------------------
        else:

            puntos = rng.uniform(
                low=-2 * escala,
                high=2 * escala,
                size=(n, 3)
            )

        puntos += centros[k]

        X_total.append(puntos)

        y_total.append(
            np.full(
                n,
                k
            )
        )

    X = np.vstack(X_total)
    y = np.concatenate(y_total)

    return X, y


# ============================================================
# GENERACIÓN DE LOS TRES DATASETS
# ============================================================

X1, y1 = dataset_clusters_redondos(
    n_clusters=N_CLUSTERS,
    n_samples=N_SAMPLES,
    random_state=RANDOM_STATE
)

X2, y2 = dataset_diferentes_formas(
    n_clusters=N_CLUSTERS,
    n_samples=N_SAMPLES,
    random_state=RANDOM_STATE
)

X3, y3 = dataset_diferentes_distribuciones(
    n_clusters=N_CLUSTERS,
    n_samples=N_SAMPLES,
    random_state=RANDOM_STATE
)


# ============================================================
# REPRESENTACIÓN 3D
# ============================================================

plot_dataset_3d(
    X1,
    y1,
    "Dataset 1 - Clusters esféricos"
)

plot_dataset_3d(
    X2,
    y2,
    "Dataset 2 - Clusters con diferentes formas"
)

plot_dataset_3d(
    X3,
    y3,
    "Dataset 3 - Diferentes distribuciones y densidades"
)


# ============================================================
# INFORMACIÓN DE LOS DATASETS
# ============================================================

print("Dataset 1:")
print("X =", X1.shape)
print("y =", y1.shape)

print("\nDataset 2:")
print("X =", X2.shape)
print("y =", y2.shape)

print("\nDataset 3:")
print("X =", X3.shape)
print("y =", y3.shape)
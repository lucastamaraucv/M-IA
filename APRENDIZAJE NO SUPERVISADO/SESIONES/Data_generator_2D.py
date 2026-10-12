# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:41:45 2026

@author: jmesc
"""

"""
Generación de tres datasets sintéticos para clustering.

Dataset 1:
    Clusters circulares / redondos.

Dataset 2:
    Clusters con diferentes formas geométricas.

Dataset 3:
    Clusters con diferentes distribuciones y densidades.

Todos los datasets tienen dos variables:
    X1, X2
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

N_CLUSTERS = 4          # Número de clusters
N_SAMPLES = 1200        # Número total aproximado de muestras

# Controla la distancia aproximada entre los centros
# Cuanto mayor sea este valor, más separados estarán los clusters
SEPARACION = 8.0

RANDOM_STATE = 42


# ============================================================
# FUNCIÓN PARA GENERAR CENTROS SEPARADOS
# ============================================================

def generar_centros(n_clusters, separacion):
    """
    Genera los centros distribuidos sobre una circunferencia.

    El parámetro separacion controla aproximadamente la distancia
    entre clusters.
    """

    angulos = np.linspace(
        0,
        2 * np.pi,
        n_clusters,
        endpoint=False
    )

    centros = np.column_stack([
        separacion * np.cos(angulos),
        separacion * np.sin(angulos)
    ])

    return centros


# ============================================================
# FUNCIÓN PARA REPRESENTAR LOS DATOS EN 2D
# ============================================================

def plot_dataset_2d(X, y, title):

    plt.figure(figsize=(8, 7))

    scatter = plt.scatter(
        X[:, 0],
        X[:, 1],
        c=y,
        s=25,
        alpha=0.7
    )

    plt.xlabel("Variable X1")
    plt.ylabel("Variable X2")

    plt.title(title)

    plt.grid(alpha=0.3)

    plt.axis("equal")

    plt.tight_layout()

    plt.show()


# ============================================================
# DATASET 1
# CLUSTERS CIRCULARES / REDONDOS
# ============================================================

def dataset_clusters_redondos(
        n_clusters=4,
        n_samples=1200,
        separacion=8.0,
        random_state=42):

    # Generación de los centros
    centros = generar_centros(
        n_clusters,
        separacion
    )

    # Generación de clusters gaussianos circulares
    X, y = make_blobs(
        n_samples=n_samples,
        centers=centros,
        n_features=2,
        cluster_std=1.0,
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
        separacion=8.0,
        random_state=42):

    rng = np.random.default_rng(random_state)

    puntos_cluster = n_samples // n_clusters

    X_total = []
    y_total = []

    # Centros de los clusters
    centros = generar_centros(
        n_clusters,
        separacion
    )

    for k in range(n_clusters):

        n = puntos_cluster

        # Se repiten cuatro tipos de geometría
        tipo = k % 4

        # ----------------------------------------------------
        # TIPO 0: CLUSTER CIRCULAR
        # ----------------------------------------------------

        if tipo == 0:

            puntos = rng.normal(
                loc=0,
                scale=1.0,
                size=(n, 2)
            )

        # ----------------------------------------------------
        # TIPO 1: CLUSTER ELÍPTICO
        # ----------------------------------------------------

        elif tipo == 1:

            puntos = rng.normal(
                loc=0,
                scale=1,
                size=(n, 2)
            )

            # Elongación en X
            puntos[:, 0] *= 3.0
            puntos[:, 1] *= 0.5

            # Rotación del cluster
            angulo = np.pi / 4

            R = np.array([
                [np.cos(angulo), -np.sin(angulo)],
                [np.sin(angulo),  np.cos(angulo)]
            ])

            puntos = puntos @ R.T

        # ----------------------------------------------------
        # TIPO 2: ANILLO
        # ----------------------------------------------------

        elif tipo == 2:

            theta = rng.uniform(
                0,
                2 * np.pi,
                n
            )

            radio = rng.normal(
                loc=2.0,
                scale=0.15,
                size=n
            )

            x = radio * np.cos(theta)
            y = radio * np.sin(theta)

            puntos = np.column_stack([
                x,
                y
            ])

        # ----------------------------------------------------
        # TIPO 3: FORMA CURVA
        # ----------------------------------------------------

        else:

            t = rng.uniform(
                -2,
                2,
                n
            )

            x = t

            y = (
                0.7 * t**2
                + rng.normal(
                    scale=0.25,
                    size=n
                )
            )

            puntos = np.column_stack([
                x,
                y
            ])

            # Centrar aproximadamente la curva
            puntos[:, 1] -= np.mean(
                puntos[:, 1]
            )

        # ----------------------------------------------------
        # DESPLAZAMIENTO AL CENTRO CORRESPONDIENTE
        # ----------------------------------------------------

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
        separacion=8.0,
        random_state=42):

    rng = np.random.default_rng(random_state)

    puntos_cluster = n_samples // n_clusters

    X_total = []
    y_total = []

    centros = generar_centros(
        n_clusters,
        separacion
    )

    for k in range(n_clusters):

        n = puntos_cluster

        # Cambiar distribución según cluster
        tipo = k % 4

        # ----------------------------------------------------
        # La escala controla la dispersión.
        # Al aumentar k, cambia la densidad.
        # ----------------------------------------------------

        escala = 0.4 + 0.4 * k

        # ----------------------------------------------------
        # DISTRIBUCIÓN NORMAL
        # ----------------------------------------------------

        if tipo == 0:

            puntos = rng.normal(
                loc=0,
                scale=escala,
                size=(n, 2)
            )

        # ----------------------------------------------------
        # DISTRIBUCIÓN LAPLACE
        # ----------------------------------------------------

        elif tipo == 1:

            puntos = rng.laplace(
                loc=0,
                scale=escala,
                size=(n, 2)
            )

        # ----------------------------------------------------
        # DISTRIBUCIÓN t-STUDENT
        # ----------------------------------------------------

        elif tipo == 2:

            puntos = rng.standard_t(
                df=3,
                size=(n, 2)
            )

            puntos *= escala

        # ----------------------------------------------------
        # DISTRIBUCIÓN UNIFORME
        # ----------------------------------------------------

        else:

            puntos = rng.uniform(
                low=-2 * escala,
                high=2 * escala,
                size=(n, 2)
            )

        # Desplazar al centro correspondiente
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
    separacion=SEPARACION,
    random_state=RANDOM_STATE
)

X2, y2 = dataset_diferentes_formas(
    n_clusters=N_CLUSTERS,
    n_samples=N_SAMPLES,
    separacion=SEPARACION,
    random_state=RANDOM_STATE
)

X3, y3 = dataset_diferentes_distribuciones(
    n_clusters=N_CLUSTERS,
    n_samples=N_SAMPLES,
    separacion=SEPARACION,
    random_state=RANDOM_STATE
)


# ============================================================
# REPRESENTACIÓN 2D
# ============================================================

plot_dataset_2d(
    X1,
    y1,
    "Dataset 1 - Clusters circulares"
)

plot_dataset_2d(
    X2,
    y2,
    "Dataset 2 - Clusters con diferentes formas"
)

plot_dataset_2d(
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
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 16:46:58 2026

@author: jmesc
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.datasets import make_circles
from sklearn.datasets import make_moons

from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import AffinityPropagation

from sklearn.metrics import silhouette_score
from sklearn.metrics import rand_score


# ============================================================
# PARÁMETROS GENERALES DEL DATASET
# ============================================================

N_POINTS_PER_CLUSTER = 120

# Tipos de clusters que queremos generar
SHAPES = [
    "blob",
    "ring",
    "moon",
    "ellipse"
]

N_CLUSTERS = len(SHAPES)


# ============================================================
# DISPERSIÓN / RUIDO DE CADA TIPO DE CLUSTER
# ============================================================

BLOB_STD = 0.45

RING_NOISE = 0.05

MOON_NOISE = 0.06

ELLIPSE_STD = 0.35


# ============================================================
# TAMAÑO DE LAS FORMAS
# ============================================================

RING_SCALE = 1.4

MOON_SCALE = 1.35

ELLIPSE_SCALE_X = 2.5
ELLIPSE_SCALE_Y = 0.55


# ============================================================
# POSICIÓN DE LOS CLUSTERS
# ============================================================

# Distancia mínima entre centros
MIN_CENTER_DISTANCE = 6.0

# Región donde pueden aparecer aleatoriamente
CENTER_RANGE = (-10, 10)


# ============================================================
# PARÁMETROS DBSCAN
# ============================================================

DBSCAN_EPS = 0.50
DBSCAN_MIN_SAMPLES = 5


# ============================================================
# PARÁMETROS MEAN SHIFT
# ============================================================

MEANSHIFT_QUANTILE = 0.20


# ============================================================
# PARÁMETROS AFFINITY PROPAGATION
# ============================================================

AP_DAMPING = 0.80

# Puedes usar None para dejar que sklearn use
# la mediana de las similitudes.
#
# Con formas muy distintas, Affinity Propagation puede
# dividir una misma geometría en varios ejemplares.
AP_PREFERENCE = None


# ============================================================
# FUNCIÓN PARA GENERAR CENTROS ALEATORIOS
# ============================================================

def generar_centros_aleatorios(
    n_clusters,
    min_distance,
    center_range=(-10, 10),
    max_intentos=10000
):

    centros = []

    minimo, maximo = center_range

    intentos = 0

    while len(centros) < n_clusters:

        nuevo_centro = np.random.uniform(
            minimo,
            maximo,
            size=2
        )

        if len(centros) == 0:

            centros.append(nuevo_centro)

        else:

            distancias = [
                np.linalg.norm(
                    nuevo_centro - centro
                )
                for centro in centros
            ]

            if min(distancias) >= min_distance:

                centros.append(
                    nuevo_centro
                )

        intentos += 1

        if intentos > max_intentos:

            raise RuntimeError(
                "No ha sido posible generar los centros. "
                "Reduce MIN_CENTER_DISTANCE o aumenta CENTER_RANGE."
            )

    return np.array(centros)


# ============================================================
# FUNCIÓN DE ROTACIÓN
# ============================================================

def rotar_puntos(X, angulo_grados):

    angulo = np.radians(
        angulo_grados
    )

    R = np.array([
        [
            np.cos(angulo),
            -np.sin(angulo)
        ],
        [
            np.sin(angulo),
            np.cos(angulo)
        ]
    ])

    return X @ R.T


# ============================================================
# GENERADOR DE UN CLUSTER SEGÚN SU FORMA
# ============================================================

def generar_cluster(
    tipo,
    n_points
):

    # --------------------------------------------------------
    # BLOB
    # --------------------------------------------------------

    if tipo == "blob":

        X_cluster, _ = make_blobs(
            n_samples=n_points,
            centers=[[0, 0]],
            cluster_std=BLOB_STD,
            random_state=None
        )


    # --------------------------------------------------------
    # ANILLO
    # --------------------------------------------------------

    elif tipo == "ring":

        # Generamos dos círculos,
        # pero utilizamos únicamente el exterior.
        X_temp, y_temp = make_circles(
            n_samples=2 * n_points,
            factor=0.45,
            noise=RING_NOISE,
            random_state=None
        )

        X_cluster = X_temp[
            y_temp == 0
        ][:n_points]

        X_cluster *= RING_SCALE


    # --------------------------------------------------------
    # LUNA
    # --------------------------------------------------------

    elif tipo == "moon":

        # make_moons crea dos lunas.
        # Aquí seleccionamos una de ellas para que constituya
        # un único cluster no convexo.
        X_temp, y_temp = make_moons(
            n_samples=2 * n_points,
            noise=MOON_NOISE,
            random_state=None
        )

        X_cluster = X_temp[
            y_temp == 0
        ][:n_points]

        # Centrar la luna en el origen
        X_cluster = (
            X_cluster
            - np.mean(
                X_cluster,
                axis=0
            )
        )

        X_cluster *= MOON_SCALE


    # --------------------------------------------------------
    # ELIPSE
    # --------------------------------------------------------

    elif tipo == "ellipse":

        X_cluster, _ = make_blobs(
            n_samples=n_points,
            centers=[[0, 0]],
            cluster_std=ELLIPSE_STD,
            random_state=None
        )

        transformacion = np.array([
            [ELLIPSE_SCALE_X, 0],
            [0, ELLIPSE_SCALE_Y]
        ])

        X_cluster = (
            X_cluster
            @ transformacion
        )


    else:

        raise ValueError(
            f"Forma no reconocida: {tipo}"
        )


    # --------------------------------------------------------
    # Rotación aleatoria
    # --------------------------------------------------------

    angulo = np.random.uniform(
        0,
        360
    )

    X_cluster = rotar_puntos(
        X_cluster,
        angulo
    )


    return X_cluster


# ============================================================
# GENERAR POSICIONES ALEATORIAS
# ============================================================

centers = generar_centros_aleatorios(
    n_clusters=N_CLUSTERS,
    min_distance=MIN_CENTER_DISTANCE,
    center_range=CENTER_RANGE
)


print(
    "\nCentros utilizados:"
)

print(
    centers
)


# ============================================================
# GENERACIÓN DEL DATASET COMPLETO
# ============================================================

X_lista = []

labels_lista = []


for k, tipo in enumerate(SHAPES):

    X_cluster = generar_cluster(
        tipo,
        N_POINTS_PER_CLUSTER
    )

    # Trasladar el cluster a su posición aleatoria
    X_cluster = (
        X_cluster
        + centers[k]
    )

    X_lista.append(
        X_cluster
    )

    labels_lista.append(
        np.full(
            N_POINTS_PER_CLUSTER,
            k
        )
    )


X = np.vstack(
    X_lista
)

labels_true = np.concatenate(
    labels_lista
)


# ============================================================
# FUNCIÓN PARA SILHOUETTE SCORE
# ============================================================

def calcular_silhouette(
    X,
    labels,
    ignorar_ruido=False
):

    if ignorar_ruido:

        mascara = labels != -1

        X_eval = X[
            mascara
        ]

        labels_eval = labels[
            mascara
        ]

    else:

        X_eval = X

        labels_eval = labels


    clusters = np.unique(
        labels_eval
    )


    if len(clusters) < 2:

        return np.nan


    if len(clusters) >= len(X_eval):

        return np.nan


    return silhouette_score(
        X_eval,
        labels_eval
    )


# ============================================================
# 1. DBSCAN
# ============================================================

dbscan = DBSCAN(
    eps=DBSCAN_EPS,
    min_samples=DBSCAN_MIN_SAMPLES
)

labels_dbscan = dbscan.fit_predict(
    X
)


clusters_dbscan = set(
    labels_dbscan
)

n_clusters_dbscan = len(
    clusters_dbscan
)


if -1 in clusters_dbscan:

    n_clusters_dbscan -= 1


n_noise_dbscan = np.sum(
    labels_dbscan == -1
)


silhouette_dbscan = calcular_silhouette(
    X,
    labels_dbscan,
    ignorar_ruido=True
)


rand_dbscan = rand_score(
    labels_true,
    labels_dbscan
)


# ============================================================
# 2. MEAN SHIFT
# ============================================================

bandwidth = estimate_bandwidth(
    X,
    quantile=MEANSHIFT_QUANTILE,
    n_samples=len(X)
)


meanshift = MeanShift(
    bandwidth=bandwidth,
    bin_seeding=True
)


labels_meanshift = (
    meanshift.fit_predict(X)
)


n_clusters_meanshift = len(
    np.unique(
        labels_meanshift
    )
)


silhouette_meanshift = calcular_silhouette(
    X,
    labels_meanshift
)


rand_meanshift = rand_score(
    labels_true,
    labels_meanshift
)


# ============================================================
# 3. AFFINITY PROPAGATION
# ============================================================

affinity = AffinityPropagation(
    damping=AP_DAMPING,
    preference=AP_PREFERENCE,
    random_state=0
)


labels_affinity = (
    affinity.fit_predict(X)
)


cluster_centers_indices = (
    affinity.cluster_centers_indices_
)


n_clusters_affinity = len(
    cluster_centers_indices
)


silhouette_affinity = calcular_silhouette(
    X,
    labels_affinity
)


rand_affinity = rand_score(
    labels_true,
    labels_affinity
)


# ============================================================
# RESULTADOS POR PANTALLA
# ============================================================

print(
    "\n"
    + "=" * 65
)

print(
    "RESULTADOS DEL CLUSTERING"
)

print(
    "=" * 65
)


print(
    "\nNúmero REAL de clusters:",
    N_CLUSTERS
)


print(
    "Formas reales:",
    SHAPES
)


# ------------------------------------------------------------
# DBSCAN
# ------------------------------------------------------------

print(
    "\n--- DBSCAN ---"
)

print(
    "Número de clusters encontrados:",
    n_clusters_dbscan
)

print(
    "Puntos considerados ruido:",
    n_noise_dbscan
)

print(
    "Silhouette Score:",
    round(
        silhouette_dbscan,
        3
    )
)

print(
    "Rand Index:",
    round(
        rand_dbscan,
        3
    )
)


# ------------------------------------------------------------
# MEAN SHIFT
# ------------------------------------------------------------

print(
    "\n--- MEAN SHIFT ---"
)

print(
    "Bandwidth:",
    round(
        bandwidth,
        3
    )
)

print(
    "Número de clusters encontrados:",
    n_clusters_meanshift
)

print(
    "Silhouette Score:",
    round(
        silhouette_meanshift,
        3
    )
)

print(
    "Rand Index:",
    round(
        rand_meanshift,
        3
    )
)


# ------------------------------------------------------------
# AFFINITY PROPAGATION
# ------------------------------------------------------------

print(
    "\n--- AFFINITY PROPAGATION ---"
)

print(
    "Número de clusters encontrados:",
    n_clusters_affinity
)

print(
    "Silhouette Score:",
    round(
        silhouette_affinity,
        3
    )
)

print(
    "Rand Index:",
    round(
        rand_affinity,
        3
    )
)


print(
    "\n"
    + "=" * 65
)


# ============================================================
# REPRESENTACIÓN GRÁFICA
# ============================================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(14, 12)
)


# ============================================================
# CLUSTERS REALES
# ============================================================

axes[0, 0].scatter(
    X[:, 0],
    X[:, 1],
    c=labels_true,
    cmap="viridis",
    s=28
)


axes[0, 0].scatter(
    centers[:, 0],
    centers[:, 1],
    marker="X",
    s=180,
    c="red",
    edgecolor="black"
)


axes[0, 0].set_title(
    f"Clusters reales\n"
    f"K = {N_CLUSTERS}"
)

axes[0, 0].set_xlabel(
    "Característica 1"
)

axes[0, 0].set_ylabel(
    "Característica 2"
)

axes[0, 0].grid(
    alpha=0.3
)


# ============================================================
# DBSCAN
# ============================================================

axes[0, 1].scatter(
    X[:, 0],
    X[:, 1],
    c=labels_dbscan,
    cmap="viridis",
    s=28
)


mascara_ruido = (
    labels_dbscan == -1
)


axes[0, 1].scatter(
    X[mascara_ruido, 0],
    X[mascara_ruido, 1],
    c="black",
    marker="x",
    s=45
)


axes[0, 1].set_title(
    f"DBSCAN\n"
    f"Clusters = {n_clusters_dbscan} | "
    f"Silhouette = {silhouette_dbscan:.3f} | "
    f"RI = {rand_dbscan:.3f}"
)

axes[0, 1].set_xlabel(
    "Característica 1"
)

axes[0, 1].set_ylabel(
    "Característica 2"
)

axes[0, 1].grid(
    alpha=0.3
)


# ============================================================
# MEAN SHIFT
# ============================================================

axes[1, 0].scatter(
    X[:, 0],
    X[:, 1],
    c=labels_meanshift,
    cmap="viridis",
    s=28
)


centros_meanshift = (
    meanshift.cluster_centers_
)


axes[1, 0].scatter(
    centros_meanshift[:, 0],
    centros_meanshift[:, 1],
    marker="X",
    s=180,
    c="red",
    edgecolor="black"
)


axes[1, 0].set_title(
    f"Mean Shift\n"
    f"Clusters = {n_clusters_meanshift} | "
    f"Silhouette = {silhouette_meanshift:.3f} | "
    f"RI = {rand_meanshift:.3f}"
)

axes[1, 0].set_xlabel(
    "Característica 1"
)

axes[1, 0].set_ylabel(
    "Característica 2"
)

axes[1, 0].grid(
    alpha=0.3
)


# ============================================================
# AFFINITY PROPAGATION
# ============================================================

axes[1, 1].scatter(
    X[:, 0],
    X[:, 1],
    c=labels_affinity,
    cmap="viridis",
    s=28
)


ejemplares = X[
    cluster_centers_indices
]


axes[1, 1].scatter(
    ejemplares[:, 0],
    ejemplares[:, 1],
    marker="*",
    s=300,
    c="red",
    edgecolor="black"
)


axes[1, 1].set_title(
    f"Affinity Propagation\n"
    f"Clusters = {n_clusters_affinity} | "
    f"Silhouette = {silhouette_affinity:.3f} | "
    f"RI = {rand_affinity:.3f}"
)

axes[1, 1].set_xlabel(
    "Característica 1"
)

axes[1, 1].set_ylabel(
    "Característica 2"
)

axes[1, 1].grid(
    alpha=0.3
)


# ============================================================
# AJUSTES FINALES
# ============================================================

plt.tight_layout()

plt.show()
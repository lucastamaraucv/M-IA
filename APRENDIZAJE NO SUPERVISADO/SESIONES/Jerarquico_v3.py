# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:53:22 2026

@author: jmesc
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (
    pairwise_distances,
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score,
)

from scipy.cluster.hierarchy import linkage, dendrogram


# ============================================================
# 1. PARÁMETROS DEL EXPERIMENTO
# ============================================================

N_SAMPLES = 180
N_CLUSTERS = 4

# ------------------------------------------------------------
# Dispersión de los clusters
# ------------------------------------------------------------
# Puede ser un único valor:
CLUSTER_STD = 0.75

# También podría indicarse una dispersión diferente para cada cluster:
# CLUSTER_STD = [0.5, 0.8, 1.0, 0.6]


# ------------------------------------------------------------
# Distancia mínima entre los centros
# ------------------------------------------------------------
MIN_CENTER_DISTANCE = 5.0


# ------------------------------------------------------------
# Semilla aleatoria
# ------------------------------------------------------------
RANDOM_STATE = 7


# ============================================================
# 2. GENERACIÓN DE CENTROS ALEATORIOS
# ============================================================

def generate_random_centers(
    n_clusters,
    min_distance,
    random_state=None,
    max_attempts=100000,
):
    """
    Genera centros bidimensionales aleatorios imponiendo
    una distancia mínima entre cualquier pareja de centros.
    """

    rng = np.random.default_rng(random_state)

    # Región en la que se generan los centros.
    # Aumenta automáticamente con el número de clusters.
    span = min_distance * max(2.0, np.sqrt(n_clusters))

    centers = []

    for _ in range(max_attempts):

        if len(centers) == n_clusters:
            break

        candidate = rng.uniform(
            -span,
            span,
            size=2
        )

        # Se acepta el centro únicamente si respeta
        # la distancia mínima respecto a los anteriores.
        if all(
            np.linalg.norm(candidate - center) >= min_distance
            for center in centers
        ):
            centers.append(candidate)

    if len(centers) != n_clusters:
        raise RuntimeError(
            "No se han podido generar los centros con la "
            "distancia mínima solicitada."
        )

    return np.asarray(centers)


# ============================================================
# 3. FUNCIONES PARA CLUSTERING DIVISIVO
#    DIANA / Macnaughton-Smith
# ============================================================

def cluster_diameter(indices, distance_matrix):
    """
    Calcula el diámetro de un cluster.

    Diámetro =
    máxima distancia entre dos puntos pertenecientes al cluster.
    """

    indices = np.asarray(indices, dtype=int)

    if len(indices) <= 1:
        return 0.0

    submatrix = distance_matrix[
        np.ix_(indices, indices)
    ]

    return float(np.max(submatrix))


# ============================================================

def macnaughton_smith_split(indices, distance_matrix):
    """
    Divide un cluster en dos grupos mediante
    el procedimiento de Macnaughton-Smith.

    Procedimiento:

    1. Se busca el punto cuya disimilitud media con respecto
       al resto del cluster sea máxima.

    2. Ese punto forma inicialmente el SPLINTER GROUP.

    3. Para cada punto restante se calcula:

       delta(i) =

       disimilitud media respecto al grupo restante

                         -

       disimilitud media respecto al splinter group

    4. Si delta(i) > 0, el punto que tenga el mayor delta
       pasa al splinter group.

    5. Se repite hasta que ningún delta sea positivo.
    """

    indices = np.asarray(indices, dtype=int)

    if len(indices) < 2:
        raise ValueError(
            "El cluster debe contener al menos dos puntos."
        )

    # --------------------------------------------------------
    # Submatriz de distancias
    # --------------------------------------------------------

    submatrix = distance_matrix[
        np.ix_(indices, indices)
    ]

    # --------------------------------------------------------
    # Disimilitud media de cada punto respecto al resto
    # --------------------------------------------------------

    mean_dissimilarity = (
        submatrix.sum(axis=1)
        / (len(indices) - 1)
    )

    # --------------------------------------------------------
    # Punto inicial del Splinter Group
    # --------------------------------------------------------

    first_splinter = int(
        indices[
            np.argmax(mean_dissimilarity)
        ]
    )

    splinter = [first_splinter]

    remainder = [
        int(i)
        for i in indices
        if i != first_splinter
    ]

    # --------------------------------------------------------
    # Transferencia de elementos al Splinter Group
    # --------------------------------------------------------

    while len(remainder) > 1:

        best_point = None
        best_delta = 0.0

        for point in remainder:

            other_remainder = [
                j
                for j in remainder
                if j != point
            ]

            # Distancia media al grupo original
            if other_remainder:

                d_remainder = np.mean(
                    [
                        distance_matrix[point, j]
                        for j in other_remainder
                    ]
                )

            else:

                d_remainder = 0.0

            # Distancia media al splinter group
            d_splinter = np.mean(
                [
                    distance_matrix[point, j]
                    for j in splinter
                ]
            )

            # ----------------------------------------------
            # Criterio Macnaughton-Smith
            # ----------------------------------------------

            delta = (
                d_remainder
                - d_splinter
            )

            if delta > best_delta:

                best_delta = delta
                best_point = point

        # Si no existe delta positivo se termina
        if best_point is None:
            break

        remainder.remove(best_point)
        splinter.append(best_point)

    return (
        np.asarray(remainder, dtype=int),
        np.asarray(splinter, dtype=int),
    )


# ============================================================
# 4. ALGORITMO DIVISIVO DIANA
# ============================================================

def divisive_clustering(X, n_clusters):
    """
    Clustering jerárquico divisivo tipo DIANA.

    Se comienza con todos los datos formando un único cluster.

    En cada iteración se selecciona el cluster con mayor
    diámetro y se divide mediante Macnaughton-Smith.
    """

    n_samples = len(X)

    if not 2 <= n_clusters < n_samples:

        raise ValueError(
            "n_clusters debe estar entre 2 y n_samples - 1."
        )

    # --------------------------------------------------------
    # Matriz completa de distancias
    # --------------------------------------------------------

    D = pairwise_distances(
        X,
        metric="euclidean"
    )

    # Inicialmente todos los puntos pertenecen al mismo cluster
    clusters = [
        np.arange(
            n_samples,
            dtype=int
        )
    ]

    # --------------------------------------------------------
    # División sucesiva
    # --------------------------------------------------------

    while len(clusters) < n_clusters:

        # Diámetro de cada cluster existente
        diameters = [
            cluster_diameter(
                cluster,
                D
            )
            for cluster in clusters
        ]

        # DIANA divide el cluster de mayor diámetro
        cluster_to_split = int(
            np.argmax(diameters)
        )

        current_cluster = clusters.pop(
            cluster_to_split
        )

        # División Macnaughton-Smith
        group_1, group_2 = macnaughton_smith_split(
            current_cluster,
            D
        )

        clusters.extend(
            [
                group_1,
                group_2
            ]
        )

    # --------------------------------------------------------
    # Generación del vector de etiquetas
    # --------------------------------------------------------

    labels = np.empty(
        n_samples,
        dtype=int
    )

    for label, cluster in enumerate(clusters):

        labels[cluster] = label

    return labels


# ============================================================
# 5. CONSTRUCCIÓN DEL DENDROGRAMA DIVISIVO
# ============================================================

def divisive_linkage_matrix(X):
    """
    Construye una matriz compatible con:

        scipy.cluster.hierarchy.dendrogram

    para representar gráficamente el árbol divisivo.

    La altura de cada nodo se define como el diámetro
    del cluster antes de realizar la división.
    """

    D = pairwise_distances(
        X,
        metric="euclidean"
    )

    n_samples = len(X)

    linkage_rows = []

    next_cluster_id = n_samples

    # --------------------------------------------------------
    # Construcción recursiva del árbol
    # --------------------------------------------------------

    def build_tree(indices):

        nonlocal next_cluster_id

        indices = np.asarray(
            indices,
            dtype=int
        )

        # ----------------------------------------------------
        # Hoja del árbol
        # ----------------------------------------------------

        if len(indices) == 1:

            return (
                int(indices[0]),
                1,
                0.0
            )

        # ----------------------------------------------------
        # División DIANA
        # ----------------------------------------------------

        left, right = macnaughton_smith_split(
            indices,
            D
        )

        # Construcción de las ramas hijas
        left_id, left_count, left_height = build_tree(
            left
        )

        right_id, right_count, right_height = build_tree(
            right
        )

        # ----------------------------------------------------
        # Altura del nodo
        # ----------------------------------------------------
        # Se utiliza el diámetro del cluster padre.
        # max() garantiza monotonicidad del árbol.

        height = max(
            cluster_diameter(
                indices,
                D
            ),
            left_height,
            right_height
        )

        current_id = next_cluster_id

        next_cluster_id += 1

        # Formato requerido por scipy:
        #
        # [cluster1,
        #  cluster2,
        #  distancia,
        #  número de elementos]

        linkage_rows.append(
            [
                left_id,
                right_id,
                height,
                left_count + right_count
            ]
        )

        return (
            current_id,
            left_count + right_count,
            height
        )

    # Comenzamos con todos los datos
    build_tree(
        np.arange(
            n_samples,
            dtype=int
        )
    )

    return np.asarray(
        linkage_rows,
        dtype=float
    )


# ============================================================
# 6. MÉTRICAS DE EVALUACIÓN
# ============================================================

def clustering_metrics(X, labels):

    return {

        "Silhouette Score":
            silhouette_score(
                X,
                labels
            ),

        "Calinski-Harabasz":
            calinski_harabasz_score(
                X,
                labels
            ),

        "Davies-Bouldin":
            davies_bouldin_score(
                X,
                labels
            )
    }


# ============================================================
# 7. GENERACIÓN DE LOS DATOS SINTÉTICOS
# ============================================================

centers = generate_random_centers(

    n_clusters=N_CLUSTERS,

    min_distance=MIN_CENTER_DISTANCE,

    # --------------------------------------------------------
    # MODIFICACIÓN:
    # Los centros cambian de posición en cada ejecución
    # --------------------------------------------------------
    random_state=None
)


X, y_true = make_blobs(

    n_samples=N_SAMPLES,

    n_features=2,

    centers=centers,

    cluster_std=CLUSTER_STD,

    random_state=RANDOM_STATE
)


# ============================================================
# 8. CLUSTERING JERÁRQUICO AGLOMERATIVO
# ============================================================

agglomerative = AgglomerativeClustering(

    n_clusters=N_CLUSTERS,

    linkage="ward"
)


labels_agg = agglomerative.fit_predict(X)


# ------------------------------------------------------------
# Árbol jerárquico completo para el dendrograma
# ------------------------------------------------------------

Z_agg = linkage(
    X,
    method="ward"
)


# ============================================================
# 9. CLUSTERING JERÁRQUICO DIVISIVO
# ============================================================

labels_div = divisive_clustering(

    X,

    n_clusters=N_CLUSTERS
)


# Árbol completo divisivo
Z_div = divisive_linkage_matrix(X)


# ============================================================
# 10. CÁLCULO DE LAS MÉTRICAS
# ============================================================

metrics_agg = clustering_metrics(
    X,
    labels_agg
)

metrics_div = clustering_metrics(
    X,
    labels_div
)


# ------------------------------------------------------------
# Tabla de resultados
# ------------------------------------------------------------

results = pd.DataFrame(

    [
        metrics_agg,
        metrics_div
    ],

    index=[
        "Aglomerativo (Ward)",
        "Divisivo (DIANA)"
    ]
)


print(
    "\n"
    "================ MÉTRICAS ================"
    "\n"
)

print(
    results.round(4)
)


print("\nInterpretación:")

print(
    "  Silhouette Score  -> cuanto MAYOR, mejor"
)

print(
    "  Calinski-Harabasz -> cuanto MAYOR, mejor"
)

print(
    "  Davies-Bouldin    -> cuanto MENOR, mejor"
)


# ============================================================
# 11. PLOT DE LOS DATOS SINTÉTICOS
# ============================================================

plt.figure(
    figsize=(8, 7)
)


plt.scatter(

    X[:, 0],

    X[:, 1],

    c=y_true,

    cmap="tab10",

    s=35,

    alpha=0.8
)


# Centros reales
plt.scatter(

    centers[:, 0],

    centers[:, 1],

    marker="X",

    s=220,

    edgecolor="black",

    linewidth=1.2,

    label="Centros reales"
)


plt.title(
    "Datos sintéticos generados"
)

plt.xlabel(
    "Característica 1"
)

plt.ylabel(
    "Característica 2"
)

plt.grid(
    alpha=0.25
)

plt.legend()

plt.tight_layout()


# ============================================================
# 12. DENDROGRAMAS EN UNA SOLA FIGURA
# ============================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(16, 6)
)


# ------------------------------------------------------------
# DENDROGRAMA AGLOMERATIVO
# ------------------------------------------------------------

dendrogram(
    Z_agg,
    no_labels=True,
    color_threshold=None,
    ax=axes[0]
)

axes[0].set_title(
    "Dendrograma jerárquico aglomerativo - Ward"
)

axes[0].set_xlabel(
    "Muestras"
)

axes[0].set_ylabel(
    "Distancia de enlace (Ward)"
)

axes[0].grid(
    axis="y",
    alpha=0.25
)


# ------------------------------------------------------------
# DENDROGRAMA DIVISIVO
# ------------------------------------------------------------

dendrogram(
    Z_div,
    no_labels=True,
    color_threshold=None,
    ax=axes[1]
)

axes[1].set_title(
    "Dendrograma jerárquico divisivo - DIANA / Macnaughton-Smith"
)

axes[1].set_xlabel(
    "Muestras"
)

axes[1].set_ylabel(
    "Disimilitud: diámetro del cluster"
)

axes[1].grid(
    axis="y",
    alpha=0.25
)

plt.tight_layout()


# ============================================================
# 13. COMPARACIÓN DE LOS CLUSTERS OBTENIDOS
# ============================================================

fig, axes = plt.subplots(

    1,

    2,

    figsize=(13, 5.5)
)


# ------------------------------------------------------------
# Aglomerativo
# ------------------------------------------------------------

axes[0].scatter(

    X[:, 0],

    X[:, 1],

    c=labels_agg,

    cmap="tab10",

    s=35
)


axes[0].set_title(
    "Clustering aglomerativo - Ward"
)

axes[0].set_xlabel(
    "Característica 1"
)

axes[0].set_ylabel(
    "Característica 2"
)

axes[0].grid(
    alpha=0.25
)


# ------------------------------------------------------------
# Divisivo
# ------------------------------------------------------------

axes[1].scatter(

    X[:, 0],

    X[:, 1],

    c=labels_div,

    cmap="tab10",

    s=35
)


axes[1].set_title(
    "Clustering divisivo - DIANA"
)

axes[1].set_xlabel(
    "Característica 1"
)

axes[1].set_ylabel(
    "Característica 2"
)

axes[1].grid(
    alpha=0.25
)


plt.tight_layout()

plt.show()
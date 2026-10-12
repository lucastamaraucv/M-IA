# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 19:00:47 2026

@author: jmesc
"""

import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import make_moons
from sklearn.cluster import (
    KMeans,
    SpectralClustering,
    AgglomerativeClustering
)


# ============================================================
# FUNCTION TO CALCULATE WCSS
# ============================================================

def calculate_wcss(X, labels):

    wcss = 0.0

    for cluster in np.unique(labels):

        # Points belonging to the cluster
        cluster_points = X[labels == cluster]

        # Cluster centroid
        centroid = np.mean(cluster_points, axis=0)

        # Sum of squared distances to the centroid
        wcss += np.sum(
            (cluster_points - centroid) ** 2
        )

    return wcss


# ============================================================
# FUNCTION TO FIND THE ELBOW AUTOMATICALLY
# ============================================================

def find_elbow(k_values, values):

    k_values = np.array(k_values, dtype=float)
    values = np.array(values, dtype=float)

    # Normalize X axis
    x = (
        (k_values - k_values.min())
        /
        (k_values.max() - k_values.min())
    )

    # Normalize Y axis
    y = (
        (values - values.min())
        /
        (values.max() - values.min())
    )

    # First and last point
    x1, y1 = x[0], y[0]
    x2, y2 = x[-1], y[-1]

    # Distance from every point to the line
    # joining the first and last points
    distances = np.abs(
        (y2 - y1) * x
        -
        (x2 - x1) * y
        +
        x2 * y1
        -
        y2 * x1
    )

    distances = distances / np.sqrt(
        (y2 - y1) ** 2
        +
        (x2 - x1) ** 2
    )

    # Do not allow the first or last point
    # to be selected as the elbow
    distances[0] = 0
    distances[-1] = 0

    elbow_index = np.argmax(distances)

    return int(k_values[elbow_index])


# ============================================================
# 1. GENERATE THE TWO MOONS DATASET
# ============================================================

X, y_true = make_moons(
    n_samples=200,
    noise=0.01,
    random_state=0
)


# ============================================================
# 2. RANGE OF K VALUES
# ============================================================

K_values = range(1, 11)


# Lists to store WCSS
wcss_kmeans = []
wcss_spectral = []
wcss_agglomerative = []


# ============================================================
# 3. CALCULATE WCSS FOR THE THREE ALGORITHMS
# ============================================================

for k in K_values:

    # --------------------------------------------------------
    # K = 1
    # --------------------------------------------------------

    if k == 1:

        labels = np.zeros(
            X.shape[0],
            dtype=int
        )

        initial_wcss = calculate_wcss(
            X,
            labels
        )

        wcss_kmeans.append(initial_wcss)
        wcss_spectral.append(initial_wcss)
        wcss_agglomerative.append(initial_wcss)

        continue


    # --------------------------------------------------------
    # K-MEANS
    # --------------------------------------------------------

    kmeans = KMeans(
        n_clusters=k,
        random_state=0,
        n_init='auto'
    )

    labels_kmeans = kmeans.fit_predict(X)

    # inertia_ is exactly the WCSS
    wcss_kmeans.append(
        kmeans.inertia_
    )


    # --------------------------------------------------------
    # SPECTRAL CLUSTERING
    # --------------------------------------------------------

    spectral = SpectralClustering(
        n_clusters=k,
        affinity='nearest_neighbors',
        n_neighbors=10,
        random_state=0
    )

    labels_spectral = spectral.fit_predict(X)

    wcss_spectral.append(
        calculate_wcss(
            X,
            labels_spectral
        )
    )


    # --------------------------------------------------------
    # AGGLOMERATIVE CLUSTERING
    # --------------------------------------------------------

    agglomerative = AgglomerativeClustering(
        n_clusters=k,
        linkage='ward'
    )

    labels_agglomerative = (
        agglomerative.fit_predict(X)
    )

    wcss_agglomerative.append(
        calculate_wcss(
            X,
            labels_agglomerative
        )
    )


# ============================================================
# 4. FIND THE OPTIMAL K USING THE ELBOW
# ============================================================

k_opt_kmeans = find_elbow(
    K_values,
    wcss_kmeans
)

k_opt_spectral = find_elbow(
    K_values,
    wcss_spectral
)

k_opt_agglomerative = find_elbow(
    K_values,
    wcss_agglomerative
)


# Print results
print(
    "Optimal K - K-Means:",
    k_opt_kmeans
)

print(
    "Optimal K - Spectral Clustering:",
    k_opt_spectral
)

print(
    "Optimal K - Agglomerative Clustering:",
    k_opt_agglomerative
)


# ============================================================
# 5. PLOT THE THREE ELBOW CURVES
# ============================================================

plt.figure(
    figsize=(11, 7)
)


# ------------------------------------------------------------
# K-Means curve
# ------------------------------------------------------------

plt.plot(
    K_values,
    wcss_kmeans,
    marker='o',
    label='K-Means'
)


# ------------------------------------------------------------
# Spectral Clustering curve
# ------------------------------------------------------------

plt.plot(
    K_values,
    wcss_spectral,
    marker='s',
    label='Spectral Clustering'
)


# ------------------------------------------------------------
# Agglomerative Clustering curve
# ------------------------------------------------------------

plt.plot(
    K_values,
    wcss_agglomerative,
    marker='^',
    label='Agglomerative Clustering'
)


# ============================================================
# 6. VERTICAL LINES WITH THE OPTIMAL K
# ============================================================

plt.axvline(
    x=k_opt_kmeans,
    linestyle='--',
    linewidth=2,
    label=f'K-Means optimal K = {k_opt_kmeans}'
)

plt.axvline(
    x=k_opt_spectral,
    linestyle=':',
    linewidth=2,
    label=f'Spectral optimal K = {k_opt_spectral}'
)

plt.axvline(
    x=k_opt_agglomerative,
    linestyle='-.',
    linewidth=2,
    label=f'Agglomerative optimal K = {k_opt_agglomerative}'
)


# ============================================================
# GRAPH FORMAT
# ============================================================

plt.xlabel(
    'Number of clusters (K)',
    fontsize=12
)

plt.ylabel(
    'WCSS',
    fontsize=12
)

plt.title(
    'Elbow Method: Comparison of Clustering Algorithms',
    fontsize=14
)

plt.xticks(K_values)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.tight_layout()

plt.show()
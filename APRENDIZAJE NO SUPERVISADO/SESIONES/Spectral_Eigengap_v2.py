# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:53:22 2026

@author: jmesc
"""

import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import make_moons
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.neighbors import kneighbors_graph

from scipy.sparse.csgraph import laplacian


# ============================================================
# FUNCTION TO ESTIMATE THE NUMBER OF CLUSTERS USING EIGENGAP
# ============================================================

def estimate_clusters_eigengap(X, n_neighbors=10, max_clusters=10):

    # --------------------------------------------------------
    # 1. Construct the KNN graph
    # --------------------------------------------------------

    W = kneighbors_graph(
        X,
        n_neighbors=n_neighbors,
        mode='connectivity',
        include_self=False
    )

    # Make the graph symmetric
    W = W.maximum(W.T)


    # --------------------------------------------------------
    # 2. Calculate the normalized Laplacian matrix
    # --------------------------------------------------------

    L = laplacian(
        W,
        normed=True
    )


    # --------------------------------------------------------
    # 3. Calculate eigenvalues
    # --------------------------------------------------------

    eigenvalues = np.linalg.eigvalsh(
        L.toarray()
    )

    # Sort eigenvalues in ascending order
    eigenvalues = np.sort(eigenvalues)


    # --------------------------------------------------------
    # 4. Calculate Eigengaps
    # --------------------------------------------------------

    # Avoid K = 1 because clustering requires at least
    # two groups in this example
    max_clusters = min(max_clusters, len(eigenvalues) - 1)

    candidate_K = np.arange(
        2,
        max_clusters + 1
    )

    # Gap between lambda_K and lambda_(K+1)
    eigengaps = []

    for K in candidate_K:

        gap = eigenvalues[K] - eigenvalues[K - 1]

        eigengaps.append(gap)

    eigengaps = np.array(eigengaps)


    # --------------------------------------------------------
    # 5. Select K corresponding to the largest Eigengap
    # --------------------------------------------------------

    best_position = np.argmax(eigengaps)

    n_clusters = candidate_K[best_position]


    return n_clusters, eigenvalues, candidate_K, eigengaps


# ============================================================
# 1. GENERATE THE "TWO MOONS" DATASET
# ============================================================

X, y_true = make_moons(
    n_samples=200,
    noise=0.05,
    random_state=0
)


# Number of neighbors used to construct the graph
n_neighbors = 10

# Maximum number of clusters to investigate
max_clusters = 10


# ============================================================
# 2. ESTIMATE THE NUMBER OF CLUSTERS USING EIGENGAP
# ============================================================

n_clusters, eigenvalues, candidate_K, eigengaps = \
    estimate_clusters_eigengap(
        X,
        n_neighbors=n_neighbors,
        max_clusters=max_clusters
    )


print("Estimated number of clusters:", n_clusters)


# ============================================================
# 3. REPRESENT THE EIGENGAP
# ============================================================

plt.figure(figsize=(9, 5))


# Plot first eigenvalues
indices = np.arange(
    1,
    max_clusters + 2
)

plt.plot(
    indices,
    eigenvalues[:max_clusters + 1],
    marker='o'
)


# Draw a vertical line between lambda_K and lambda_(K+1)
plt.axvline(
    x=n_clusters + 0.5,
    color='red',
    linestyle='--',
    linewidth=2,
    label=f'Eigengap -> K = {n_clusters}'
)


plt.xlabel('Eigenvalue index')
plt.ylabel('Eigenvalue')

plt.title(
    'Eigengap Method for Estimating the Number of Clusters'
)

plt.xticks(indices)

plt.grid()

plt.legend()

plt.tight_layout()

plt.show()


# ============================================================
# 4. RUN THE CLUSTERING ALGORITHMS
# ============================================================


# ------------------------------------------------------------
# K-Means
# ------------------------------------------------------------

kmeans = KMeans(
    n_clusters=n_clusters,
    random_state=0,
    n_init='auto'
)

y_kmeans = kmeans.fit_predict(X)


# ------------------------------------------------------------
# Spectral Clustering
# ------------------------------------------------------------

spectral = SpectralClustering(
    n_clusters=n_clusters,
    affinity='nearest_neighbors',
    n_neighbors=n_neighbors,
    random_state=0
)

y_spectral = spectral.fit_predict(X)


# ============================================================
# 5. VISUALIZE THE RESULTS
# ============================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(18, 5)
)


fig.suptitle(
    f'Comparing K-Means and Spectral Clustering '
    f'(Estimated K = {n_clusters})',
    fontsize=16
)


# ------------------------------------------------------------
# Plot K-Means
# ------------------------------------------------------------

axes[0].scatter(
    X[:, 0],
    X[:, 1],
    c=y_kmeans,
    s=50,
    cmap='viridis'
)

axes[0].set_title('K-Means')

axes[0].set_xticks([])
axes[0].set_yticks([])


# ------------------------------------------------------------
# Plot Spectral Clustering
# ------------------------------------------------------------

axes[1].scatter(
    X[:, 0],
    X[:, 1],
    c=y_spectral,
    s=50,
    cmap='viridis'
)

axes[1].set_title('Spectral Clustering')

axes[1].set_xticks([])
axes[1].set_yticks([])


plt.tight_layout()

plt.show()
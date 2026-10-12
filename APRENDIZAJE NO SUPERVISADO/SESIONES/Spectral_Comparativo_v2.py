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
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering

from scipy.cluster.hierarchy import linkage, dendrogram


# 1. Generate the "two moons" dataset
X, y_true = make_moons(n_samples=200, noise=0.05, random_state=0)

# Number of clusters
n_clusters = 2


# ============================================================
# METHOD OF THE ELBOW
# ============================================================

inertias = []

K_values = range(1, 11)

for k in K_values:

    kmeans_elbow = KMeans(
        n_clusters=k,
        random_state=0,
        n_init='auto'
    )

    kmeans_elbow.fit(X)

    inertias.append(kmeans_elbow.inertia_)


# Plot elbow method
plt.figure(figsize=(8, 5))

plt.plot(
    K_values,
    inertias,
    marker='o'
)

plt.axvline(
    x=n_clusters,
    color='red',
    linestyle='--',
    label=f'K = {n_clusters}'
)

plt.xlabel('Number of clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method')

plt.xticks(K_values)

plt.legend()
plt.grid()

plt.tight_layout()
plt.show()


# ============================================================
# HIERARCHICAL CLUSTERING - DENDROGRAM
# ============================================================

# Calculate the linkage matrix
Z = linkage(
    X,
    method='ward'
)





# Plot dendrogram
plt.figure(figsize=(14, 6))

dendrogram(
    Z,
    no_labels=True,
)


plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Samples')
plt.ylabel('Linkage distance')

plt.legend()

plt.tight_layout()
plt.show()


# ============================================================
# RUN THE THREE CLUSTERING ALGORITHMS
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
    random_state=0
)

y_spectral = spectral.fit_predict(X)


# ------------------------------------------------------------
# Agglomerative Hierarchical Clustering
# ------------------------------------------------------------

hierarchical = AgglomerativeClustering(
    n_clusters=n_clusters,
    linkage='ward'
)

y_hierarchical = hierarchical.fit_predict(X)


# ============================================================
# VISUALIZE THE THREE RESULTS
# ============================================================

fig, axes = plt.subplots(
    1,
    3,
    figsize=(18, 5)
)

fig.suptitle(
    'Comparing K-Means, Spectral Clustering and Hierarchical Clustering',
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


# ------------------------------------------------------------
# Plot Hierarchical Clustering
# ------------------------------------------------------------

axes[2].scatter(
    X[:, 0],
    X[:, 1],
    c=y_hierarchical,
    s=50,
    cmap='viridis'
)

axes[2].set_title('Agglomerative Hierarchical Clustering')

axes[2].set_xticks([])
axes[2].set_yticks([])


plt.tight_layout()

plt.show()
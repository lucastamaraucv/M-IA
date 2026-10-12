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

# 1. Generate the "two moons" dataset
X, y_true = make_moons(n_samples=200, noise=0.05, random_state=0)
n_clusters = 2

# --- Run the three algorithms ---

# K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
y_kmeans = kmeans.fit_predict(X)

# Spectral Clustering
spectral = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', random_state=0)
y_spectral = spectral.fit_predict(X)


# --- Visualize the results ---
fig, axes = plt.subplots(1, 2, figsize=(18, 5))
fig.suptitle('Comparing K-Means, Spectral, and Louvain Clustering', fontsize=16)

# Plot K-Means
axes[0].scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
axes[0].set_title(f'K-Means (Failed)')
axes[0].set_xticks([])
axes[0].set_yticks([])

# Plot Spectral Clustering
axes[1].scatter(X[:, 0], X[:, 1], c=y_spectral, s=50, cmap='viridis')
axes[1].set_title(f'Spectral Clustering (Succeeded)')
axes[1].set_xticks([])
axes[1].set_yticks([])




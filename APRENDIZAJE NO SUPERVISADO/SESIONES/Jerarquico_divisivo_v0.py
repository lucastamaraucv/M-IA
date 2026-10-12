# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:04:11 2026

@author: jmesc
"""
# ============================================================
# CLUSTERING JERÁRQUICO DIVISIVO
# ============================================================
#
# Algoritmo:
#   Bisecting K-Means
#
# Scikit-learn:
#   sklearn.cluster.BisectingKMeans
#
# Métricas:
#   - Silhouette Score
#   - Calinski-Harabasz
#   - Davies-Bouldin
#
# Representaciones:
#   1. Dendrograma divisivo
#   2. Clusters originales vs clusters encontrados
#
# ============================================================


import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.cluster import BisectingKMeans

from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)


# ============================================================
# 1. PARÁMETROS DEL PROBLEMA
# ============================================================

# Número total de muestras
N_MUESTRAS = 1500

# Número de clusters
N_CLUSTERS = 4

# Dispersión de los clusters
#
# Valor pequeño -> clusters compactos
# Valor grande  -> clusters más dispersos
DISPERSION = 0.8

# Distancia mínima entre los centros de los clusters
DISTANCIA_MINIMA = 5.0

# Número de características
N_CARACTERISTICAS = 2

# Número de inicializaciones de K-Means
# realizadas en cada división
N_INIT = 10


# ============================================================
# 2. GENERACIÓN ALEATORIA DE LOS CENTROS
# ============================================================

def generar_centros_aleatorios(
        n_clusters,
        distancia_minima,
        n_caracteristicas=2
):
    """
    Genera centros aleatorios garantizando una distancia
    mínima entre ellos.

    Al no utilizar una semilla fija, la posición de los
    clusters cambia cada vez que se ejecuta el programa.
    """

    rng = np.random.default_rng()

    centros = []

    # Tamaño del espacio donde se generan los centros
    rango = max(
        5.0,
        distancia_minima * np.sqrt(n_clusters)
    )

    max_intentos = 100000

    for _ in range(max_intentos):

        # Nuevo centro candidato
        candidato = rng.uniform(
            -rango,
            rango,
            size=n_caracteristicas
        )

        # Si todavía no hay centros, se acepta directamente
        if len(centros) == 0:

            centros.append(candidato)

        else:

            # Distancias entre el nuevo centro y los existentes
            distancias = [
                np.linalg.norm(candidato - centro)
                for centro in centros
            ]

            # Solo se acepta si respeta la distancia mínima
            if min(distancias) >= distancia_minima:
                centros.append(candidato)

        # Cuando tenemos todos los centros terminamos
        if len(centros) == n_clusters:
            return np.array(centros)

    raise RuntimeError(
        "No ha sido posible generar los centros. "
        "Reduce DISTANCIA_MINIMA."
    )


# Generación de los centros
centros = generar_centros_aleatorios(
    N_CLUSTERS,
    DISTANCIA_MINIMA,
    N_CARACTERISTICAS
)


# ============================================================
# 3. GENERACIÓN DE LOS DATOS SINTÉTICOS
# ============================================================

X, y_real = make_blobs(

    n_samples=N_MUESTRAS,

    # Los centros son los generados aleatoriamente
    centers=centros,

    # Número de características
    n_features=N_CARACTERISTICAS,

    # Dispersión
    cluster_std=DISPERSION,

    # Sin semilla fija:
    # datos diferentes en cada ejecución
    random_state=None
)


# ============================================================
# 4. MODELO DE CLUSTERING JERÁRQUICO DIVISIVO
# ============================================================

modelo = BisectingKMeans(

    # Número final de clusters
    n_clusters=10,

    # Inicialización aleatoria
    init="random",

    # Número de intentos en cada división
    n_init=N_INIT,

    # Sin semilla para introducir variabilidad
    random_state=None,

    # Se divide siempre el cluster con mayor SSE
    bisecting_strategy="biggest_inertia"
)


# Entrenamiento del modelo
y_pred = modelo.fit_predict(X)


# ============================================================
# 5. MÉTRICAS DE EVALUACIÓN
# ============================================================

silhouette = silhouette_score(
    X,
    y_pred
)

calinski = calinski_harabasz_score(
    X,
    y_pred
)

davies = davies_bouldin_score(
    X,
    y_pred
)


# ============================================================
# 6. MOSTRAR RESULTADOS
# ============================================================

print("\n" + "=" * 60)

print("CLUSTERING JERÁRQUICO DIVISIVO")

print("=" * 60)

print(f"\nNúmero de muestras: {N_MUESTRAS}")

print(f"Número de clusters: {N_CLUSTERS}")

print(f"Dispersión: {DISPERSION}")

print(
    f"Distancia mínima entre centros: "
    f"{DISTANCIA_MINIMA}"
)

print(
    "Estrategia divisiva: "
    "Bisecting K-Means"
)

print(
    "Criterio de división: "
    "cluster con mayor inercia (SSE)"
)


print("\nMÉTRICAS")

print("-" * 60)

print(
    f"Silhouette Score:        "
    f"{silhouette:.4f}"
)

print(
    f"Calinski-Harabasz:       "
    f"{calinski:.4f}"
)

print(
    f"Davies-Bouldin:          "
    f"{davies:.4f}"
)

print("=" * 60)


# ============================================================
# 7. FUNCIÓN PARA EL DENDROGRAMA DIVISIVO
# ============================================================

def dibujar_dendrograma_divisivo(
        modelo,
        X,
        ax
):
    """
    Representa el árbol divisivo generado por BisectingKMeans.

    El eje vertical representa la inercia (SSE) del cluster
    justo antes de ser dividido.

    El árbol comienza con un único cluster que contiene todos
    los datos y se divide progresivamente hasta alcanzar K
    clusters.
    """

    # --------------------------------------------------------
    # Árbol interno generado por BisectingKMeans
    # --------------------------------------------------------

    if not hasattr(
        modelo,
        "_bisecting_tree"
    ):

        raise AttributeError(
            "Esta versión de scikit-learn no permite acceder "
            "al árbol interno de BisectingKMeans."
        )


    raiz = modelo._bisecting_tree


    # --------------------------------------------------------
    # Obtener las hojas del árbol
    # --------------------------------------------------------

    hojas = list(
        raiz.iter_leaves()
    )


    # Posición horizontal de cada hoja
    posiciones = {
        id(hoja): i
        for i, hoja in enumerate(hojas)
    }


    # Etiquetas de los clusters finales
    etiquetas = {
        id(hoja): f"Cluster {hoja.label + 1}"
        for hoja in hojas
    }


    # --------------------------------------------------------
    # SSE inicial de todos los datos
    # --------------------------------------------------------

    centro_global = np.mean(
        X,
        axis=0
    )

    sse_raiz = np.sum(
        (X - centro_global) ** 2
    )


    # --------------------------------------------------------
    # Función recursiva
    # --------------------------------------------------------

    def recorrer(
            nodo,
            es_raiz=False
    ):

        # ----------------------------------------------------
        # Si es una hoja
        # ----------------------------------------------------

        if (
            nodo.left is None
            and nodo.right is None
        ):

            x = posiciones[id(nodo)]

            return x, 0


        # ----------------------------------------------------
        # Recorrer hijos
        # ----------------------------------------------------

        x_izq, y_izq = recorrer(
            nodo.left
        )

        x_der, y_der = recorrer(
            nodo.right
        )


        # ----------------------------------------------------
        # Altura de la división
        # ----------------------------------------------------

        if es_raiz:

            altura = sse_raiz

        else:

            altura = float(
                nodo.score
            )


        # ----------------------------------------------------
        # Dibujar la división
        # ----------------------------------------------------

        ax.plot(
            [
                x_izq,
                x_izq,
                x_der,
                x_der
            ],
            [
                y_izq,
                altura,
                altura,
                y_der
            ],
            linewidth=1.5
        )


        # Posición del nodo padre
        x_padre = (
            x_izq + x_der
        ) / 2


        return (
            x_padre,
            altura
        )


    # Dibujar todo el árbol
    recorrer(
        raiz,
        es_raiz=True
    )


    # --------------------------------------------------------
    # Configuración del gráfico
    # --------------------------------------------------------

    ax.set_xticks(
        range(len(hojas))
    )

    ax.set_xticklabels(
        [
            etiquetas[id(hoja)]
            for hoja in hojas
        ]
    )


    ax.set_xlabel(
        "Clusters finales"
    )

    ax.set_ylabel(
        "Inercia del cluster (SSE)"
    )

    ax.set_title(
        "Dendrograma divisivo - Bisecting K-Means"
    )

    ax.grid(
        axis="y",
        alpha=0.3
    )


# ============================================================
# 8. REPRESENTACIÓN DEL DENDROGRAMA
# ============================================================

fig, ax = plt.subplots(
    figsize=(11, 6)
)

dibujar_dendrograma_divisivo(
    modelo,
    X,
    ax
)

plt.tight_layout()

plt.show()


# ============================================================
# 9. CLUSTERS ORIGINALES VS CLUSTERS ENCONTRADOS
# ============================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(13, 5)
)


# ============================================================
# CLUSTERS ORIGINALES
# ============================================================

axes[0].scatter(

    X[:, 0],
    X[:, 1],

    c=y_real,

    cmap="tab10",

    s=30,

    alpha=0.8
)


# Centros reales utilizados para generar los datos

axes[0].scatter(

    centros[:, 0],
    centros[:, 1],

    marker="X",

    s=200,

    edgecolors="black",

    linewidths=1.5
)


axes[0].set_title(
    f"Clusters originales\n"
    f"K = {N_CLUSTERS}"
)

axes[0].set_xlabel(
    "Característica 1"
)

axes[0].set_ylabel(
    "Característica 2"
)

axes[0].grid(
    alpha=0.3
)


# ============================================================
# CLUSTERS ENCONTRADOS
# ============================================================

axes[1].scatter(

    X[:, 0],
    X[:, 1],

    c=y_pred,

    cmap="tab10",

    s=30,

    alpha=0.8
)


# Centros obtenidos por Bisecting K-Means

axes[1].scatter(

    modelo.cluster_centers_[:, 0],
    modelo.cluster_centers_[:, 1],

    marker="X",

    s=200,

    edgecolors="black",

    linewidths=1.5
)


axes[1].set_title(

    "Clustering jerárquico divisivo\n"
    f"Silhouette = {silhouette:.3f}"
)

axes[1].set_xlabel(
    "Característica 1"
)

axes[1].set_ylabel(
    "Característica 2"
)

axes[1].grid(
    alpha=0.3
)


# ============================================================
# 10. MISMOS LÍMITES EN AMBAS GRÁFICAS
# ============================================================

xmin = X[:, 0].min()

xmax = X[:, 0].max()

ymin = X[:, 1].min()

ymax = X[:, 1].max()


margen_x = 0.1 * (
    xmax - xmin
)

margen_y = 0.1 * (
    ymax - ymin
)


for ax in axes:

    ax.set_xlim(
        xmin - margen_x,
        xmax + margen_x
    )

    ax.set_ylim(
        ymin - margen_y,
        ymax + margen_y
    )

    ax.set_aspect(
        "equal",
        adjustable="box"
    )


fig.suptitle(

    "Clusters originales vs clustering jerárquico divisivo",

    fontsize=14
)


plt.tight_layout()

plt.show()

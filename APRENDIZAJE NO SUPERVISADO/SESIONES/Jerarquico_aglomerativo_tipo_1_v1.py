# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:01:09 2026

@author: jmesc
"""

# ============================================================
# CLUSTERING JERÁRQUICO AGLOMERATIVO
# ============================================================
# Generación de datos sintéticos + Agglomerative Clustering
#
# Métricas:
#   - Silhouette Score
#   - Calinski-Harabasz
#   - Davies-Bouldin
#
# Representaciones:
#   1. Dendrograma
#   2. Clusters originales vs clusters encontrados
#
# El dendrograma se construye directamente a partir de
# children_ y distances_ de AgglomerativeClustering.
# No se utiliza scipy.
# ============================================================


import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering

from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)


# ============================================================
# 1. PARÁMETROS DEL PROBLEMA
# ============================================================

# Número de muestras
N_MUESTRAS = 500

# Número real de clusters
N_CLUSTERS = 4

# Dispersión de los clusters
# Valores pequeños -> clusters compactos
# Valores grandes  -> clusters más dispersos
DISPERSION = 0.8

# Distancia mínima entre los centros de los clusters
DISTANCIA_MINIMA = 5.0

# Número de características
# En este ejemplo debe mantenerse en 2 para poder representarlo
N_CARACTERISTICAS = 2

# Método de enlace del clustering jerárquico
# Opciones:
#   "ward"
#   "complete"
#   "average"
#   "single"
LINKAGE = "ward"


# ============================================================
# 2. GENERACIÓN ALEATORIA DE LOS CENTROS
# ============================================================

def generar_centros_aleatorios(
        n_clusters,
        distancia_minima,
        n_caracteristicas=2
):
    """
    Genera posiciones aleatorias para los centros de los clusters
    garantizando aproximadamente una distancia mínima entre ellos.

    Los centros son diferentes cada vez que se ejecuta el programa.
    """

    rng = np.random.default_rng()

    centros = []

    # Rango espacial donde se generan los centros.
    # Se adapta automáticamente al número de clusters y a la
    # distancia mínima solicitada.
    rango = distancia_minima * np.sqrt(n_clusters)

    max_intentos = 100000
    intentos = 0

    while len(centros) < n_clusters:

        # Nuevo centro candidato
        candidato = rng.uniform(
            -rango,
            rango,
            size=n_caracteristicas
        )

        # Primer centro
        if len(centros) == 0:
            centros.append(candidato)

        else:

            # Distancias del candidato a los centros existentes
            distancias = [
                np.linalg.norm(candidato - centro)
                for centro in centros
            ]

            # Se acepta únicamente si está suficientemente separado
            if min(distancias) >= distancia_minima:
                centros.append(candidato)

        intentos += 1

        if intentos > max_intentos:
            raise RuntimeError(
                "No ha sido posible generar los centros. "
                "Reduce DISTANCIA_MINIMA o aumenta el rango espacial."
            )

    return np.array(centros)


# Generamos los centros
centros = generar_centros_aleatorios(
    N_CLUSTERS,
    DISTANCIA_MINIMA,
    N_CARACTERISTICAS
)


# ============================================================
# 3. GENERACIÓN DE LOS DATOS SINTÉTICOS
# ============================================================

# No especificamos random_state para que los datos sean diferentes
# cada vez que se ejecuta el programa.

X, y_real = make_blobs(
    n_samples=N_MUESTRAS,
    centers=centros,
    n_features=N_CARACTERISTICAS,
    cluster_std=DISPERSION,
    random_state=None
)


# ============================================================
# 4. MODELO DE CLUSTERING JERÁRQUICO AGLOMERATIVO
# ============================================================

modelo = AgglomerativeClustering(

    # Número de clusters que queremos obtener
    n_clusters=N_CLUSTERS,

    # Método de enlace
    linkage=LINKAGE,

    # Obliga a calcular el árbol jerárquico completo
    compute_full_tree=True,

    # Guarda las distancias entre las fusiones.
    # Necesario para representar el dendrograma.
    compute_distances=True
)


# Entrenamiento del modelo
y_pred = modelo.fit_predict(X)


# ============================================================
# CENTROIDES DE LOS CLUSTERS ENCONTRADOS
# ============================================================

centroides_encontrados = np.array([
    X[y_pred == cluster].mean(axis=0)
    for cluster in range(N_CLUSTERS)
])


# ============================================================
# 5. MÉTRICAS DE EVALUACIÓN
# ============================================================

silhouette = silhouette_score(X, y_pred)

calinski = calinski_harabasz_score(X, y_pred)

davies = davies_bouldin_score(X, y_pred)


print("\n" + "=" * 55)
print("RESULTADOS DEL CLUSTERING JERÁRQUICO")
print("=" * 55)

print(f"\nNúmero de muestras: {N_MUESTRAS}")
print(f"Número de clusters: {N_CLUSTERS}")
print(f"Dispersión: {DISPERSION}")
print(f"Distancia mínima entre centros: {DISTANCIA_MINIMA}")
print(f"Método de enlace: {LINKAGE}")

print("\nMÉTRICAS")
print("-" * 55)

print(f"Silhouette Score:        {silhouette:.4f}")
print(f"Calinski-Harabasz:       {calinski:.4f}")
print(f"Davies-Bouldin:          {davies:.4f}")

print("=" * 55)


# ============================================================
# 6. FUNCIÓN PARA REPRESENTAR EL DENDROGRAMA
# ============================================================

def dibujar_dendrograma(modelo, ax, n_clusters=None):
    """
    Construye un dendrograma directamente a partir de la
    información proporcionada por AgglomerativeClustering.

    No utiliza scipy.

    Parameters
    ----------
    modelo:
        Modelo AgglomerativeClustering entrenado.

    ax:
        Eje de matplotlib donde se dibuja el dendrograma.

    n_clusters:
        Número de clusters utilizado. Si se proporciona,
        se representa también la altura aproximada de corte.
    """

    children = modelo.children_
    distances = modelo.distances_

    n_muestras = modelo.n_leaves_

    # --------------------------------------------------------
    # Obtener el orden de las hojas del árbol
    # --------------------------------------------------------

    def obtener_hojas(nodo):

        # Si el nodo corresponde a una muestra original
        if nodo < n_muestras:
            return [nodo]

        # Índice de la fusión
        indice = nodo - n_muestras

        hijo_izq = children[indice, 0]
        hijo_der = children[indice, 1]

        return (
            obtener_hojas(hijo_izq)
            + obtener_hojas(hijo_der)
        )

    # El último nodo creado es la raíz del árbol
    nodo_raiz = n_muestras + len(children) - 1

    orden_hojas = obtener_hojas(nodo_raiz)

    # Coordenada X de cada muestra
    posicion_x = {
        hoja: i
        for i, hoja in enumerate(orden_hojas)
    }


    # --------------------------------------------------------
    # Representación recursiva del árbol
    # --------------------------------------------------------

    def dibujar_nodo(nodo):

        # ---------------------------------------
        # Nodo hoja
        # ---------------------------------------

        if nodo < n_muestras:

            return posicion_x[nodo], 0


        # ---------------------------------------
        # Nodo interno
        # ---------------------------------------

        indice = nodo - n_muestras

        hijo_izq = children[indice, 0]
        hijo_der = children[indice, 1]

        # Coordenadas de los hijos
        x_izq, y_izq = dibujar_nodo(hijo_izq)
        x_der, y_der = dibujar_nodo(hijo_der)

        # Altura de esta unión
        altura = distances[indice]

        # Dibujar forma de U
        ax.plot(
            [x_izq, x_izq, x_der, x_der],
            [y_izq, altura, altura, y_der],
            linewidth=1
        )

        # Posición horizontal del nuevo nodo
        x_nuevo = (x_izq + x_der) / 2

        return x_nuevo, altura


    # Dibujar desde la raíz
    dibujar_nodo(nodo_raiz)


    # --------------------------------------------------------
    # Línea aproximada correspondiente al corte en K clusters
    # --------------------------------------------------------

    if n_clusters is not None and n_clusters > 1:

        indice_inferior = n_muestras - n_clusters - 1
        indice_superior = n_muestras - n_clusters

        if (
            indice_inferior >= 0
            and indice_superior < len(distances)
        ):

            altura_corte = (
                distances[indice_inferior]
                + distances[indice_superior]
            ) / 2

            ax.axhline(
                y=altura_corte,
                linestyle="--",
                linewidth=1.5,
                label=f"Corte K = {n_clusters}"
            )

            ax.legend()


    # --------------------------------------------------------
    # Configuración de la gráfica
    # --------------------------------------------------------

    ax.set_title(
        f"Dendrograma - Clustering jerárquico ({LINKAGE})"
    )

    ax.set_xlabel("Muestras")
    ax.set_ylabel("Distancia de fusión")

    ax.set_xticks([])

    ax.grid(
        axis="y",
        alpha=0.3
    )


# ============================================================
# 7. REPRESENTACIÓN DEL DENDROGRAMA
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 6)
)

dibujar_dendrograma(
    modelo,
    ax,
    n_clusters=N_CLUSTERS
)

plt.tight_layout()
plt.show()


# ============================================================
# 8. CLUSTERS ORIGINALES VS CLUSTERS ENCONTRADOS
# ============================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(13, 5)
)


# ------------------------------------------------------------
# Clusters originales
# ------------------------------------------------------------

axes[0].scatter(
    X[:, 0],
    X[:, 1],
    c=y_real,
    cmap="tab10",
    s=30,
    alpha=0.8
)

# Centros originales utilizados para generar los datos
axes[0].scatter(
    centros[:, 0],
    centros[:, 1],
    marker="X",
    s=200,
    edgecolors="black",
    linewidths=1.5
)

axes[0].set_title(
    f"Clusters originales\nK = {N_CLUSTERS}"
)

axes[0].set_xlabel("Característica 1")
axes[0].set_ylabel("Característica 2")

axes[0].grid(alpha=0.3)


# ------------------------------------------------------------
# Clusters encontrados
# ------------------------------------------------------------

axes[1].scatter(
    X[:, 0],
    X[:, 1],
    c=y_pred,
    cmap="tab10",
    s=30,
    alpha=0.8
)


# ------------------------------------------------------------
# Centroides de los clusters encontrados
# ------------------------------------------------------------

axes[1].scatter(
    centroides_encontrados[:, 0],
    centroides_encontrados[:, 1],
    marker="X",
    s=200,
    edgecolors="black",
    linewidths=1.5,
    label="Centroides"
)

axes[1].legend()


axes[1].set_title(
    "Agglomerative Clustering\n"
    f"Silhouette = {silhouette:.3f}"
)

axes[1].set_xlabel("Característica 1")
axes[1].set_ylabel("Característica 2")

axes[1].grid(alpha=0.3)


# ------------------------------------------------------------
# Mismos límites en ambos gráficos
# ------------------------------------------------------------

xmin = X[:, 0].min()
xmax = X[:, 0].max()

ymin = X[:, 1].min()
ymax = X[:, 1].max()

margen_x = 0.1 * (xmax - xmin)
margen_y = 0.1 * (ymax - ymin)

for ax in axes:

    ax.set_xlim(
        xmin - margen_x,
        xmax + margen_x
    )

    ax.set_ylim(
        ymin - margen_y,
        ymax + margen_y
    )

    # Misma escala en X e Y
    ax.set_aspect(
        "equal",
        adjustable="box"
    )


fig.suptitle(
    "Comparación entre los clusters reales y los encontrados",
    fontsize=14
)

plt.tight_layout()
plt.show()

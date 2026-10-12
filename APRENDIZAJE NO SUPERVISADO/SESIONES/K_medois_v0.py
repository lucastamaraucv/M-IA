# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 18:49:32 2026

@author: jmesc
"""

"""
Generación de tres datasets sintéticos y análisis mediante K-Medoids.

Modelo utilizado:
    kmedoids.fasterpam()

Para cada dataset se representa:

1. Arriba izquierda:
   Datos originales.

2. Arriba derecha:
   Método del codo + coeficiente de silueta.

3. Abajo:
   Resultado final de K-Medoids y posición de los medoides.

El número de clusters final K_MODELO se introduce manualmente.
"""

import numpy as np
import matplotlib.pyplot as plt
import kmedoids

from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
from sklearn.metrics import pairwise_distances

from matplotlib.gridspec import GridSpec


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

N_CLUSTERS_REALES = 4      # Número real de clusters generados
N_SAMPLES = 1200           # Número total de muestras

# Separación aproximada entre clusters
SEPARACION = 8.0

RANDOM_STATE = 42

# ------------------------------------------------------------
# Valores de K que se estudiarán con:
#   - método del codo
#   - coeficiente de silueta
# ------------------------------------------------------------

K_MIN = 2
K_MAX = 8

# ------------------------------------------------------------
# Número de clusters que queremos utilizar finalmente.
#
# NO se calcula automáticamente.
# Lo elige el usuario después de observar las gráficas.
# ------------------------------------------------------------

K_MODELO = 4


# ============================================================
# 2. GENERACIÓN DE CENTROS
# ============================================================

def generar_centros(n_clusters, separacion):

    if n_clusters == 1:

        return np.array([
            [0.0, 0.0]
        ])

    # Radio necesario para obtener aproximadamente
    # la separación indicada entre centros consecutivos
    radio = separacion / (
        2 * np.sin(np.pi / n_clusters)
    )

    angulos = np.linspace(
        0,
        2 * np.pi,
        n_clusters,
        endpoint=False
    )

    centros = np.column_stack([

        radio * np.cos(angulos),

        radio * np.sin(angulos)

    ])

    return centros


# ============================================================
# 3. REPARTIR MUESTRAS ENTRE LOS CLUSTERS
# ============================================================

def repartir_muestras(
        n_samples,
        n_clusters):

    cantidades = np.full(
        n_clusters,
        n_samples // n_clusters,
        dtype=int
    )

    resto = (
        n_samples
        % n_clusters
    )

    cantidades[:resto] += 1

    return cantidades


# ============================================================
# 4. DATASET 1
# CLUSTERS CIRCULARES
# ============================================================

def dataset_clusters_redondos(
        n_clusters,
        n_samples,
        separacion,
        random_state):

    centros = generar_centros(
        n_clusters,
        separacion
    )

    X, y = make_blobs(

        n_samples=n_samples,

        centers=centros,

        cluster_std=1.0,

        random_state=random_state
    )

    return X, y


# ============================================================
# 5. DATASET 2
# CLUSTERS CON DIFERENTES FORMAS
# ============================================================

def dataset_diferentes_formas(
        n_clusters,
        n_samples,
        separacion,
        random_state):

    rng = np.random.default_rng(
        random_state
    )

    cantidades = repartir_muestras(
        n_samples,
        n_clusters
    )

    centros = generar_centros(
        n_clusters,
        separacion
    )

    X_total = []
    y_total = []

    for k in range(n_clusters):

        n = cantidades[k]

        tipo = k % 4

        # ====================================================
        # TIPO 0
        # CLUSTER CIRCULAR
        # ====================================================

        if tipo == 0:

            puntos = rng.normal(

                loc=0,

                scale=0.9,

                size=(n, 2)
            )

        # ====================================================
        # TIPO 1
        # CLUSTER ELÍPTICO
        # ====================================================

        elif tipo == 1:

            puntos = rng.normal(

                loc=0,

                scale=1,

                size=(n, 2)
            )

            puntos[:, 0] *= 2.8
            puntos[:, 1] *= 0.45

            angulo = np.pi / 4

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

            puntos = puntos @ R.T

        # ====================================================
        # TIPO 2
        # CLUSTER CON FORMA DE ANILLO
        # ====================================================

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

            x = (
                radio
                * np.cos(theta)
            )

            y = (
                radio
                * np.sin(theta)
            )

            puntos = np.column_stack([
                x,
                y
            ])

        # ====================================================
        # TIPO 3
        # CLUSTER PARABÓLICO
        # ====================================================

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

                    loc=0,

                    scale=0.20,

                    size=n
                )
            )

            # Centrar aproximadamente
            y -= np.mean(y)

            puntos = np.column_stack([
                x,
                y
            ])

        # ----------------------------------------------------
        # Desplazar el cluster
        # ----------------------------------------------------

        puntos += centros[k]

        X_total.append(
            puntos
        )

        y_total.append(
            np.full(
                n,
                k
            )
        )

    X = np.vstack(
        X_total
    )

    y = np.concatenate(
        y_total
    )

    return X, y


# ============================================================
# 6. DATASET 3
# DIFERENTES DISTRIBUCIONES Y DENSIDADES
# ============================================================

def dataset_diferentes_distribuciones(
        n_clusters,
        n_samples,
        separacion,
        random_state):

    rng = np.random.default_rng(
        random_state
    )

    cantidades = repartir_muestras(
        n_samples,
        n_clusters
    )

    centros = generar_centros(
        n_clusters,
        separacion
    )

    # Diferentes dispersiones:
    # distintos niveles de densidad
    escalas = np.linspace(
        0.35,
        1.60,
        n_clusters
    )

    X_total = []
    y_total = []

    for k in range(n_clusters):

        n = cantidades[k]

        escala = escalas[k]

        tipo = k % 4

        # ====================================================
        # DISTRIBUCIÓN NORMAL
        # ====================================================

        if tipo == 0:

            puntos = rng.normal(

                loc=0,

                scale=escala,

                size=(n, 2)
            )

        # ====================================================
        # DISTRIBUCIÓN LAPLACE
        # ====================================================

        elif tipo == 1:

            puntos = rng.laplace(

                loc=0,

                scale=escala,

                size=(n, 2)
            )

        # ====================================================
        # DISTRIBUCIÓN t-STUDENT
        # ====================================================

        elif tipo == 2:

            puntos = rng.standard_t(

                df=3,

                size=(n, 2)
            )

            puntos *= escala

        # ====================================================
        # DISTRIBUCIÓN UNIFORME
        # ====================================================

        else:

            puntos = rng.uniform(

                low=-2 * escala,

                high=2 * escala,

                size=(n, 2)
            )

        # ----------------------------------------------------
        # Trasladar cluster
        # ----------------------------------------------------

        puntos += centros[k]

        X_total.append(
            puntos
        )

        y_total.append(
            np.full(
                n,
                k
            )
        )

    X = np.vstack(
        X_total
    )

    y = np.concatenate(
        y_total
    )

    return X, y


# ============================================================
# 7. ANÁLISIS MEDIANTE K-MEDOIDS
# ============================================================

def analizar_kmedoids_y_representar(
        X,
        y_real,
        titulo,
        k_modelo,
        k_min=2,
        k_max=8):

    # ========================================================
    # MATRIZ DE DISTANCIAS
    # ========================================================
    #
    # K-Medoids trabaja con distancias entre los puntos.
    #
    # La calculamos SOLO UNA VEZ y después la reutilizamos
    # para todos los valores de K.
    #
    # ========================================================

    matriz_distancias = pairwise_distances(
        X,
        metric="euclidean"
    )

    # ========================================================
    # VALORES DE K A ESTUDIAR
    # ========================================================

    valores_k = list(
        range(
            k_min,
            k_max + 1
        )
    )

    costes = []
    siluetas = []

    # ========================================================
    # ENTRENAMIENTO PARA DIFERENTES VALORES DE K
    # ========================================================

    for k in valores_k:

        # ----------------------------------------------------
        # K-MEDOIDS MEDIANTE FasterPAM
        # ----------------------------------------------------

        resultado = kmedoids.fasterpam(

            matriz_distancias,

            k,

            init="build",

            random_state=RANDOM_STATE
        )

        # ----------------------------------------------------
        # Etiqueta de cluster de cada dato
        # ----------------------------------------------------

        labels = resultado.labels

        # ----------------------------------------------------
        # FUNCIÓN DE COSTE
        #
        # En K-Medoids:
        #
        # suma de distancias de los puntos a sus medoides.
        #
        # Se utiliza para construir la curva del codo.
        # ----------------------------------------------------

        costes.append(
            resultado.loss
        )

        # ----------------------------------------------------
        # COEFICIENTE DE SILUETA
        # ----------------------------------------------------

        silueta = silhouette_score(
            X,
            labels,
            metric="euclidean"
        )

        siluetas.append(
            silueta
        )


    # ========================================================
    # ENTRENAMIENTO FINAL CON EL K ELEGIDO MANUALMENTE
    # ========================================================

    resultado_final = kmedoids.fasterpam(

        matriz_distancias,

        k_modelo,

        init="build",

        random_state=RANDOM_STATE
    )

    # --------------------------------------------------------
    # Etiquetas finales
    # --------------------------------------------------------

    labels_final = (
        resultado_final.labels
    )

    # --------------------------------------------------------
    # Índices de los medoides
    # --------------------------------------------------------

    indices_medoides = (
        resultado_final.medoids
    )

    # --------------------------------------------------------
    # Coordenadas de los medoides
    # --------------------------------------------------------

    medoides = X[
        indices_medoides
    ]


    # ========================================================
    # INFORMACIÓN POR CONSOLA
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(titulo)

    print(
        "=" * 70
    )

    print(
        "Modelo: K-Medoids - FasterPAM"
    )

    print(
        "K utilizado:",
        k_modelo
    )

    print(
        "Coste final:",
        round(
            resultado_final.loss,
            4
        )
    )

    silueta_final = silhouette_score(

        X,

        labels_final
    )

    print(
        "Coeficiente de Silueta:",
        round(
            silueta_final,
            4
        )
    )

    print(
        "Índices de los medoides:",
        indices_medoides
    )

    print(
        "Coordenadas de los medoides:"
    )

    print(
        medoides
    )


    # ========================================================
    # CREAR FIGURA CON TRES SUBGRÁFICAS
    # ========================================================

    fig = plt.figure(
        figsize=(14, 10)
    )

    gs = GridSpec(

        2,
        2,

        figure=fig,

        height_ratios=[
            1,
            1.15
        ]
    )

    # --------------------------------------------------------
    # Arriba izquierda
    # --------------------------------------------------------

    ax1 = fig.add_subplot(
        gs[0, 0]
    )

    # --------------------------------------------------------
    # Arriba derecha
    # --------------------------------------------------------

    ax2 = fig.add_subplot(
        gs[0, 1]
    )

    # --------------------------------------------------------
    # Parte inferior
    # ocupa todo el ancho
    # --------------------------------------------------------

    ax3 = fig.add_subplot(
        gs[1, :]
    )


    # ========================================================
    # SUBGRÁFICA 1
    # DATOS ORIGINALES
    # ========================================================

    ax1.scatter(

        X[:, 0],

        X[:, 1],

        c=y_real,

        cmap="tab10",

        s=20,

        alpha=0.7
    )

    ax1.set_title(
        "Datos originales"
    )

    ax1.set_xlabel(
        "Variable X1"
    )

    ax1.set_ylabel(
        "Variable X2"
    )

    ax1.grid(
        alpha=0.3
    )

    ax1.axis(
        "equal"
    )


    # ========================================================
    # SUBGRÁFICA 2
    #
    # SILUETA + MÉTODO DEL CODO
    # ========================================================

    # --------------------------------------------------------
    # EJE IZQUIERDO
    # COEFICIENTE DE SILUETA
    # --------------------------------------------------------

    ax2.plot(

        valores_k,

        siluetas,

        "o-",

        linewidth=2,

        label="Coeficiente de Silueta"
    )

    ax2.set_xlabel(
        "Número de clusters K"
    )

    ax2.set_ylabel(
        "Coeficiente de Silueta"
    )

    ax2.set_xticks(
        valores_k
    )

    ax2.grid(
        alpha=0.3
    )

    # --------------------------------------------------------
    # Marcar el K escogido manualmente
    # --------------------------------------------------------

    ax2.axvline(

        k_modelo,

        linestyle=":",

        linewidth=1.8,

        label=f"K elegido = {k_modelo}"
    )


    # ========================================================
    # EJE DERECHO
    # FUNCIÓN DE COSTE DE K-MEDOIDS
    # ========================================================

    ax2b = ax2.twinx()

    ax2b.plot(

        valores_k,

        costes,

        "s--",

        linewidth=2,

        label="Coste K-Medoids"
    )

    ax2b.set_ylabel(
        "Coste K-Medoids"
    )


    # ========================================================
    # LEYENDA CONJUNTA
    # ========================================================

    lineas1, etiquetas1 = (
        ax2.get_legend_handles_labels()
    )

    lineas2, etiquetas2 = (
        ax2b.get_legend_handles_labels()
    )

    ax2.legend(

        lineas1 + lineas2,

        etiquetas1 + etiquetas2,

        loc="best"
    )

    ax2.set_title(
        "Método del codo y coeficiente de silueta"
    )


    # ========================================================
    # SUBGRÁFICA 3
    #
    # RESULTADO FINAL K-MEDOIDS
    # ========================================================

    ax3.scatter(

        X[:, 0],

        X[:, 1],

        c=labels_final,

        cmap="tab10",

        s=25,

        alpha=0.70
    )


    # ========================================================
    # REPRESENTAR LOS MEDOIDES
    # ========================================================

    ax3.scatter(

        medoides[:, 0],

        medoides[:, 1],

        marker="X",

        s=300,

        edgecolors="black",

        linewidths=1.5,

        label="Medoides"
    )


    # ========================================================
    # ETIQUETAR MEDOIDES
    # ========================================================

    for i, medoide in enumerate(
            medoides):

        ax3.text(

            medoide[0],

            medoide[1],

            f"  M{i + 1}",

            fontsize=11,

            fontweight="bold"
        )


    ax3.set_title(

        f"Resultado final de K-Medoids "
        f"(FasterPAM) con K = {k_modelo}"
    )

    ax3.set_xlabel(
        "Variable X1"
    )

    ax3.set_ylabel(
        "Variable X2"
    )

    ax3.grid(
        alpha=0.3
    )

    ax3.axis(
        "equal"
    )

    ax3.legend()


    # ========================================================
    # TÍTULO GENERAL
    # ========================================================

    fig.suptitle(

        titulo,

        fontsize=15,

        fontweight="bold"
    )

    plt.tight_layout(
        rect=[
            0,
            0,
            1,
            0.97
        ]
    )

    plt.show()


# ============================================================
# 8. GENERACIÓN DE LOS TRES DATASETS
# ============================================================

X1, y1 = dataset_clusters_redondos(

    N_CLUSTERS_REALES,

    N_SAMPLES,

    SEPARACION,

    RANDOM_STATE
)


X2, y2 = dataset_diferentes_formas(

    N_CLUSTERS_REALES,

    N_SAMPLES,

    SEPARACION,

    RANDOM_STATE
)


X3, y3 = dataset_diferentes_distribuciones(

    N_CLUSTERS_REALES,

    N_SAMPLES,

    SEPARACION,

    RANDOM_STATE
)


# ============================================================
# 9. ANÁLISIS DE LOS TRES DATASETS
# ============================================================

analizar_kmedoids_y_representar(

    X1,

    y1,

    "Dataset 1 - Clusters circulares",

    K_MODELO,

    K_MIN,

    K_MAX
)


analizar_kmedoids_y_representar(

    X2,

    y2,

    "Dataset 2 - Clusters con diferentes formas",

    K_MODELO,

    K_MIN,

    K_MAX
)


analizar_kmedoids_y_representar(

    X3,

    y3,

    "Dataset 3 - Diferentes distribuciones y densidades",

    K_MODELO,

    K_MIN,

    K_MAX
)
"""
PROBLEMA 1 - Sesiones de doblaje

Enunciado: hay que coordinar el doblaje de una pelicula. Los actores deben
coincidir en las tomas donde sus personajes aparecen juntos. Cada actor cobra
un dia completo de desplazamiento si trabaja ese dia, sin importar cuantas
tomas grabe. No se pueden grabar mas de 6 tomas por dia. Objetivo: repartir
las 30 tomas (10 actores) en dias minimizando el gasto total en actores.

Estrategia: cada toma se representa como un bitmask (que actores participan).
El coste de un dia es el numero de actores distintos (union de bitmasks); el
coste total es la suma por dia. Es un problema de MINIMIZACION.
- Fuerza bruta (backtracking): prueba todas las particiones, solo viable en
  pocas tomas (se usa aqui para validar el algoritmo mejorado).
- Algoritmo mejorado: voraz (arma dias) + busqueda local (los mejora).
"""

import itertools
import random
import numpy as np
import pandas as pd
from functools import lru_cache
from math import comb

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ipn6IrbQP4ax8zOnivdBIw2lN0JISkJG4fXndYd27U0/export?format=csv&gid=0"


def cargar_bitmasks(url=SHEET_URL):
    """Descarga la matriz actor x toma y la convierte directamente a {toma: bitmask}."""
    df = pd.read_csv(url, skiprows=1, index_col=0).dropna(how="all")
    df = df.drop(columns=[c for c in df.columns if "Unnamed" in c or c == "Total"], errors="ignore")
    df = df[pd.to_numeric(df.index, errors="coerce").notna()]  # quita la fila "TOTAL"
    return {int(t): int("".join(str(int(v)) for v in fila), 2) for t, fila in df.iterrows()}


def coste_dia(dia, bitmasks):
    """Nº de actores distintos en un dia = popcount de la union (OR) de sus bitmasks."""
    m = 0
    for t in dia:
        m |= bitmasks[t]
    return bin(m).count("1")


def coste_total(particion, bitmasks):
    return sum(coste_dia(d, bitmasks) for d in particion)


def actores_de(dia, bitmasks, n_actores=10):
    """Lista de actores (1..n_actores) que participan en algun momento de un dia."""
    m = 0
    for t in dia:
        m |= bitmasks[t]
    return [i + 1 for i in range(n_actores) if m & (1 << (n_actores - 1 - i))]


# --- Combinatoria: cuantas soluciones hay (con y sin restriccion de 6/dia) ---

def numero_bell(n):
    """B(n): particiones de un conjunto de n elementos, sin limite de tamano (triangulo de Bell).
    Cada fila nueva empieza en el ultimo valor de la fila anterior, y cada
    siguiente valor es "el anterior de esta misma fila" + "el de la fila vieja"."""
    fila = [1]
    for _ in range(n):
        nueva = [fila[-1]]
        for x in fila:
            nueva.append(nueva[-1] + x)
        fila = nueva
    return fila[0]


@lru_cache(maxsize=None)
def particiones_restringidas(n, k=6):
    """R(n): como B(n) pero con grupos de tamano maximo k."""
    if n == 0:
        return 1
    return sum(comb(n - 1, i - 1) * particiones_restringidas(n - i, k) for i in range(1, min(n, k) + 1))


# --- Fuerza bruta (solo para validar en pocas tomas) ---

def fuerza_bruta(tomas, bitmasks, max_dia=6):
    """Backtracking: prueba TODAS las particiones validas y devuelve la de menor coste."""
    mejor = [None, None]  # [particion, coste]

    def backtrack(restantes, particion, coste):
        if not restantes:
            if mejor[1] is None or coste < mejor[1]:
                mejor[0], mejor[1] = [list(d) for d in particion], coste
            return
        if mejor[1] is not None and coste >= mejor[1]:
            return  # poda
        primera, resto = restantes[0], restantes[1:]
        for tam in range(1, min(max_dia, len(restantes)) + 1):
            for companeras in itertools.combinations(resto, tam - 1):
                dia = (primera,) + companeras
                restantes_ = [t for t in resto if t not in companeras]
                backtrack(restantes_, particion + [dia], coste + coste_dia(dia, bitmasks))

    backtrack(list(tomas), [], 0)
    return mejor


# --- Algoritmo mejorado: voraz + busqueda local ---

def algoritmo_mejorado(tomas, bitmasks, max_dia=6, seed=42, max_iter=1000):
    tomas = list(tomas)
    random.Random(seed).shuffle(tomas)

    # 1) Voraz: cada toma va al dia abierto que menos actores nuevos sume, o a uno nuevo
    dias = []
    for toma in tomas:
        candidatos = [d for d in dias if len(d) < max_dia]
        if candidatos:
            mejor_dia = min(candidatos, key=lambda d: coste_dia(d + [toma], bitmasks) - coste_dia(d, bitmasks))
            mejor_dia.append(toma)
        else:
            dias.append([toma])

    # 2) Busqueda local: dos tipos de movimiento.
    #    a) MOVER una toma suelta de un dia a otro con hueco libre.
    #    b) INTERCAMBIAR una toma de un dia por una de otro dia. Esto es
    #       necesario porque "mover" no sirve cuando los dos dias ya estan
    #       llenos (6 tomas): en ese caso solo un intercambio puede mejorar,
    #       y sin este movimiento el algoritmo se queda atascado en un
    #       optimo local (verificado: pasa justo con la solucion real).
    coste = coste_total(dias, bitmasks)
    mejora = True
    while mejora and max_iter > 0:
        mejora, max_iter = False, max_iter - 1
        for i, j in itertools.combinations(range(len(dias)), 2):
            # a) mover, en ambos sentidos
            for origen, destino in ((i, j), (j, i)):
                for toma in list(dias[origen]):
                    if len(dias[destino]) < max_dia:
                        dias[origen].remove(toma); dias[destino].append(toma)
                        nuevo = coste_total([d for d in dias if d], bitmasks)
                        if nuevo < coste:
                            coste, mejora = nuevo, True
                        else:
                            dias[destino].remove(toma); dias[origen].append(toma)
            # b) intercambiar una toma de i por una de j
            for toma_i in list(dias[i]):
                for toma_j in list(dias[j]):
                    # las listas van cambiando con cada intercambio aceptado:
                    # si alguna de las dos tomas ya no esta donde estaba
                    # (snapshot desactualizado), nos la saltamos sin más
                    if toma_i not in dias[i] or toma_j not in dias[j]:
                        continue
                    dias[i].remove(toma_i); dias[j].remove(toma_j)
                    dias[i].append(toma_j); dias[j].append(toma_i)
                    nuevo = coste_total(dias, bitmasks)
                    if nuevo < coste:
                        coste, mejora = nuevo, True
                    else:
                        dias[i].remove(toma_j); dias[j].remove(toma_i)
                        dias[i].append(toma_i); dias[j].append(toma_j)
    return [d for d in dias if d], coste


def generar_datos_aleatorios(n_actores=10, n_tomas=30, prob=0.25, seed=None):
    """Matriz actor x toma aleatoria (como bitmasks), sin filas/columnas vacias."""
    rng = np.random.default_rng(seed)
    m = (rng.random((n_tomas, n_actores)) < prob).astype(int)
    for i in range(n_tomas):
        if m[i].sum() == 0:
            m[i, rng.integers(0, n_actores)] = 1
    for j in range(n_actores):
        if m[:, j].sum() == 0:
            m[rng.integers(0, n_tomas), j] = 1
    return {i + 1: int("".join(map(str, fila)), 2) for i, fila in enumerate(m)}


if __name__ == "__main__":
    bitmasks = cargar_bitmasks()
    n = len(bitmasks)

    print(f"Combinatoria: sin restricciones B({n})={numero_bell(n):.3e}  "
          f"con restriccion R({n})={particiones_restringidas(n):,}")

    subset = list(bitmasks)[:8]
    _, coste_fb = fuerza_bruta(subset, bitmasks)
    _, coste_mej = algoritmo_mejorado(subset, bitmasks)
    print(f"Validacion (8 tomas): fuerza bruta={coste_fb}  mejorado={coste_mej}  "
          f"coinciden={coste_fb == coste_mej}")

    dias, coste = algoritmo_mejorado(list(bitmasks), bitmasks)
    print(f"\nSolucion sobre las {n} tomas reales: {len(dias)} dias, coste={coste}")
    for i, dia in enumerate(sorted(dias, key=min), 1):
        actores = actores_de(dia, bitmasks)
        print(f"  Dia {i}: tomas={sorted(dia)}  actores que viajan={actores}  (coste={len(actores)})")

    print("\nEscalabilidad con datos aleatorios:")
    for n_tomas in (15, 30, 60, 100):
        bm = generar_datos_aleatorios(n_tomas=n_tomas, seed=0)
        dias, coste = algoritmo_mejorado(list(bm), bm)
        print(f"  n_tomas={n_tomas:3d} -> {len(dias)} dias, coste={coste}")

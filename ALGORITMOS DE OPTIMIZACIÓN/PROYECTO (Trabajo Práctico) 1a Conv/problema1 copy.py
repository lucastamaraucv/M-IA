import itertools
import random


def coste_dia(dia, bitmasks):
    m = 0
    for t in dia:
        m |= bitmasks[t]
    return bin(m).count("1")


def coste_total(particion, bitmasks):
    return sum(coste_dia(d, bitmasks) for d in particion)


def generar_datos_aleatorios(n_actores=5, n_tomas=8, prob=0.3, seed=2):
    rnd = random.Random(seed)
    bitmasks = {}
    for i in range(n_tomas):
        bits = [1 if rnd.random() < prob else 0 for _ in range(n_actores)]
        if sum(bits) == 0:
            bits[rnd.randrange(n_actores)] = 1
        bitmasks[i + 1] = int("".join(map(str, bits)), 2)
    return bitmasks


def algoritmo_mejorado(tomas, bitmasks, max_dia=4, seed=42, max_iter=10):
    tomas = list(tomas)
    random.Random(seed).shuffle(tomas)

    dias = []
    for toma in tomas:
        candidatos = [d for d in dias if len(d) < max_dia]
        if candidatos:
            mejor_dia = min(candidatos, key=lambda d: coste_dia(d + [toma], bitmasks) - coste_dia(d, bitmasks))
            mejor_dia.append(toma)
        else:
            dias.append([toma])

    coste = coste_total(dias, bitmasks)
    mejora = True
    while mejora and max_iter > 0:
        mejora, max_iter = False, max_iter - 1
        for i, j in itertools.combinations(range(len(dias)), 2):
            for origen, destino in ((i, j), (j, i)):
                for toma in list(dias[origen]):
                    if len(dias[destino]) < max_dia:
                        dias[origen].remove(toma); dias[destino].append(toma)
                        nuevo = coste_total([d for d in dias if d], bitmasks)
                        if nuevo < coste:
                            coste, mejora = nuevo, True
                        else:
                            dias[destino].remove(toma); dias[origen].append(toma)
            for toma_i in list(dias[i]):
                for toma_j in list(dias[j]):
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


bitmasks = generar_datos_aleatorios()
dias, coste = algoritmo_mejorado(list(bitmasks), bitmasks)
print("Dias:", dias)
print("Coste final:", coste)

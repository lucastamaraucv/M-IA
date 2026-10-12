import numpy as np

data = np.loadtxt('electricity.txt', delimiter=',')
print(f"electricity.txt: {data.shape[0]} filas x {data.shape[1]} nodos")

# Tomar los primeros 168 pasos (1 semana = window=168 del paper)
ventana = data[:168, :]

# Encontrar los nodos con mayor autocorrelacion a lag=24 (patron diario mas claro)
# Un nodo con patron diario limpio tiene alta correlacion entre h[t] y h[t-24]
autocorr = []
for j in range(ventana.shape[1]):
    serie = ventana[:, j]
    if serie.max() > serie.min():  # descarta nodos constantes
        a = np.corrcoef(serie[24:], serie[:-24])[0, 1]
        autocorr.append((a, j))

autocorr.sort(reverse=True)
mejores = [j for _, j in autocorr[:3]]
print(f"Nodos con patron diario mas claro: {mejores}")
print(f"Autocorrelaciones (lag=24): {[round(autocorr[i][0],3) for i in range(3)]}")

# Extraer y normalizar esos 3 nodos (min-max, igual que el paper normalize=3)
ventana_sel = ventana[:, mejores]
vmin = ventana_sel.min(axis=0)
vmax = ventana_sel.max(axis=0)
ventana_norm = (ventana_sel - vmin) / (vmax - vmin + 1e-8)

print(f"Rango normalizado: [{ventana_norm.min():.3f}, {ventana_norm.max():.3f}]")

# Vista rapida del patron diario (hora 0-23, nodo 0)
print(f"\nPatron horas 0-23 (nodo {mejores[0]}, normalizado):")
print(np.round(ventana_norm[:24, 0], 3))

# Guardar
np.savetxt('electricity_sample.csv', ventana_norm, delimiter=',', fmt='%.6f')
print(f"\nelectricity_sample.csv guardado — datos REALES del paper (nodos {mejores})")

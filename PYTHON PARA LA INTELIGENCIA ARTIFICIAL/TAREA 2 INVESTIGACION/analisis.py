import numpy as np

# ── Parametros del paper (Sec. 4.4) ──────────────────────────────────────────
a1, a2, b1, b2 = 0.95, 0.05, 0.0, -0.9

def run_lineal(cc, a1=a1, a2=a2, b1=b1, b2=b2):
    vd = vs = 0.0; VD, VS = [], []
    for ct in cc:
        vd = a1*vd + b1*vs + (1-a1)*ct
        vs = a2*vs + b2*vd + (1-a2)*ct
        VD.append(vd); VS.append(vs)
    return np.array(VD), np.array(VS)

def ganancia(periodo, comp):
    tt = np.arange(1000)
    cc = np.sin(2*np.pi*tt/periodo)
    vd, vs = run_lineal(cc)
    s = (vd if comp == 'd' else vs)[500:]
    return (s.max()-s.min()) / (cc.max()-cc.min())

print("=" * 65)
print("ANALISIS DE GANANCIA — comparacion con el paper (Sec. 4.4)")
print("=" * 65)

# Paper usa: periodo 120 (baja) y periodo 4 (alta) en su ejemplo
print("\n[A] Periodos del ejemplo del PAPER (Sec. 4.4):")
print(f"  {'':22} {'T=120 (baja frec.)':<22} {'T=4 (alta frec.)'}")
print(f"  {'Dendrita v_d':<22} {ganancia(120,'d'):<22.3f} {ganancia(4,'d'):.3f}")
print(f"  {'Soma     v_s':<22} {ganancia(120,'s'):<22.3f} {ganancia(4,'s'):.3f}")
print("  => Paper dice: dendrita ~0.70 baja / ~0.03 alta | soma ~0.70 baja / ~0.88 alta")

# Nuestro codigo usa: periodo 168 (semanal) y 24 (diario)
print("\n[B] Periodos del DATASET ELECTRICO (nuestro experimento):")
print(f"  {'':22} {'T=168h (semanal)':<22} {'T=24h (diario)'}")
print(f"  {'Dendrita v_d':<22} {ganancia(168,'d'):<22.3f} {ganancia(24,'d'):.3f}")
print(f"  {'Soma     v_s':<22} {ganancia(168,'s'):<22.3f} {ganancia(24,'s'):.3f}")

# Verdad: el dataset es sintetico, no el real
print("\n" + "=" * 65)
print("PROBLEMA 1 — DATASET")
print("=" * 65)
data = np.loadtxt('electricity_sample.csv', delimiter=',')
print(f"  Nuestro CSV: {data.shape[0]} filas x {data.shape[1]} nodos")
print(f"  Paper (electricity.txt): 26304 filas x 321 nodos")
print(f"  => Nuestro CSV es SINTETICO (patron diario+semanal construido,")
print(f"     NO es el electricity.txt real de laiguokun/UCI)")

print("\n" + "=" * 65)
print("PROBLEMA 2 — PARAMETROS: codigo original vs nuestro")
print("=" * 65)
print("  Paper (TSLIF.py original):")
print("    decay_factor = [0.8, 0.2, 0.3, 0.7], kk=0.8, yy=0.1")
print("    v1 = df[0]*v1 + df[1]*x  - yy*v2  (a1=0.8, input=0.2, coup=-0.1)")
print("    v2 = df[2]*v2 + df[3]*x  - kk*v1  (a2=0.3, input=0.7, coup=-0.8)")
print()
print("  Nuestro codigo:")
print("    a1=0.95, a2=0.05, b1=0.0, b2=-0.9, g1=0.5, g2=1.0")
print("    vd = 0.95*vd + 0.0*vs  + 0.05*c - 0.5*sd_prev")
print("    vs = 0.05*vs - 0.9*vd  + 0.95*c - 1.0*ss_prev")
print()
a1r, a2r = 0.8, 0.3
print(f"  Paper: a1={a1r} (decaimiento dendrita), a2={a2r} (decaimiento soma)")
print(f"  Nuestro: a1={a1} (dendrita), a2={a2} (soma)")
print(f"  => a2=0.3 en el paper vs a2=0.05 nuestro: diferencia significativa")

# Ganancia con parametros reales del paper
print("\n[C] Ganancia con los parametros REALES del TSLIF.py (a1=0.8, a2=0.3):")
def run_real(cc):
    # decay_factor=[0.8, 0.2, 0.3, 0.7], kk=0.8, yy=0.1
    vd = vs = 0.0; VD, VS = [], []
    for ct in cc:
        vd_new = 0.8*vd + 0.2*ct - 0.1*vs
        vs_new = 0.3*vs + 0.7*ct - 0.8*vd_new
        vd, vs = vd_new, vs_new
        VD.append(vd); VS.append(vs)
    return np.array(VD), np.array(VS)

def ganancia_real(periodo, comp):
    tt = np.arange(1000)
    cc = np.sin(2*np.pi*tt/periodo)
    vd, vs = run_real(cc)
    s = (vd if comp == 'd' else vs)[500:]
    return (s.max()-s.min()) / (cc.max()-cc.min())

print(f"  {'':22} {'T=168h (semanal)':<22} {'T=24h (diario)'}")
print(f"  {'Dendrita v_d':<22} {ganancia_real(168,'d'):<22.3f} {ganancia_real(24,'d'):.3f}")
print(f"  {'Soma     v_s':<22} {ganancia_real(168,'s'):<22.3f} {ganancia_real(24,'s'):.3f}")

print("\n" + "=" * 65)
print("CONCLUSION")
print("=" * 65)
print("  1. El dataset NO es el real del paper (es sintetico)")
print("  2. Los parametros difieren del TSLIF.py original")
print("  3. La separacion de frecuencias SI se demuestra, pero con")
print("     parametros ajustados manualmente (no los aprendidos en el paper)")
print("  4. La idea conceptual del paper SI es correcta en nuestro codigo")

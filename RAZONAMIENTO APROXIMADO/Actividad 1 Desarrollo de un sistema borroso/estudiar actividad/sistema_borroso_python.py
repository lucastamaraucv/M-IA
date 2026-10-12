"""
=============================================================================
Sistema de Razonamiento Aproximado aplicado a señales de trading BTC
Version en Python, para APRENDER como funciona por dentro lo que ya
implementaste en FuzzyCLIPS (ver carpeta subir/: BC_btc_trading.clp y
BH_btc_trading.clp).

Este script NO es un entregable de la actividad. Es material de estudio:
reproduce en Python, con una libreria de logica borrosa real, los mismos
calculos que hace FuzzyCLIPS, para que puedas comparar "por dentro" el
mismo problema resuelto con dos herramientas distintas.

Libreria usada: scikit-fuzzy (la libreria de logica borrosa mas usada en
Python). Instalar una sola vez con:

    pip install scikit-fuzzy

Ejecutar:

    python sistema_borroso_python.py
=============================================================================

Estructura del script:

  PARTE 1 (sin librerias, solo Python/NumPy)
      Reproduce el PUNTO 3 de la actividad: Modus Ponens Generalizado
      sobre universos discretos, usando relaciones borrosas y la
      implicacion de Lukasiewicz. Se hace "a pelo" porque scikit-fuzzy
      no esta pensado para relaciones borrosas discretas -- esta parte
      te permite ver el algoritmo linea por linea, sin caja negra.

  PARTE 2 (con scikit-fuzzy)
      Reproduce los PUNTOS 4 y 5: el mismo sistema Mamdani que esta
      implementado en BC_btc_trading.clp / BH_btc_trading.clp, pero
      escrito con la libreria de Python. Al final compara el resultado
      con el 4.007658833768494 que obtuviste ejecutando FuzzyCLIPS de
      verdad -- deberian coincidir casi exactamente.
"""

import numpy as np


# =============================================================================
# PARTE 1 -- Punto 3: Modus Ponens Generalizado (universo discreto)
# =============================================================================
#
# Conceptos que se ven aqui:
#   - Conjunto borroso discreto: {elemento: grado}
#   - T-norma minimo: para combinar los 2 antecedentes de la regla (AND)
#   - Implicacion de Lukasiewicz: para construir la relacion borrosa R
#   - Composicion sup-min: el propio Modus Ponens Generalizado

def lukasiewicz(a: float, b: float) -> float:
    """Implicacion de Lukasiewicz: I(a,b) = min(1, 1-a+b).

    Se usa en vez de, por ejemplo, la implicacion de Mamdani (min(a,b))
    porque Lukasiewicz es a la vez S-implicacion y R-implicacion -- una
    eleccion "de manual" para este tipo de ejercicio.
    """
    return min(1.0, 1.0 - a + b)


def punto_3_mpg():
    print("=" * 70)
    print("PUNTO 3 -- Modus Ponens Generalizado (universo NO continuo)")
    print("=" * 70)

    # Universos discretos pequeños (igual que en la memoria)
    X = [20, 50, 80]          # RSI
    Z = [2, 8, 16]            # Volatilidad
    Y = [-10, -5, 0, 5, 10]   # Senal

    # Conjuntos borrosos de la regla R1: "SI RSI=sobrevendido Y
    # Volatilidad=baja ENTONCES Senal=comprar_fuerte"
    A = {20: 1.0, 50: 0.2, 80: 0.0}   # RSI sobrevendido
    C = {2: 1.0, 8: 0.4, 16: 0.0}     # Volatilidad baja
    B = {-10: 0.0, -5: 0.0, 0: 0.0, 5: 0.6, 10: 1.0}  # Senal comprar_fuerte

    # Observacion real (imprecisa): RSI ronda 20-25, Volatilidad ronda 2-5
    Aprime = {20: 0.9, 50: 0.3, 80: 0.0}
    Cprime = {2: 1.0, 8: 0.5, 16: 0.0}

    # --- Paso 1: antecedente combinado, t-norma minimo (conjuncion AND) ---
    print("\nPaso 1 -- Antecedente combinado (A x C)(x,z) = min(A(x), C(z)):")
    AC = {}
    for x in X:
        for z in Z:
            AC[(x, z)] = min(A[x], C[z])
            print(f"  ({x:>2},{z:>2}) -> min({A[x]}, {C[z]}) = {AC[(x, z)]}")

    # --- Paso 2: relacion borrosa R((x,z),y) = I((A x C)(x,z), B(y)) ---
    print("\nPaso 2 -- Relacion R((x,z),y) = Lukasiewicz(AxC(x,z), B(y)):")
    R = {}
    header = "           " + "  ".join(f"y={y:>3}" for y in Y)
    print(header)
    for x in X:
        for z in Z:
            row = []
            for y in Y:
                val = lukasiewicz(AC[(x, z)], B[y])
                R[(x, z, y)] = val
                row.append(val)
            print(f"  ({x:>2},{z:>2})  " + "  ".join(f"{v:5.2f}" for v in row))

    # --- Paso 3: observacion combinada ---
    print("\nPaso 3 -- Observacion combinada (A' x C')(x,z) = min(A'(x), C'(z)):")
    ACp = {}
    for x in X:
        for z in Z:
            ACp[(x, z)] = min(Aprime[x], Cprime[z])
            print(f"  ({x:>2},{z:>2}) -> min({Aprime[x]}, {Cprime[z]}) = {ACp[(x, z)]}")

    # --- Paso 4: Modus Ponens Generalizado (composicion sup-min) ---
    print("\nPaso 4 -- MPG: B'(y) = sup_(x,z) min[(A'xC')(x,z), R((x,z),y)]")
    Bprime = {}
    for y in Y:
        mejor = 0.0
        for x in X:
            for z in Z:
                mejor = max(mejor, min(ACp[(x, z)], R[(x, z, y)]))
        Bprime[y] = mejor

    resultado = " + ".join(f"{Bprime[y]}/{y}" for y in Y)
    print(f"\n  B' = {resultado}")
    print("\n  (Debe coincidir con la Seccion 3 de la memoria: 0.5/-10 + 0.5/-5"
          " + 0.5/0 + 0.6/5 + 0.9/10)")
    return Bprime


# =============================================================================
# PARTE 2 -- Puntos 4 y 5: inferencia tipo Mamdani con scikit-fuzzy
# =============================================================================
#
# Aqui SI se usa una libreria real (scikit-fuzzy) para que veas como se
# modela en Python exactamente el mismo sistema que esta en
# BC_btc_trading.clp. Las funciones de pertenencia de abajo son las MISMAS
# que las del deftemplate de FuzzyCLIPS -- compara ambos archivos.

def punto_4_5_mamdani():
    try:
        import skfuzzy as fuzz
        from skfuzzy import control as ctrl
    except ImportError:
        print("\nFalta instalar la libreria. Ejecuta:")
        print("    pip install scikit-fuzzy")
        return

    print("\n" + "=" * 70)
    print("PUNTOS 4 y 5 -- Inferencia tipo Mamdani (scikit-fuzzy)")
    print("=" * 70)

    # --- Variables lingueisticas (Antecedent = entrada, Consequent = salida) ---
    # El universo (np.arange) es la version "continua" del [min, max] que
    # se declara en (deftemplate RSI 0 100 ...) de FuzzyCLIPS.
    rsi = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'RSI')
    volatilidad = ctrl.Antecedent(np.arange(0, 20.01, 0.01), 'Volatilidad')
    senal = ctrl.Consequent(np.arange(-10, 10.01, 0.01), 'Senal')

    # Funciones de pertenencia -- MISMOS puntos (valor, grado) que en
    # BC_btc_trading.clp, solo que aqui se escriben como trapmf/trimf
    # (trapezoidal / triangular) en vez de listas de pares.
    #
    #   deftemplate: (sobrevendido (0 1) (30 1) (50 0))
    #   equivalente: trapmf([0, 0, 30, 50])  -> plano en 1 desde 0 a 30,
    #                                           bajando hasta 0 en 50
    rsi['sobrevendido'] = fuzz.trapmf(rsi.universe, [0, 0, 30, 50])
    rsi['neutral'] = fuzz.trimf(rsi.universe, [30, 50, 70])
    rsi['sobrecomprado'] = fuzz.trapmf(rsi.universe, [50, 70, 100, 100])

    volatilidad['baja'] = fuzz.trapmf(volatilidad.universe, [0, 0, 5, 10])
    volatilidad['media'] = fuzz.trimf(volatilidad.universe, [5, 10, 15])
    volatilidad['alta'] = fuzz.trapmf(volatilidad.universe, [10, 15, 20, 20])

    senal['vender_fuerte'] = fuzz.trapmf(senal.universe, [-10, -10, -8, -4])
    senal['vender'] = fuzz.trimf(senal.universe, [-8, -4, 0])
    senal['mantener'] = fuzz.trimf(senal.universe, [-4, 0, 4])
    senal['comprar'] = fuzz.trimf(senal.universe, [0, 4, 8])
    senal['comprar_fuerte'] = fuzz.trapmf(senal.universe, [4, 8, 10, 10])

    # --- Las 5 reglas, identicas a BC_btc_trading.clp ---
    # El operador "&" es la t-norma minimo (AND borroso) -- el mismo papel
    # que cumple min() en el punto 3, aqui aplicado automaticamente por
    # la libreria.
    r1 = ctrl.Rule(rsi['sobrevendido'] & volatilidad['baja'], senal['comprar_fuerte'])
    r2 = ctrl.Rule(rsi['sobrevendido'] & volatilidad['alta'], senal['comprar'])
    r3 = ctrl.Rule(rsi['neutral'], senal['mantener'])
    r4 = ctrl.Rule(rsi['sobrecomprado'] & volatilidad['baja'], senal['vender_fuerte'])
    r5 = ctrl.Rule(rsi['sobrecomprado'] & volatilidad['alta'], senal['vender'])

    sistema = ctrl.ControlSystem([r1, r2, r3, r4, r5])
    sim = ctrl.ControlSystemSimulation(sistema)

    # --- Observacion: la misma que en BH_btc_trading.clp (RSI=35, Vol=8) ---
    sim.input['RSI'] = 35
    sim.input['Volatilidad'] = 8
    sim.compute()

    # --- Paso 1 (fuzzificacion), mostrado a mano para que se vea el porque ---
    g_sobrevendido = fuzz.interp_membership(rsi.universe, rsi['sobrevendido'].mf, 35)
    g_neutral = fuzz.interp_membership(rsi.universe, rsi['neutral'].mf, 35)
    g_baja = fuzz.interp_membership(volatilidad.universe, volatilidad['baja'].mf, 8)
    g_media = fuzz.interp_membership(volatilidad.universe, volatilidad['media'].mf, 8)

    print("\nPaso 1 -- Fuzzificacion (grado de pertenencia de la observacion):")
    print(f"  RSI=35        -> sobrevendido={g_sobrevendido:.2f}  neutral={g_neutral:.2f}")
    print(f"  Volatilidad=8 -> baja={g_baja:.2f}  media={g_media:.2f}")

    print("\nPaso 2 -- Fuerza de disparo de cada regla (calculada internamente"
          " por la libreria con t-norma minimo, igual que en el punto 4):")
    print(f"  R1 (sobrevendido AND baja) -> alpha = min({g_sobrevendido:.2f}, {g_baja:.2f}) = "
          f"{min(g_sobrevendido, g_baja):.2f}  (dispara)")
    print(f"  R3 (neutral)                -> alpha = {g_neutral:.2f}  (dispara)")
    print("  R2, R4, R5                  -> alpha = 0  (no disparan)")

    print("\nPaso 3-4 -- Recorte + union + centro de gravedad "
          "(hecho automaticamente por skfuzzy.defuzz, metodo 'centroid'):")
    print(f"\n  Senal = {sim.output['Senal']:.6f}")

    print("\n  Comparacion con la ejecucion real en FuzzyCLIPS "
          "(subir/BC_btc_trading.clp):")
    print("    FuzzyCLIPS  (moment-defuzzify 4) = 4.007658833768494")
    print(f"    Python      (scikit-fuzzy)       = {sim.output['Senal']:.15f}")
    print("\n  Deberian coincidir hasta varias cifras decimales -- son el mismo")
    print("  algoritmo (Mamdani + centro de gravedad), solo que un motor lo hace")
    print("  con un lenguaje de reglas dedicado (CLIPS) y el otro con una")
    print("  libreria de proposito general (Python + scikit-fuzzy).")

    return sim.output['Senal']


# =============================================================================
if __name__ == "__main__":
    punto_3_mpg()
    punto_4_5_mamdani()

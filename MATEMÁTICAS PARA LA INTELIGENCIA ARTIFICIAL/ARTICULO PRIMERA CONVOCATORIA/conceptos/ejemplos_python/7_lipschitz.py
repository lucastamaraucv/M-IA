"""
Concepto: FUNCION LIPSCHITZ (continuidad Lipschitz)
Cita: S. Bubeck, "Convex Optimization: Algorithms and Complexity",
Foundations and Trends in Machine Learning, Vol. 8, No. 3-4, 2015,
pp. 231-357. arXiv:1405.4980.

Demuestra: para f(x) = x^2, cuya derivada f'(x) = 2x es Lipschitz con
constante L=2, el descenso de gradiente converge si el tamano de paso
respeta t <= 1/L, y diverge si se usa un paso demasiado grande.
"""


def f(x):
    return x ** 2


def gradiente_f(x):
    return 2 * x  # f'(x) = 2x  ->  L = 2 (constante de Lipschitz)


def descenso_gradiente(x0, tasa_aprendizaje, pasos=10):
    x = x0
    historial = [x]
    for _ in range(pasos):
        x = x - tasa_aprendizaje * gradiente_f(x)
        historial.append(x)
    return historial


if __name__ == "__main__":
    L = 2.0

    print("Con t = 1/L = 0.5 (respeta la cota de Lipschitz) -> CONVERGE:")
    for i, x in enumerate(descenso_gradiente(x0=10.0, tasa_aprendizaje=1 / L)):
        print(f"  paso {i}: x = {x:.6f}   f(x) = {f(x):.6f}")

    print("\nCon t = 1.5 (viola la cota, > 2/L) -> DIVERGE:")
    for i, x in enumerate(descenso_gradiente(x0=10.0, tasa_aprendizaje=1.5)):
        print(f"  paso {i}: x = {x:.6f}   f(x) = {f(x):.6f}")

    print("\nConclusion: para f(x)=x^2 la actualizacion es "
          "x_nuevo = x*(1-2t). Con t=1/L=0.5 se llega a 0 (minimo) de "
          "inmediato. Con t=1.5, |x| se DUPLICA y cambia de signo en "
          "cada paso, creciendo sin control. Respetar t <= 1/L (la cota "
          "que impone la constante de Lipschitz L del gradiente) es lo "
          "que garantiza la convergencia, tal como formaliza Bubeck (2015).")

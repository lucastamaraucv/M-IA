"""
Concepto: TURING-COMPUTABLE
Cita: A. M. Turing, "On Computable Numbers...", Proc. London Math. Soc.,
Series 2, Vol. 42 (1936-1937), pp. 230-265.

Demuestra: la funcion sucesor f(n) = n+1 es Turing-computable, simulando
una maquina de Turing real (cinta + reglas finitas) que la calcula.
"""


def turing_machine_incremento(cinta):
    # Representacion unaria: "1"*n representa el numero n.
    cinta = list(cinta) + ['_']  # '_' = blanco (fin de cinta)
    estado = 'mover_derecha'
    pos = 0

    while estado != 'halt':
        simbolo = cinta[pos]

        if estado == 'mover_derecha':
            if simbolo == '1':
                pos += 1
            elif simbolo == '_':
                estado = 'escribir_uno'

        elif estado == 'escribir_uno':
            cinta[pos] = '1'  # escribe un simbolo extra: n -> n+1
            estado = 'halt'

    return ''.join(cinta).rstrip('_')


if __name__ == "__main__":
    for n in [0, 1, 3, 5]:
        entrada = "1" * n
        salida = turing_machine_incremento(entrada)
        print(f"f({n}) = {len(salida)}   (cinta entrada='{entrada or '(vacia)'}' -> "
              f"cinta salida='{salida}')")

    print("\nConclusion: una maquina con reglas finitas y mecanicas que "
          "SIEMPRE se detiene y produce el resultado correcto -> f(n)=n+1 "
          "es Turing-computable.")

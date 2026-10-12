"""
Concepto: TURING-COMPLETO
Base: construccion de la maquina universal de Turing (Turing, 1936,
seccion "Universal computing machines"). No hay un unico paper que
acune el termino "Turing-complete"; es un concepto estandar de la
teoria de la computabilidad.

Demuestra: Brainfuck, un lenguaje de solo 8 simbolos, es Turing-completo
porque tiene bucles condicionados a memoria ([ ]) + memoria ilimitada.
Eso basta para simular cualquier maquina de Turing.
"""


def ejecutar_brainfuck(codigo, pasos_maximos=100000):
    cinta = [0] * 1000
    puntero = 0
    salida = []
    pc = 0
    pasos = 0

    saltos = {}
    pila = []
    for i, c in enumerate(codigo):
        if c == '[':
            pila.append(i)
        elif c == ']':
            inicio = pila.pop()
            saltos[inicio] = i
            saltos[i] = inicio

    while pc < len(codigo) and pasos < pasos_maximos:
        c = codigo[pc]
        if c == '+':
            cinta[puntero] = (cinta[puntero] + 1) % 256
        elif c == '-':
            cinta[puntero] = (cinta[puntero] - 1) % 256
        elif c == '>':
            puntero += 1
        elif c == '<':
            puntero -= 1
        elif c == '.':
            salida.append(chr(cinta[puntero]))
        elif c == '[' and cinta[puntero] == 0:
            pc = saltos[pc]
        elif c == ']' and cinta[puntero] != 0:
            pc = saltos[pc]
        pc += 1
        pasos += 1

    return ''.join(salida)


if __name__ == "__main__":
    # Programa 1: imprime "A" (codigo ASCII 65) sumando 65 veces.
    programa_A = "+" * 65 + "."
    print("Programa que imprime 'A':", ejecutar_brainfuck(programa_A))

    # Programa 2: usa un BUCLE [ ] para multiplicar 6*7=42 y luego
    # imprimir el caracter correspondiente ('*' = codigo 42).
    # Celda 0 = contador (6), cada vuelta suma 7 a la celda 1.
    programa_multiplicacion = "++++++[>+++++++<-]>."
    print("Programa con bucle (6*7=42 -> chr):",
          ejecutar_brainfuck(programa_multiplicacion))

    print("\nConclusion: el '[' y ']' (bucle condicionado a memoria) son "
          "los que dan a este lenguaje, a pesar de solo 8 simbolos, "
          "capacidad Turing-completa. Un lenguaje SIN bucles jamas podria "
          "serlo, sin importar cuantos comandos tenga.")

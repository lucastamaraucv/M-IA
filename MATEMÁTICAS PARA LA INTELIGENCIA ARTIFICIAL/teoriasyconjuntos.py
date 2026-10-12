import random
from itertools import product
from math import factorial

# =========================
# UTILIDADES
# =========================

def bool_to_str(b):
    return "T" if b else "F"

def str_to_bool_list(s):
    return [x.upper() == "T" for x in s.strip().split()]

# =========================
# MÓDULO 1: LÓGICA
# =========================

def teoria_logica():
    print("\n📘 TEORÍA: Implicación lógica (p → q)")
    print("-----------------------------------")
    print("La implicación p → q significa:")
    print(" 'Si p entonces q'")
    print("\nRegla clave:")
    print("p → q ≡ ¬p ∨ q")
    print("\n⚠️ Solo es FALSO cuando:")
    print("p = True y q = False")
    print("\nTabla:")
    print("p q | p→q")
    for p, q in product([False, True], repeat=2):
        val = (not p) or q
        print(bool_to_str(p), bool_to_str(q), "|", bool_to_str(val))

def practica_logica():
    print("\n🧪 PRÁCTICA")
    print("Construye la tabla de verdad de: p → q")
    print("Orden: (F,F), (F,T), (T,F), (T,T)")

    def formula(p, q):
        return (not p) or q

    correcta = [formula(p, q) for p, q in product([False, True], repeat=2)]

    entrada = input("Tu respuesta (ej: T T F T): ")
    usuario = str_to_bool_list(entrada)

    if usuario == correcta:
        print("✅ Correcto")
        print("✔️ Entendiste la implicación")
        return True
    else:
        print("❌ Incorrecto")
        print("Tu respuesta :", [bool_to_str(x) for x in usuario])
        print("Correcta     :", [bool_to_str(x) for x in correcta])
        print("\n📌 Explicación:")
        print("p → q solo falla cuando p es True y q es False")
        return False

# =========================
# MÓDULO 2: COMBINATORIA
# =========================

def teoria_combinatoria():
    print("\n📘 TEORÍA: Permutaciones sin repetición")
    print("--------------------------------------")
    print("Se usa cuando:")
    print("- Importa el orden")
    print("- No se repiten elementos")
    print("\nFórmula:")
    print("P(n, r) = n! / (n - r)!")
    print("\nEjemplo:")
    print("Con 5 letras, formar palabras de 3 letras:")
    print("P(5,3) = 5! / 2! = 60")

def practica_combinatoria():
    print("\n🧪 PRÁCTICA")

    n = random.randint(4, 7)
    r = random.randint(2, n)

    print(f"¿Cuántas palabras de {r} letras distintas se pueden formar con {n} letras?")

    correcta = factorial(n) // factorial(n - r)

    try:
        usuario = int(input("Tu respuesta: "))
    except:
        print("Entrada inválida")
        return False

    if usuario == correcta:
        print("✅ Correcto")
        print("✔️ Aplicaste correctamente P(n,r)")
        return True
    else:
        print("❌ Incorrecto")
        print("Respuesta correcta:", correcta)
        print("\n📌 Explicación:")
        print(f"P({n},{r}) = {n}! / ({n}-{r})!")
        return False

# =========================
# FLUJO PRINCIPAL
# =========================

def main():
    score = 0
    total = 0

    while True:
        print("\n============================")
        print("APRENDIZAJE GUIADO")
        print("============================")
        print("1. Lógica (p → q)")
        print("2. Combinatoria")
        print("3. Salir")

        opcion = input("Elige opción: ")

        if opcion == "1":
            teoria_logica()
            if practica_logica():
                score += 1
            total += 1

        elif opcion == "2":
            teoria_combinatoria()
            if practica_combinatoria():
                score += 1
            total += 1

        elif opcion == "3":
            print("\n📊 RESULTADO FINAL")
            print(f"Aciertos: {score}/{total}")
            if total > 0:
                print(f"Precisión: {round(score/total*100,2)}%")
            print("Sigue practicando.")
            break

        else:
            print("Opción inválida")

# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    main()
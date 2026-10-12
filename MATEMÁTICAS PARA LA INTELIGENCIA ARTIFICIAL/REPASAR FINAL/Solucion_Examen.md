# Solución — Examen 1ª Convocatoria — 02MIAR: Matemáticas para la IA

---

### 1. El enunciado `p ∨ ¬q` es equivalente a:

- a) `¬(¬p ∨ q)` = `p ∧ ¬q` → **no** equivalente.
- b) `¬(q ∧ ¬p)` = `¬q ∨ p` = `p ∨ ¬q` → **equivalente**.
- c) `p → ¬q` = `¬p ∨ ¬q` → no equivalente (difiere, p.ej. p=F,q=T).
- d) `q → p` = `¬q ∨ p` = `p ∨ ¬q` → **también equivalente** (matemáticamente idéntico a b).

**Respuesta: b)** — Nota: por tabla de verdad, b) y d) son idénticas a `p∨¬q` (ambas se reducen a `¬q∨p`). Es muy probable que sea una errata del enunciado (dos opciones correctas); si solo se puede marcar una, **b)** es la transformación más directa (De Morgan).

---

### 2. `p(x): ∀y∈A, ∃x∈A : y = x³`

Se pregunta si la función cubo es sobreyectiva en A (todo elemento de A tiene raíz cúbica en A).

- a) N: y=2 no tiene raíz cúbica en N → falso.
- b) Z: y=2 no tiene raíz cúbica entera → falso.
- c) Q: y=2 no tiene raíz cúbica racional → falso.
- d) R: todo real tiene raíz cúbica real → **verdadero**.

**Respuesta: d)**

---

### 3. |A|=15, |B|=30, f: A → f(A) ⊂ B

- a) f puede ser inyectiva → sí (15 ≤ 30).
- b) f puede ser sobreyectiva → sí, trivialmente sobre su propia imagen f(A).
- c) f puede tener inversa → sí, si es biyectiva sobre f(A) (posible al ser inyectiva).
- d) Todas las anteriores → **correcto**.

**Respuesta: d)**

---

### 4. Contraseñas de 4 dígitos (0-9) sin repetición

Variaciones sin repetición: 10·9·8·7 = **5040**

---

### 5. f(x) = √(x²) si x>0 ; x² si x≤0

Para x>0: √(x²) = |x| = x. Para x≤0: x².

- a) lim x→0⁺ f(x) = 0 → verdadero.
- b) lim x→0⁻ f(x) = 0 → verdadero.
- c) f continua en 0 → verdadero (f(0)=0, ambos límites laterales = 0).
- d) f derivable en 0 → derivada por la derecha: f'(0⁺)=1 (pendiente de f(x)=x). Derivada por la izquierda: f'(0⁻)=2x|₀=0. **1 ≠ 0 → no derivable.**

**Respuesta (la falsa): d)**

---

### 6. Partición Ω=A∪B, A∩B=∅. P(A)=0.6, P(C|A)=0.5, P(C|B)=1/4

P(B) = 1 − 0.6 = 0.4

P(C) = P(C|A)·P(A) + P(C|B)·P(B) = 0.5·0.6 + 0.25·0.4 = 0.3 + 0.1 = 0.4

**Respuesta: 0,4**

---

### 7. Complejidad del doble bucle anidado (m × n)

Bucle externo recorre A (m), interno recorre B (n) → m·n impresiones.

**Respuesta: b) O(m·n)**

---

### 8. ∅ ≠ A ⊆ B. ¿Cuál afirmación es SIEMPRE falsa?

- a) A∪B⊆A ⟺ B⊆A (ya que A∪B=B cuando A⊆B) → cierto si A=B, no siempre falsa.
- b) A∩B⊆A: como A⊆B, A∩B=A ⊆ A, siempre **verdadera** → descartada.
- c) B\A⊆A: si A=B, B\A=∅⊆A (cierto); no siempre falsa.
- d) A×B⊆A∪B: los elementos de A×B son pares ordenados, los de A∪B son elementos simples; un par ordenado nunca es igual a un elemento de A∪B (ni siquiera en el caso A=B). **Siempre falsa.**

**Respuesta: d)**

---

### 9. v=(α,−2), α≥0. ¿Para cuántos α se cumple ‖v‖₂² = 2‖v‖₁?

‖v‖₂² = α²+4
‖v‖₁ = α+2 (α≥0)

α²+4 = 2(α+2) = 2α+4
α² − 2α = 0 → α(α−2)=0 → α=0 ó α=2

Ambos no negativos → **2 valores**.

**Respuesta: b) 2**

---

### 10. det(−2AB)

A (única con a₁₃=a₂₂=a₃₁=1, resto 0):

```
A = [0 0 1]
    [0 1 0]
    [1 0 0]
```

det(A) = −1 (matriz antidiagonal, permutación impar).

B diagonalizable, autovalores −1, 1, 3 → det(B) = (−1)(1)(3) = −3.

det(−2AB) = (−2)³ · det(A) · det(B) = −8 · (−1) · (−3) = −8·3 = **−24**

---

### 11. A ∈ R^{2×2} simétrica, det(A) = −1

- a) A no es diagonalizable → **falso**, toda matriz simétrica real es diagonalizable (teorema espectral).
- b) A definida negativa → requeriría ambos autovalores negativos → det>0, contradice det=−1 → falso.
- c) A²=Id → requeriría autovalores ±1 exactamente, no garantizado solo con λ₁λ₂=−1 → falso en general.
- d) Autovalores λ y −1/λ: como det(A)=λ₁λ₂=−1 → λ₂=−1/λ₁ → **siempre cierto**.

**Respuesta: d)**

---

### 12. ∫₋₁¹ (x² − x) dx

∫x² dx en [−1,1] = 2/3 (función par)
∫x dx en [−1,1] = 0 (función impar)

**Respuesta: 2/3 ≈ 0,6667**

---

### 13. Beneficio esperado del jugador (dado trucado)

P(impar total) = 2·P(par total), y P(impar)+P(par)=1 → P(par)=1/3, P(impar)=2/3.
Cada valor impar {1,3,5}: P = (2/3)/3 = 2/9. Cada valor par {2,4,6}: P = (1/3)/3 = 1/9.

Pago esperado (impares, el jugador paga n): (1+3+5)·(2/9) = 9·2/9 = 2
Ganancia esperada (pares, el jugador gana n): (2+4+6)·(1/9) = 12/9 = 4/3

Beneficio esperado = 4/3 − 2 = **−2/3 ≈ −0,6667 €**

**Respuesta: −2/3 (−0,6667)**

---

### 14. f(x,y) = 1 + x² − 3y²

∇f = (2x, −6y) = (0,0) → único punto crítico (0,0).

Hessiana: f_xx=2, f_yy=−6, f_xy=0 → det(H) = (2)(−6) − 0 = −12 < 0 → **punto de silla**.

**Respuesta: d)**

---

### 15. Regla de la cadena: [f∘g]'(0)

[f∘g]'(0) = ∂f/∂x(g(0))·g₁'(0) + ∂f/∂y(g(0))·g₂'(0)
= (1)(−2) + (4)(1) = −2 + 4 = **2**

---

### 16. Penalización para que E[puntuación] = −1/5

5 opciones, 1 correcta. P(acierto)=1/5, P(fallo)=4/5. Penalización = x.

E = (1/5)(1) + (4/5)(−x) = −1/5
1 − 4x = −1 → 4x = 2 → **x = 1/2**

**Respuesta: a) 1/2**

---

## Resumen de respuestas

| # | Respuesta |
|---|-----------|
| 1 | b) *(ver nota: b y d son equivalentes)* |
| 2 | d) |
| 3 | d) |
| 4 | 5040 |
| 5 | d) (la falsa) |
| 6 | 0,4 |
| 7 | b) |
| 8 | d) |
| 9 | b) 2 |
| 10 | −24 |
| 11 | d) |
| 12 | 2/3 |
| 13 | −2/3 (−0,6667) |
| 14 | d) |
| 15 | 2 |
| 16 | a) 1/2 |

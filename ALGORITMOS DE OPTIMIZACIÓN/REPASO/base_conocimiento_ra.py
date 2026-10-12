# -*- coding: utf-8 -*-
"""Base de conocimiento de Razonamiento Aproximado (VIU, J.A. Olivas), embebida
en codigo para que quede dentro del .exe al compilar con PyInstaller.
Version condensada del Resumen_Teorico_Curso_Razonamiento_Aproximado.txt."""

BASE_CONOCIMIENTO_RA = """BASE DE CONOCIMIENTO - RAZONAMIENTO APROXIMADO (VIU, José A. Olivas). Resumen de todos los PDFs y archivos .clp del curso (bloques 1-3 = temario: incertidumbre, lógica borrosa, CLIPS/FuzzyCLIPS; 4 = manual FuzzyCLIPS 6.10d; 5-11 = Zadeh 1965, papers y tesis del profesor, boletic, informes OBS). Convenciones: [OJO] = errata/incoherencia/hueco del material original (no inventar solución); [DERIVADO] = cálculo hecho al preparar este resumen (no está en el PDF; verificar). Los ejercicios (1.5-bis, 2.9-bis) no traen solución en los PDFs. Notación: μ/x = grado μ del elemento x; CF=factor de certeza; BEL/PL=creencia/plausibilidad.

1. MODELOS CLÁSICOS DE TRATAMIENTO DE INCERTIDUMBRE
 (Mod_Incertidumbre_OLIVAS_VIU, 53 págs. + Ejer Incert_VIU, 27 págs.)
1.1 Necesidad de modelar incertidumbre
"El conocimiento humano está lleno de incertidumbre e imprecisión;
los esquemas de representación del conocimiento no la contemplan por sí
solos, deben complementarse con un método de representación de la
incertidumbre". Causas de incertidumbre: insuficiente
experiencia, inadecuada representación del conocimiento, información poco
fiable, no completitud, inexactitud inherente al lenguaje.
Los 4 enfoques que anuncia el propio índice del curso: probabilidad Bayesiana, factores de certeza, teoría de la
evidencia/Dempster-Shafer, lógica borrosa.
[OJO] Este PDF (Mod_Incertidumbre) NO desarrolla lógica borrosa pese a
anunciarla en el índice — termina en Dempster-Shafer. La lógica
borrosa se desarrolla en su propio PDF de 141 páginas (bloque 2 de este
resumen).

1.2 Probabilidad Bayesiana
Se basa en el teorema de Bayes; aplicado a reconocimiento de
patrones/clasificación; ejemplo citado: sistema experto PROSPECTOR (Duda et
al. 1979) para exploración de yacimientos de cobre.
Fórmula básica: P(h/e) = P(h∧e)/P(e) = P(h)·P(e/h)/P(e).
Ejemplo meningitis: P(S/M)=0.5, P(M)=1/50.000, P(S)=1/20 →
P(M/S) = 0.5·(1/50.000)/(1/20) = 0.0002.
Generalización a n evidencias con k hipótesis mutuamente exclusivas
y exhaustivas (ΣP(hj)=1) e independientes:
  P(hi/e1∧...∧en) = [P(hi)·P(e1/hi)·...·P(en/hi)] /
 Σj[P(hj)·P(e1/hj)·...·P(en/hj)]
Ejemplo completo "inversores": h1=inversor_alto_riesgo,
h2=inversor_bajo_riesgo (exclusivas/exhaustivas); e1=soltero,
e2=ingresos_altos, e3=joven. P(h1)=0.3, P(h2)=0.7; P(e1/h1)=0.6,
P(e1/h2)=0.4; P(e2/h1)=0.2, P(e2/h2)=0.8; P(e3/h1)=0.5, P(e3/h2)=0.5.
Resultados: P(h1/e1)=0.39, P(h2/e1)=0.61; P(h1/e1∧e3)=0.4,
P(h2/e1∧e3)=0.6; P(h1/e1∧e2∧e3)=0.14, P(h2/e1∧e2∧e3)=0.86. Conclusión
literal: "h2 es la situación más probable".
Defectos del enfoque probabilista: (1) hacen falta
muchas P(hi) y P(ej/hi), no siempre fáciles de estimar; (2) requieren
muestras representativas; (3) nueva evidencia obliga a reconstruir todo;
(4) la independencia de hipótesis rara vez ocurre; (5) asume que la
evidencia que soporta una hipótesis también informa sobre su negación
(P(c/a)=0.8 → P(¬c/a)=0.2), lo cual no siempre es cierto (ej. un síntoma
médico no necesariamente "descarta" la ausencia de la enfermedad en esa
proporción).
Estos 5 defectos son exactamente lo que motivan los dos
enfoques siguientes: los Factores de Certeza evitan el requisito de
P(h)+P(¬h)=1 (defecto 5), y Dempster-Shafer generaliza formalmente esa
misma idea con intervalos de creencia en vez de un único número.

1.3 Factores de Certeza — MYCIN
Introducidos por Buchanan y Shortliffe (1979) en el sistema experto
médico MYCIN. No se basan en probabilidad ni en poblaciones
muestrales, sino en el juicio de un experto. Viven en el
intervalo [-1,1]: 1=confianza total, -1=no-creencia total.
Combinación de dos reglas con la misma conclusión h, CF(h,e1) y
CF(h,e2):
  (a) si ambos CF > 0: CF(h,e1) + CF(h,e2)·(1-CF(h,e1))
  (b) si ambos CF < 0: CF(h,e1) + CF(h,e2)·(1+CF(h,e1))
  (c) en cualquier otro caso: [CF(h,e1)+CF(h,e2)] / (1-min(|CF(h,e1)|,|CF(h,e2)|))
Ejemplo tráfico, ambas positivas: R1 viernes→tráfico 0.8, R2
llueve→tráfico 0.7 → 0.8+0.7·(1-0.8) = 0.94.
Ejemplo tráfico, signos distintos: R1 viernes→tráfico 0.8,
R2 fin_de_mes→tráfico -0.4 → resultado 0.66 (caso c).
CF de una condición simple: CF(h,e1) = CF(e1)·CFR(h,e1).
Condición conjunta (Y): CF(h,e1∧...∧en) = CFR(h,...)·min[CF(e1),...,CF(en)]. Condición disyuntiva (O): CF(h,e1∨...∨en) =
CFR(h,...)·max[CF(e1),...,CF(en)].
Ejemplo con Y/O combinados: R1 (A 0.7 Y B 0.2)→C,-0.8; R2
(D 0.3 O F 0.6)→C,-0.4. CF(C,A∧B)=0.2·(-0.8)=-0.16; CF(C,D∨F)=0.6·(-0.4)=
-0.24; CF(C,(A∧B)∧(D∨F)) = -0.16-0.24·(1-0.16) = -0.33.
Ejemplo de encadenamiento de reglas, inversores: R1
e1→h CFR=0.75, R2 e2→h CFR=0.6, R3 e3→h CFR=-0.8, R4 h→g CFR=-0.7
(g=invertir_en_bonos). FC observados: e1=0.9, e2=0.5, e3=0.9. Cálculo:
CF(h,e1)=0.67; CF(h,e2)=0.3; CF(h,e3)=-0.72; CF(h,e1∧e2)=0.77;
CF(h,e1∧e2∧e3) = [0.77-0.72]/(1-0.72) = 0.17; CF(g,h) = 0.17·(-0.7) =
-0.12 → "No debería invertir".

1.4 Teoría de la Evidencia — Dempster-Shafer
Objetivo: eliminar el punto débil de Bayes de que creer más en h no
tiene por qué implicar creer menos en ¬h.
Marco de discernimiento H={h1,...,hm}, hipótesis mutuamente
exclusivas y exhaustivas. Conjunto potencia P(H): 2^M subconjuntos. Masa de probabilidad básica m: 2^M→[0,1], con m(∅)=0 y
Σ(Si⊆H) m(Si)=1.
Creencia: BEL(S) = Σ(X⊆S) m(X). Plausibilidad:
PL(S) = 1-BEL(¬S). Intervalo de creencia: [BEL(S), PL(S)]. Incertidumbre:
PL(S)-BEL(S).
Regla de combinación de Dempster-Shafer:
  m3(C) = [Σ(X∩Y=C) m1(X)·m2(Y)] / [1 - Σ(X∩Y=∅) m1(X)·m2(Y)]
El denominador normaliza restando el "conflicto" entre evidencias
(numerador de la suma que va sobre X∩Y=∅). Si el conflicto es 1, m3 queda
indefinida ("asignación contradictoria", p.44).
Caso de estudio completo "Watson" (crimen, p.45-52): marco
H={Bob,Jim,Sally}; masas iniciales de Watson y masas de nueva evidencia
(colillas/facturas); tabla cruzada X×Y para calcular el conflicto
(=0.245, normalización 1-0.245=0.755) y las masas combinadas finales,
p.ej. m3(Bob)=0.17/0.755=0.225.

1.5-bis ENUNCIADOS TRANSCRITOS de Ejer Incert_VIU (27 págs., SIN solución)
La versión anterior de este resumen solo indicaba el número de
ejercicios; aquí quedan transcritos con todos sus datos (texto del PDF, autor J.
A. Olivas). Ninguno trae solución. FC = factor de certeza; en las reglas
"Entonces X, v" v es el FC de la regla. m = masa de probabilidad; BEL = creencia;
Pl = plausibilidad; Inc = incertidumbre = Pl − BEL. Fórmulas-recordatorio que
el propio PDF pone al pie: Bayes P(h/e)=P(h∧e)/P(e)=P(h)P(e/h)/P(e); general
P(hi/e1..en)=P(hi)P(e1/hi)…P(en/hi)/[Σj P(hj)P(e1/hj)…P(en/hj)]; combinación de
Dempster-Shafer m3(C)=[Σ_{X∩Y=C} m1(X)·m2(Y)]/[1−Σ_{X∩Y=∅} m1(X)·m2(Y)].

EJERCICIO INTEGRADOR "Incertidumbre con las tres técnicas"
  Diálogo Ingeniero del Conocimiento (IC) – Experto (E): conclusiones posibles
  C1, C2, C3 (aisladas o en cualquier combinación; sin dependencia entre
  ellas). C3 se alcanza cuando se dan A8, A9 o ambos. C2 requiere siempre A6 y A7
  a la vez. C1 se alcanza por dos caminos: desde la conclusión parcial B1 o
  desde la conclusión parcial B2. B1 se obtiene con A1 y A2 juntos. B2 se obtiene
  por dos caminos: A2 ∧ A3 ∧ A4, o bien A4, A5 o ambos (A4 ∨ A5).
  Se pide:
 1. ¿Qué esquema de representación del conocimiento (reglas de producción) y por
 qué? Expresar la base de conocimientos.
 2. Si se observan A1, A3, A4, A5, A7, A9: ¿qué método de inferencia (razonamiento
 hacia adelante)?
 3. Inferencias con reglas de producción, describiendo cada paso: agenda/
 memoria de trabajo, reglas seleccionadas, conjunto conflicto, regla
 disparada, inferencia (una regla disparada no vuelve al conjunto conflicto).
 4. Solo A9 observado (A8 y A9 son evidencias de C3): P(C3∧A9)=0.12; P(A9)=0.36
 → ¿incertidumbre de C3 dado A9? (Bayes: P(C3/A9)=0.12/0.36=0.333).
 5. A4 y A5 observados a la vez (P=0.2); P(B2)=0.7; P(A4∧A5 | B2)=0.003 → ¿P(B2 |
 A4∧A5) con Bayes?
 6. Con factores de certeza: relación que alcanza C3 = 0.9; C2 = 0.4; C1 desde B1
 = 0.4 y desde B2 = 0.8; la que obtiene B1 = −0.8; las que concluyen B2 = 0.9.
 7. Observados A1, A2, A3, A4, A5, A6, A7, A9 con FC(A1)=0.5; FC(A2)=0.8;
 FC(A3)=0.9; FC(A4)=0.9; FC(A5)=−0.8; FC(A6)=−0.9; FC(A7)=0.4; FC(A9)=0.4:
 ¿FC de todas las inferencias?
 Con Teoría de la evidencia sobre {C1,C2,C3}: BEL(C1,C3)=0.6; BEL(C1,C2)=0.5;
 Inc(C1,C3)=0.2; m(C1)=0.1; m(C3)=0.3; m(C1,C2,C3)=0.
 8. Calcular la masa de cada elemento del conjunto potencia (m(∅)=0).
 9. Se reasignan m2(C2)=0.1 y m2(C2,C3)=0.1 (el resto igual): calcular el
 conflicto entre las evidencias anteriores y las nuevas.
  10. Calcular la nueva masa m3(C3).
  (La numeración 8-10 es del transcriptor; en el PDF cada bloque reinicia 1-3.)

EJERCICIOS DE INFERENCIA BAYESIANA (1B-6B)
  1B: fallos de vehículo A y B (mutuamente exclusivos e independientes);
 síntomas S1, S2, S3 independientes. 60% de los fallos son de tipo A;
 P(S1/A)=0.4; P(S2/A)=0.8; P(S3/A)=0.6 [las probabilidades de los síntomas dado
 B NO se dan en el enunciado; hay que deducirlas o asumir un dato que falta].
 Se pide: (1) P(fallo B | S2); (2) P(fallo A | S1 y S3).
 [OJO] El enunciado da solo P(Si/A) y P(A)=0.6; sin P(Si/B) el cálculo de
 P(B|S2) no es determinable con datos del PDF: es un hueco del enunciado.
  2B: un paciente solo puede tener la enfermedad A, B o C (distintas e
 independientes). P(A)=0.6 y si aparecen S2, S4, S5 se padece A; P(S4/A)=0.1,
 P(S4/B)=0.1, P(S4/C)=0.8. Si aparecen S1 y S4 se padece C; P(S1/A)=0.3,
 P(S1/B)=0.4, P(S1/C)=0.3. P(B)=0.3. Síntomas independientes. Paciente con S1, S2 y
 S4. Se pide: (1) conocimiento mínimo en la base y método de representación;
 (2) base de hechos y diagnóstico; (3) certidumbre del diagnóstico (mostrar
 operaciones). [P(C)=0.1 por exhaustividad; P(S2/·) no se da.]
  3B: P(fallo de la lavadora)=0.3; P(tambor falla | falla la lavadora)=0.004;
 P(termostato falla | falla la lavadora)=0.9. (1) ¿Qué tipo de incertidumbre
 conviene?; (2) certidumbre de fallo de la lavadora por fallo del termostato;
 (3) ¿y por fallo conjunto de tambor y termostato?
  4B: electrodoméstico con fallos A y B: P(fallo del electrodoméstico)=0.6;
 P(observar fallo B | ha fallado)=0.3; P(falla el electrodoméstico | fallos A y B
 conjuntos)=0.1. (1) mejor forma de representar; (2) certidumbre de fallo por B;
 (3) P(observar fallo A | ha fallado).
  5B: inferencias posibles A y B (independientes). R1: Si x1 ∧ x2 ∧ x3 → A;
 R2: Si x4 ∨ x5 → A; R3: Si x8 ∧ x9 → A; R4: Si x6 ∨ x7 → A; R5: Si x2 ∧ x3 ∧ x9 → B.
 Se observa x5, x8, x9: certidumbre de la inferencia alcanzada. Datos: P(B)=0.3,
 P(x5/A)=0.5, P(x8/B)=0.8, P(x9/A)=0.1.
  6B: bomberos del parque Megapolis: salen solo por incendio o inundación;
 si no, se quedan en el Parque. P(incendio)=0.15; P(quedarse en el Parque)=0.8
 (→ P(inundación)=0.05). P(calor | inundación)=0.1; P(calor | Parque)=0.2; P(calor |
 incendio)=0.8. P(sequía | inundación)=0.001; P(sequía | incendio)=0.7; P(sequía |
 Parque)=0.28. P(tormenta | incendio)=0.18; P(tormenta | inundación)=0.08; P(tormenta |
 Parque)=0.74. Evidencias independientes, hipótesis exclusivas y exhaustivas.
 (1) certidumbre de que se queden en el Parque con sequía; (2) certidumbre de que
 salgan por inundación con tormenta y calor.

EJERCICIOS DE FACTORES DE CERTEZA (FC1-FC8)
  FC1: R1 Si H1 ∨ H4 → B, 0.8; R2 Si H5 ∧ H6 → D, −0.3; R3 Si H2 ∧ H3 → A, −0.5;
 R4 Si H7 → A, 1.0; R5 Si H6 ∨ B → C, 0.9; R6 Si H1 ∧ A → C, −0.6; R7 Si C → D, −0.8.
 Hechos H1..: FC(H1)=0.6; FC(H3)=−0.6; FC(H5)=0.4; FC(H6)=0.7; FC(H7)=0.8. Preguntas:
 tipo de razonamiento; inferencias paso a paso (agenda, conjunto conflicto, regla
 disparada); certezas de las inferencias.
  FC2: R1 Si H1 → B, 0.9; R2 Si ?X ∧ ?Y ∧ ?Z → A, 0.6; R3 Si A → C, −0.4; R4 Si H2 ∨
 ?Z → B, 0.8; R5 Si B → C, 1.0. ?X ∈ {x1,x2,x3,x4}, ?Y ∈ {y1,y2,y3}, ?Z ∈ {z1,z2,z3,z4}
 (variables genéricas que representan conjuntos de variables particulares).
 Hechos: H1 (FC 1), x1 (0.9), y1 (0.6), z2 (0.7), z3 (0.4). Inferencias paso a paso y sus
 certezas.
  FC3: árbol de reglas para la conclusión h con conjunciones/disyunciones de
 evidencias e11, e12, e13, e14 (OR con e15, e16), e17 ∧ e18, e21, e22, e23 y FC
 asociados (0.9, 0.6, 0.7, −0.6, 0.8, 0.9, 0.6, 0.9, 0.5, 0.8, 0.6, 0.9, 0.8, 0.9, 1.0). Hechos
 observados: e13, e14, e15, e16, e17, e18, e23. Calcular el FC de h. [OJO] El diagrama
 se ha perdido en el texto extraído: solo constan los rótulos y la lista de
 números; la estructura exacta del árbol (qué FC va en cada arista) hay que
 consultarla en la página 13 del PDF.
  FC4: R1 Si H1 ∧ H2 ∧ H3 → AMARILLO; R2 Si C2 → AMARILLO; R3 Si C4 → AMARILLO;
 R4 Si H9 → C4; R5 Si H4 ∨ H5 → C1; R6 Si C3 → C4; R7 Si H6 ∨ H7 ∨ H8 → C3; R8 Si C1 → C2.
 FC de las reglas: R1=−0.8, R2=0.8, R3=0.2, R4=−1, R5=1, R6=0.8, R7=−0.7, R8=0.9. FC de las
 evidencias: H1=0.6, H2=0.5, H3=0.9, H4=0.2, H5=0.8, H6=0.3, H7=0.8, H8=0.6, H9=0.9. Se
 observan las nueve: ¿FC de AMARILLO? (detallar).
  FC5: R1 Si A1 ∧ A2 ∧ A3 → B1, −0.7; R2 Si A2 ∨ A3 → B2, 0.9; R3 Si A4 ∧ A5 → B2,
 0.4; R4 Si B1 → C1, 0.8; R5 Si B2 → C1, −0.4; R6 Si A5 ∨ A6 ∨ A7 → B3, 0.5; R7 Si C1 → X,
 0.4; R8 Si B3 → X, 0.8. Hechos: FC(A1)=0.4, FC(A2)=0.8, FC(A3)=0.5, FC(A5)=0.4, FC(A7)=0.5
 (A1, A2, A3, A5, A7 observados). Preguntas: razonamiento; conclusiones paso a
 paso; certezas de todas.
  FC6: R1 H1 → A1, 0.8; R2 H2 ∧ H3 → A2, 0.6; R3 H4 → A3, −0.9; R4 A1 ∧ A2 ∧ A3 → M,
 0.5; R5 H5 ∧ H6 → A4, 0.9; R6 H4 ∧ A4 → M, −0.7. [conectivas ∧/∨ leídas del
 contexto; en el texto extraído los símbolos se perdieron]. Observados H1, H2, H3, H4,
 H6 con FC H1=0.6, H2=0.8, H3=0.6, H4=0.8, H6=0.9: inferencias paso a paso y
 certidumbres.
  FC7: razonamiento hacia adelante. R1 Si H1 ∧ H2 → C, 0.7; R2 Si H2 ∨ H3 ∨ H4 → C,
 −0.8; R3 Si C → A, 0.8; R4 Si H5 → A, −0.9. Hechos: H1=0.8; H2=0.4; H4=0.9; H5=0.6.
 ¿Incertidumbre de cada inferencia?
  FC8: R1 Si x1 ∧ x2 ∧ x3 → A, 0.8; R2 Si x4 ∨ x5 → A, 0.4; R3 Si x8 ∧ x9 → A, −0.8;
 R4 Si x6 ∨ x7 → A, 0.9. Observados x1=0.8; x2=0.6; x3=0.3; x5=−0.9; x6=−0.4; x7=−0.7;
 x8=0.2; x9=0.3. ¿Certidumbre de A? (todos los cálculos).

EJERCICIOS DE TEORÍA DE LA EVIDENCIA (DS1-DS9)
  DS1: tostadores tipo A (averías A1, A2, A3 o combinación) y tipo B (B1..B4
 o combinación). mA(A2,A3)=0.35; mB(B1)=0.10; mB(B2)=0.15; mB(B3)=0.30; mB(B4)=0.10;
 mB(B1,B3)=0.35. Plausibilidades: PlA(A1)=0.4; PlA(A3)=0.7; PlA(A1,A2)=0.85;
 PlA(A2,A3)=0.85. (1) creencia de A1 y A2 juntas en el tipo A; (2) incertidumbre
 de B2 y B4 en el tipo B.
  DS2: errores E1, E2, E3 o combinación. BEL(E1,E2)=0.6; BEL(E1,E3)=0.7;
 Inc(E1,E2)=0.1; m(E1)=0.4; m(E2)=0.2; m(E1,E2,E3)=0; m(∅)=0. (1) masa de cada
 elemento del conjunto potencia; (2) el ordenador falla de nuevo: m2(E1)=0.2 y
 m2(E1,E3)=0.2 (el resto igual): conflicto con las evidencias anteriores;
 (3) m3(E1) y m3(E3).
  DS3: problemas A, B, C o superposición; evidencia total 1 repartida así:
 A 0.2; B 0.1; C 0.05; [A,B] 0.3; [A,C] 0.1; [B,C] 0.1; [A,B,C] 0.15. (1) Para [A,C]: creencia,
 plausibilidad, incertidumbre e intervalo de creencia. Tras una inspección más
 profunda: A 0.1; B 0.2; C 0.1; [A,B] 0.2; [A,C] 0.3; [B,C] 0.05; [A,B,C] 0.05. (2) ¿Creencia
 del caso [A,C] ahora?
  DS4: opciones de inversión A, B, C o combinación. Inc(A,B)=0.35, Creencia(A,B)=
 0.55; Inc(A,C)=0.25, Creencia(A,C)=0.55; Inc(B,C)=0.25, Creencia(B,C)=0.45. Se pide:
 (1) marco de discernimiento y conjunto potencia; (2) masa de cada elemento del
 conjunto potencia (m(∅)=0); (3) nueva reasignación m2(A)=0.2; m2(B)=0.15; m2(C)=0.1;
 m2(AB)=0.1; m2(AC)=0.2; m2(BC)=0.1; m2(ABC)=0.15: calcular y cuantificar el conflicto.
  DS5: fallo de motor A, B, C, D o combinación; m(A)=0.7; m(D)=0.05; m(A,B)=0.1;
 m(B,C)=0.15. (a) creencia de A, B y C simultáneos; (b) creencia de A y D; (c)
 plausibilidad de A y D; (d) intervalo de creencia de A y D; (e) incertidumbre de
 A, B y C simultáneos.
  DS6: asma (A), neumonía (N), gripe (G) o combinación. m(A)=0.3; m(N)=0.2;
 m(A,N,G)=0; Creencia(A,N)=0.7; Creencia(A,G)=0.6; Inc(A,N)=0.2. (1) evidencia de
 cada elemento del conjunto potencia (m(∅)=0); (2) reasignación m2(A)=0.4 y
 m2(A,G)=0.1 (resto igual): conflicto entre evidencias.
  DS7: soluciones A, B, C, D o combinación. m1(A)=0.2; m1(B)=0.1; m1(C)=0.15;
 m1(D)=0.05; m1(A,C)=0.05; m1(B,C)=0.02; m1(B,D)=0.15; m1(A,C,D)=0.1; m1(A,B,D)=0.08;
 m1(B,C,D)=0.1. (1) incertidumbre de (A,B); (2) intervalo de creencia de (A,B,C).
  DS8: marco H={A,B}; tres expertos: m(A): 0.3 / 0.2 / 0.5; m(B): 0.3 / 0.2 /
 0.2 (E1 / E2 / E3) [m(A,B) = el resto: 0.4 / 0.6 / 0.3]. (1) ¿Qué par de
 expertos tiene los criterios más distintos y más parecidos? (razonar con
 cálculos; conflicto = medida de discrepancia entre pares); (2) masa
 conjunta de B si se combinan los expertos 1 y 2.
  DS9: soluciones A, B, C o combinación; Pl(A,C)=0.8; Inc(A,C)=0.5; Bel(A,B)=0.7;
 m(A)=m(C)=0. (1) Bel(B,C); (2) intervalo de creencia de (A,C).
  Los 24 ejercicios (1 integrador + 6 + 8 + 9) quedan cubiertos: 6 de
  Bayes, 8 de FC y 9 de Dempster-Shafer más el integrador (que a su vez tiene su
  parte de Bayes, FC y DS). Las fórmulas para resolverlos están en 1.2-1.4.

1.6 COMPLEMENTOS al bloque 1 (detalles de las diapositivas de Mod_Incertidumbre
 no recogidos arriba; revisión página a página del texto del PDF)
Necesidad de modelar incertidumbre: el conocimiento queda
representado por "un esquema de representación + un método de representación de
la incertidumbre". Ejemplos cotidianos: el médico que pone un tratamiento con
síntomas ambiguos; entender frases "entre líneas"; decidir con información
imprecisa y/o incierta. (Las causas de incertidumbre, p.4, ya constan en 1.1.)
Bayes: la incertidumbre se modela con probabilidades; el teorema
de Bayes permite calcular probabilidades complejas a partir de otras más simples
basadas en observaciones reales; usado en reconocimiento de patrones y
clasificación (ej.: PROSPECTOR). La probabilidad condicional P(h/e) se interpreta
como relación CAUSA-EFECTO entre e y h (e = evidencia que soporta h). Dos
evidencias: P(h/e1∧e2)=P(h)·P(e1∧e2/h)/P(e1∧e2); n evidencias: P(h/e1∧..∧en)=
P(h)·P(e1∧..∧en/h)/P(e1∧..∧en). Con k hipótesis mutuamente exclusivas
(P(hi∧hj)=0) y exhaustivas (Σj P(hj)=1) y n evidencias independientes
(P(ei/ej)=P(ei)) se llega a la fórmula general (ya en 1.2). Significado de los
símbolos: P(hi/e1..en) = probabilidad de hi dadas las evidencias; P(hi) = prob. de hi;
P(ei/hj) = prob. de observar ei dada hj cierta; j recorre todas las hipótesis.
Ejemplo 2 de Bayes: ¿yacimiento de cobre en una localización?
A partir de estudios de minerales de la zona (evidencias): se necesitan por
adelantado P(minerales) y P(minerales/Cu) para estimar P(Cu/minerales)
(PROSPECTOR, Duda et al. 1979).
Ejemplo "inversores" — detalle de los cálculos de la tabla:
P(h1/e1)=[0.3·0.6]/[0.3·0.6+0.7·0.4]=0.18/0.46=0.39; P(h1/e2)=0.097 (P(h2/e2)=0.903);
P(h1/e3)=0.3 (P(h2/e3)=0.7: e3 no aporta información porque P(e3/h1)=P(e3/h2)=0.5).
Tabla final (P.I. = probabilidad inicial): h1: 0.3 | e1 0.39 | e2 0.097 | e3 0.3 |
e1e3 0.4 | e1e2e3 0.14; h2: 0.7 | 0.61 | 0.903 | 0.7 | 0.6 | 0.86. Interpretación:
h2 es la situación más probable con e1e2e3 y con e1e3. (Se nota que las
probabilidades "a posteriori" del enunciado son las condicionales dadas h.)
Defectos del enfoque probabilista: el defecto 5 dice que el
enfoque asume que la evidencia "a" para una hipótesis "c" también afecta a su
negación (P(c/a)=0.8 ⇒ P(¬c/a)=0.2); "en medicina la presencia de un síntoma no sería
una evidencia que soportase a la vez la existencia y la no existencia de una
enfermedad" — motiva los CF y D-S.
Factores de certeza: se basan en el JUICIO del experto sobre
ocurrencias o relaciones ("Si se da A entonces se dará C casi con toda seguridad");
son evaluaciones personales que se añaden al enunciado del conocimiento; NO se rigen
por probabilidad ni salen de poblaciones muestrales sino de la experiencia; en
probabilidad P(hecho)+P(contrario)=1, pero un experto puede sentir algo como
cierto sin saber cuánto lo es su contrario. Introducidos en MYCIN (Buchanan y
Shortliffe 79). Uso típico: asociados a REGLAS DE PRODUCCIÓN. Ejemplo MYCIN: "Si la
coloración del organismo es gram positivo y la morfología es coco y la forma de
crecimiento es en cadenas, Entonces hay una evidencia (0.7) de que la identidad
del organismo sea un estreptococo". CF ∈ [−1,1] (1 = completa confianza, −1 =
completa no creencia).
Ejemplo de combinación con signos opuestos, aclaración: tráfico con
R1 viernes (0.8) y R2 fin de mes (−0.4): 0.8+(−0.4)/(1−min(0.8,0.4)) = 0.4/0.6 =
0.66 ("se disminuye la fuerza de la mayor").
Ejemplo "inversores" con CF: h1 inversor_de_alto_riesgo, h2
inversor_de_bajo_riesgo, e1 joven, e2 ingresos_altos, e3 casado. Reglas: Si joven →
alto riesgo 0.6; Si ingresos_altos → alto riesgo 0.1; Si casado → alto riesgo −0.7.
Con e1 y e2: CF(h,e1e2)=0.6+0.1(1−0.6)=0.64 ("poco aporta la 2ª regla"); si además
aparece e3: CF(h,e1e2e3)=[0.64+(−0.7)]/[1−min(0.64,0.7)] = −0.06/0.36 = −0.16
(el PDF escribe "[0.64+(−0.7)]/[1−0.64] = −0.16"; "si la persona es casada, se
disminuye la certeza del perfil de alto riesgo").
CF de una condición: R1: Si e1, CF(e1) Entonces h, CFR(h,e1) →
CF(h,e1)=CF(e1)·CFR(h,e1). Conjunción: CF(h,e1∧..∧en)=CFR·min[CF(e1),..,CF(en)];
disyunción (el PDF escribe "(y)" por errata en el título de la p.28):
CF(h,e1∨..∨en)=CFR·max[CF(e1),..,CF(en)].
Dempster-Shafer: desarrollada por Dempster, refinada por
Shafer; elimina puntos flacos de Bayes: la suma de la creencia en un hecho y en su
contrario NO tiene por qué ser 1 (en probabilidad, subir una hipótesis baja su
contraria). Parte de "entornos" θ1..θn; un entorno H es un conjunto de hipótesis
mutuamente exclusivas y exhaustivas = MARCO DE DISCERNIMIENTO H={h1,..,hm}.
CONJUNTO POTENCIA P(H)={∅,{h1},{h2},...,{h1,h2},...,{h1..hm}} ("todas las posibles
respuestas a las posibles preguntas"); 2^M subconjuntos. MASA m: 2^M→[0,1] con
m(∅)=0 y Σ_{Si⊆H} m(Si)=1, 0<m(Si)<1 asignada por el experto. BEL(S)=Σ_{X⊆S}
m(X) (creencia en S y en todos sus subconjuntos); BEL(H)=1. INTERVALO DE
CREENCIA de S: [BEL(S), 1−BEL(¬S)] donde ¬S es el complementario respecto al
potencia; PLAUSIBILIDAD PL(S)=1−BEL(¬S) = grado en que la evidencia no puede
refutar S; INCERTIDUMBRE (ignorancia) de S = PL(S)−BEL(S).
Bayes vs. D-S: en Bayes las probabilidades son un número; en D-S
son intervalos de creencia; al estrecharse los intervalos ambas teorías tienden a
coincidir. Ejemplo: ¿probabilidad de que una persona desconocida hable una lengua
extranjera? Bayes: 1/2; D-S: depende de la evidencia. Comparativa: PROBABILIDAD:
Σ Pi=1; para S1⊆S2, P(S1)≤P(S2); P(S)+P(¬S)=1. D-S: 0≤m(S)≤1; para S1⊆S2, m(S1) no
es necesariamente ≤ m(S2); la relación entre m(S) y m(¬S) no está definida.
Ejemplo "proceso industrial con cuatro modos de fallo A,B,C,D":
masas m(∅)=0, m(A)=0.7, m(B)=0.05, m(C)=0.02, m(D)=0.03, m(A,B)=0.1, m(A,D)=0.05,
m(A,B,D)=0.05, el resto 0 (suman 1). Creencias: Bel(A)=0.7; Bel(AB)=0.7+0.05+0.1=
0.85; Bel(AD)=0.7+0.03+0.05=0.78. Plausibilidades: Pl(A)=1−m(B)−m(C)−m(D)−m(BC)−
m(BD)−m(CD)−m(BCD)=1−0.05−0.02−0.03=0.9; Pl(B)=1−0.7−0.02−0.03−0.05=0.2; Pl(BC)=
1−0.7−0.03−0.05=0.22; Pl(ACD)=1−m(B)=0.95. Incertidumbres: A: 0.9−0.7=0.2; B:
0.2−0.05=0.15. Intervalos: A [0.7, 0.9]; ACD [0.8, 0.95]. Tabla completa (conjunto:
creencia, plausibilidad): A 0.7/0.9; B 0.05/0.2; AB 0.85/0.95; C 0.02/0.02; AC 0.72/
0.92; BC 0.07/0.22; ABC 0.87/0.97; D 0.03/0.13; AD 0.78/0.93; BD 0.08/0.28; ABD
0.98/0.98; CD 0.05/0.15; ACD 0.8/0.95; BCD 0.1/0.3; ABCD 1/1.
Regla de combinación: m1 y m2 sobre el mismo H (m2 con evidencia
añadida/actualizada); X, Y, C subconjuntos de H; el denominador normaliza para que
m esté en [0,1]; "a medida que hay más evidencia común se da mayor soporte a las
hipótesis (numerador)"; la cantidad Σ_{X∩Y=∅} m1(X)m2(Y) mide el CONFLICTO
existente entre evidencias que soportan las mismas hipótesis; si vale 1, m3(C) no
se puede definir (asignación de probabilidad contradictoria).
Caso Watson completo: cuatro personas en una habitación cerrada:
Bob, Jim, Sally y Karen; se va la luz menos de un minuto y al volver Karen ha sido
asesinada de una puñalada. Watson deduce que es cierto uno de: Bob (B), Jim (J),
Sally (S) culpable o su combinación. H={B,J,S}; potencia [∅,{B},{J},{S},{B,J},
{B,S},{J,S},{B,J,S}]. Masas iniciales m: ∅ 0; B 0.1; J 0.2; S 0.1; BJ 0.1; BS 0.1;
JS 0.3; BJS 0.1. Creencias (m / Bel): ∅ 0/0; B 0.1/0.1; J 0.2/0.2; S 0.1/0.1; BJ
0.1/0.4; BS 0.1/0.3; JS 0.3/0.6; BJS 0.1/1.0. Tras encontrar unas COLILLAS en un
cenicero y unas FACTURAS: reasigna mr: ∅ 0; B 0.2; J 0.1; S 0.05; BJ 0.05; BS 0.3;
JS 0.1; BJS 0.2. CONFLICTO (suma de productos con intersección vacía) =
0.2·0.2 + 0.1·0.2 + 0.3·0.2 + 0.1·0.1 + 0.1·0.1 + 0.1·0.1 + 0.1·0.05 + 0.2·0.05 +
0.1·0.05 + 0.05·0.1 + 0.2·0.3 + 0.1·0.1 = 0.245 (la tabla cruzada X×Y de las masas
m y mr); NORMALIZACIÓN = 1−0.245 = 0.755. Ejemplo de numerador: m3(B) =
[0.1·0.2 + 0.1·0.2 + 0.1·0.2 + 0.1·0.2 + 0.1·0.05 + 0.1·0.05 + 0.1·0.3 + 0.1·0.3 +
0.1·0.2]/0.755 = 0.17/0.755 = 0.225. Masas y creencias combinadas (m / Bel):
B 0.225/0.225; J 0.219/0.219; S 0.25/0.25; BJ 0.105/0.58; BS 0.04/0.484; JS
0.131/0.6; BJS 0.03/1.0 (suman 1).
[OJO] Las creencias de {B,J} y {B,S} del último cuadro (0.58 y 0.484) no coinciden
con la suma de masas de sus subconjuntos: Bel{B,J}=0.225+0.219+0.105=0.549 y
Bel{B,S}=0.225+0.25+0.04=0.515; los otros cuatro valores sí cuadran. (Comprobado: el conflicto 0.245 y el
numerador de m3(B)=0.17 SÍ salen de las masas; m3(S)=0.19/0.755=0.25 también.)

2. LÓGICA BORROSA (Logica_Borrosa_OLIVAS_VIU, 141 págs.)
2.1 Historia
Propuesta por Lotfi Zadeh en 1965. Cita literal: "Los
elementos clave en el pensamiento humano no son números, sino etiquetas.
Estas etiquetas permiten que los objetos pasen de pertenecer de una clase
a otra de forma suave y flexible." Se ve como extensión de la lógica
multivaluada de Lukasiewicz (1922, lógica trivaluada). Tras 1965,
profundización teórica (Zadeh, Trillas, Dubois, Prade); desde 1975,
aplicaciones (éxito en Japón: cámaras, lavadoras, ABS; frialdad inicial en
Europa/EE.UU., críticas de Kalman 1972).

2.2 Conjuntos borrosos: fundamentos
Conjunto crisp: función característica μA(x)∈{0,1}.
Conjunto borroso: función de pertenencia μA: X→[0,1].
Ejemplo canónico "edad" con 3 etiquetas, tabla exacta:
  Edad: 5 10  20 30  40  50  60  70  80
  joven: 1 1 0.8  0.5 0.2 0.1 0 0 0
  adulto:  0 0 0.8  1 1 1 1 1 1
  mayor: 0 0 0.1  0.2 0.4 0.6 0.8 1 1
Soporte: Sop(A) = {x∈X | μA(x)>0}. Notación A =
μ1/x1+...+μn/xn. Altura = mayor grado de pertenencia; Núcleo =
elementos con grado máximo; normalizado = algún elemento con grado 1.
α-corte: Aα = {x∈X | μA(x)≥α}. Ejemplo: Joven0.2 =
{5,10,20,30,40}. El núcleo es el α-corte de nivel 1.
Cardinalidad escalar: |A| = Σx∈X μA(x). Ejemplo:
|Mayor| = 0+0+0.1+0.2+0.4+0.6+0.8+1+1 = 4.1.
A⊆B (borroso) si μA(x)≤μB(x) ∀x. Convexidad borrosa: A es
convexo sii μA(λr+(1-λ)s) ≥ min[μA(r),μA(s)] ∀r,s,λ∈[0,1] (equivale a que
todos sus α-cortes sean convexos en sentido crisp).
Número borroso: conjunto borroso convexo, normalizado y con
función de pertenencia continua.

2.3 Operadores borrosos
Complemento: Ã(x)=1-μA(x). Unión: μA∪B(x)=max[μA(x),μB(x)].
Intersección: μA∩B(x)=min[μA(x),μB(x)].
Principio de extensión: generaliza f:X→Y a conjuntos borrosos. Si
varios x apuntan al mismo y, se toma el máximo de sus grados; en funciones
de varias variables, primero el mínimo dentro de cada tupla y luego el
máximo entre tuplas. Ejemplo: f:a→p,b→q,c→p con A=0.3/a+0.9/b+
0.5/c → B=f(A) = 0.5/p+0.9/q.
Complemento borroso axiomático c:[0,1]→[0,1] — C1 (c(0)=1,c(1)=0),
C2 (monótona decreciente), C3 (continua), C4 (involutiva: c(c(a))=a). Ejemplos involutivos: clásico c(a)=1-a; Sugeno
c_λ(a)=(1-a)/(1+λa); Yager c_ω(a)=(1-a^ω)^(1/ω).
T-normas (intersección) T:[0,1]²→[0,1] — axiomas: elemento
unidad T(a,1)=a, conmutativa, monótona, asociativa. Ejemplos: mínimo min(a,b); producto a·b; Lukasiewicz max(0,a+b-1); familia
de Yager Tw(a,b)=1-min[1,((1-a)^w+(1-b)^w)^(1/w)]. Cadena:
max(0,a+b-1) ≤ a·b ≤ min(a,b).
T-conormas (unión) ⊥:[0,1]²→[0,1] — axiomas análogos con
elemento cero ⊥(a,0)=a. Ejemplos: máximo max(a,b); producto
a+b-a·b; Lukasiewicz min(a+b,1); familia de Yager
⊥w(a,b)=min[1,(a^w+b^w)^(1/w)]. Cadena: max(a,b) ≤ a+b-a·b ≤ min(1,a+b).

2.4 Relaciones borrosas
Relación crisp R(X1,...,Xn)⊆X1×...×Xn. Relación binaria
borrosa: μR(x,y)∈[0,1].
Dominio (borroso): μdomR(x) = max(y∈Y) μR(x,y). Rango:
μranR(y) = max(x∈X) μR(x,y). Altura: h(R) = max(x,y) μR(x,y).
Composición max-min: μP∘Q(x,z) = max(y∈Y) min[μP(x,y),μQ(y,z)]. Alternativa max-producto: μP⊙Q(x,z) = max(y∈Y) [μP(x,y)·μQ(y,z)].
Ejemplo numérico completo con matrices P(4×3) y Q(3×2) dando
R=P∘Q (4×2) por max-min; segundo ejemplo comparando max-min vs.
max-producto sobre las mismas matrices P(3×3) y Q(3×4), con resultados
numéricos distintos para cada método.

2.5 Sistema borroso: definición y diseño
"Un Sistema Borroso es aquel que utiliza alguna de las técnicas
propias de la lógica borrosa bien sea en la representación de su
conocimiento, en la combinación de dicho conocimiento mediante diversos
operadores borrosos o en cualquier otra función propia de dicho sistema". Pasos de diseño: adquisición → representación (borrosificación) →
operadores/inferencia → desborrosificación (si aplica) → simulación.
Herramientas citadas: Fuzzy Toolbox de MATLAB, FuzzyCLIPS (NASA),
CubiCalc, TIL Shell.

2.6 Representación borrosa del conocimiento
La función de pertenencia se obtiene del experto del dominio, "no
está basada en la repetibilidad de las observaciones sino en la opinión de
un experto" — distinción clave frente a una distribución de
probabilidad.
Regla general: "Si x1 es A1,1 y ... y xn es An,1 Entonces y es B1". Cada dominio se divide en tantos conjuntos borrosos como el
experto considere, cada partición con su etiqueta lingüística. Formas
mostradas gráficamente (sin fórmula numérica dada en el PDF): triangular,
trapezoidal, acampanada.
Cercas semánticas / hedges: "Muy A" = A² (eleva al
cuadrado el grado de pertenencia); "Más o menos A" = A^0.5; "No A" =
complemento. Ejemplo: "números muy próximos a cero" = (1/(1+10x²))²
(cuadrado de la fórmula base de "próximos a cero", p.16 y p.76).

2.7 Razonamiento aproximado
Regla de composición de inferencias: B' = A'∘R, con
B'(y) = sup_x min[A'(x), R(x,y)]. La relación R de una regla "Si x
es A entonces y es B" se define vía una función de implicación:
R(x,y) = I(A(x),B(y)).
Modus Ponens Generalizado (MPG, p.81): Regla "Si x es A entonces y
es B"; Hecho "x es A'"; Conclusión "y es B'" (el modus ponens clásico es
el caso particular A'=A, B'=B).
Implicación borrosa: I:[0,1]²→[0,1], extensión de la implicación
clásica. Tres familias:
  - S-implicaciones I(a,b)=⊥(c(a),b): Kleene-Dienes max(1-a,b); Reichenbach
 1-a+ab; Lukasiewicz min(1-a+b,1). Se cumple I_b≤I_r≤I_a.
  - R-implicaciones I(a,b)=sup{x:T(a,x)≤b}: Gödel (1 si a≤b, si no b);
 Goguen (1 si a≤b, si no b/a); Lukasiewicz min(1,1-a+b) (es a la vez S
 y R). Se cumple I_g≤I≤I_a.
  - QL: I(a,b)=⊥(c(a),T(a,b)): Early-Zadeh max(1-a,min(a,b)); Klir y Yuan
 1-a+a²b.
Ejemplo completo MPG: X={x1,x2,x3}, Y={y1,y2}, A=0.5/x1+
1/x2+0.6/x3, B=1/y1+0.4/y2, implicación de Lukasiewicz →
R=1/x1y1+0.9/x1y2+1/x2y1+0.4/x2y2+1/x3y1+0.8/x3y2. Con hecho
A'=0.6/x1+0.9/x2+0.7/x3 → B'=0.9/y1+0.7/y2 (por sup-min).
Modus Tollens Generalizado: A'(x) = sup_y min[B'(y),
R(x,y)] — ejemplo con el mismo R y B' anteriores da A'=0.9/x1+0.9/x2+
0.9/x3.
4 tipos de proposiciones borrosas:
  1. No condicionada, no cualificada: "v es F" — grado de verdad = μF(v).
  2. No condicionada, cualificada: "v es F es S" — T(p)=S(F(v)); ejemplo
 "María, 26 años, joven en grado 0.87" → T(p)=0.76 (fórmula de S no
 detallada en el PDF).
  3. Condicionada, no cualificada: "Si x es A entonces y es B" —
 R(x,y)=I(A(x),B(y)); ejemplo con A=0.1/x1+0.8/x2+1/x3, B=0.5/y1+1/y2
 e implicación de Lukasiewicz.
  4. Condicionada, cualificada: "Si x es A entonces y es B es S" —
 combina los tratamientos de los casos 3 y 2.

2.8 Control borroso
Arquitectura general: valores medidos → borrosificación →
lógica de control (+ base de conocimiento) → desborrosificación → salida
crisp.
Aplicaciones comerciales citadas: depuradoras de agua,
control de tráfico, pilotaje de barcos, hornos de cemento, lavadoras
(Matsushita), aire acondicionado (Mitsubishi), cámaras (Sanyo), ABS/cruise
control (Mazda, Nissan).

**Enfoque de Mamdani**
Regla general con K reglas: "Si h1 es A(1) y...y hn es A(n)
Entonces y es B". Grado de aplicabilidad de una regla:
αr = min{μ_i1,r(1)(x1),...,μ_in,r(n)(xn)} — la conclusión de esa
regla se "corta" (recorta su altura) al nivel αr, y las salidas de todas
las reglas activas se combinan por MÁXIMO (unión).
Ejemplo numérico completo, péndulo/ángulo: R1 "Si θ es
positivo_pequeño y θ̇ es aprox._cero, Entonces F es positivo_pequeño"; R2
análoga con positivo_medio. Con θ=36°, θ̇=-2.25°/s: α1=min(0.4,0.8)=0.4,
α2=min(0.6,0.8)=0.6. Salida combinada con soportes en {1,3.5,4,6,7.5} y
niveles {0.4,0.6}.
3 métodos de desborrosificación:
  - Criterio del máximo: cualquier y del rango de máxima pertenencia
 (ejemplo: cualquier valor en [4,6]) — no determinista.
  - Media del máximo: valor medio de ese rango (ejemplo: 5).
  - Centro de gravedad: promedio ponderado por los grados (ejemplo:
 (0.4·1+0.4·3.5+0.6·4+0.6·6)/(0.4+0.4+0.6+0.6) = 3.9) — el más suave/
 continuo, pero más costoso computacionalmente.

**Enfoque de Takagi-Sugeno**
Misma partición borrosa en las entradas, pero la conclusión es una
función (normalmente lineal) de las entradas, no una etiqueta:
fr(x1,...,xn) = a1^(r)x1+...+an^(r)xn+a^(r). Salida crisp SIN
desborrosificación:
  h = [Σr αr·fr(x1,...,xn)] / [Σr αr]
Ejemplo completo "coche sorteando una curva": 4
entradas (distancia a esquina, a borde interior, ángulo, a borde
exterior), tabla de 20 reglas con coeficientes P0-P4. Con
δ1=10,δ2=30,δ3=0,δ4=50: solo R4 (α4=1/4) y R7 (α7=1/6) tienen grado >0.
f4=1.873, f7=2.820 → h = (3/5)·1.873+(2/5)·2.820 = **2.2518** (resultado
final del ejemplo, p.136-137).

2.9-bis ENUNCIADOS TRANSCRITOS de Ejercicios_LB_enunciados (9 págs.)
El PDF es una imagen escaneada (sin texto extraíble): la
versión anterior de este resumen solo describía los 11 ejercicios; aquí
quedan transcritos con TODOS sus datos, leídos de las imágenes. Autor:
José A. Olivas. NINGUNO trae solución en el PDF. Notación: "0.25/2" =
grado 0.25 para el elemento 2 (μ/x). T = t-norma, ⊥ = t-conorma, I =
función de implicación, C = complemento.

EJERCICIO DE INFERENCIA BORROSA 1
  Sistema experto borroso con variables X1, X2, Y. Universo de X1 y X2:
  A={1,2,3,4}. Universo de Y: B={a,b,c}.
  X1 grande  = 0.25/2 + 0.75/3 + 1/4
  X1 normal  = 0.5/1 + 1/2 + 0.25/3
  X2 grande  = 0.8/3 + 1/4
  X2 normal  = 1/2 + 0.6/3
  Y poco = 0.75/a + 0.25/b
  Y mucho = 0.75/b + 1/c
  Reglas: R1 Si X1 es grande y X2 es normal Entonces Y es poco.
 R2 Si X2 es muy grande Entonces Y es mucho.
  Conceptos: conjunción T(a,b)=min(a,b); agregación ⊥(a,b)=max(a,b);
  negación C(a)=1-a; implicación I(a,b)=max(1-a,b).
  Observación sobre el universo A: 0.2/1 + 0.6/2 + 0.8/3. ¿Qué inferirá el
  sistema en el universo B? Razonar detalladamente.
  [OJO] El enunciado da UNA sola observación sobre A para un sistema con
  dos variables de entrada (X1 y X2, ambas sobre A): hay que suponer que
  la misma observación se aplica a X1 y a X2. "Muy grande" = grande²
  (cercas semánticas, apartado 2.6).

EJERCICIO DE INFERENCIA BORROSA 2
  T(a,b)=max(0,a+b-1) (Łukasiewicz); ⊥(a,b)=min(a+b,1); implicación
  I(a,b)=min(1,1-a+b); complemento clásico; composición de relaciones
  max-min.
  f asocia un par de puntos con un punto: Y=f(x1,x2). Universos:
  x1: {α,β,γ}; x2: {r,s}; Y: {a,b,c}. La función f:
 (α,r)→c  (α,s)→a  (β,r)→a  (β,s)→c  (γ,r)→a  (γ,s)→b
  Conjunto borroso en x1: A = 0.2/α + 0.9/β + 0.5/γ.
  Conjuntos borrosos en x2: B = 0.7/r + 0.6/s ; C = 0.9/s.
  Se pide (numerados 8-12 en el PDF):
 8. Calcular los conjuntos borrosos D y E sobre Y con D=f(A,B) y E=f(A,C).
 ¿Qué principio de la lógica borrosa se ha de aplicar? (PRINCIPIO DE
 EXTENSIÓN, apartado 2.3, con varias variables: mínimo dentro de cada
 tupla y máximo entre tuplas).
 9. Conjunto borroso que exprese "D y E" y el que exprese "D ó E".
  10. Relación binaria borrosa (D y E → A) y la (A → C).
  11. Relación binaria J compuesta de las obtenidas en el punto 3 [sic]:
 J = (D y E → A) ∘ (A → C).
  12. Si se observa W = 0.1/a + 0.3/b + 0.5/c, ¿qué conjunto borroso se
 inferirá en el universo de x2 al usar la relación J? ¿Qué principio
 de la lógica borrosa se aplica?
  [OJO] Numeración 8-12 (empieza en 8 aunque es el segundo ejercicio) y en
  el punto 11 dice "obtenidas en el punto 3" cuando se refiere al punto 10.
  Dimensiones: (D y E → A) es una relación Y×x1 y (A → C) es x1×x2; su
  composición J es Y×x2; con W sobre Y el resultado queda sobre x2.

EJERCICIO DE INFERENCIA BORROSA 3 — metro
  Sistema experto para regular el tráfico del ferrocarril metropolitano.
  R1. Si la hora es punta de mañana entonces la frecuencia de paso de
 trenes es muy alta.
  R2. Si la frecuencia de paso de trenes es muy alta entonces el consumo
 de energía es alto.
  Universos: H (tipo de hora) {6,7,8,9,10}; F (frecuencia en segundos)
  {20,40,60,300}; C (consumo de energía) {100,1000,2000,4000}.
  punta_de_mañana = 0.4/7 + 1/8 + 0.3/9
  frecuencia_alta = 1/20 + 0.8/40 + 0.2/60
  consumo_alto = 0.5/1000 + 0.8/2000 + 1/4000
  Conceptos: T=min; ⊥=max; C(a)=1-a; I(a,b)=max(1-a,b).
  Se pide: 1) ¿Cuál sería la relación borrosa existente, y EN ESE ORDEN,
  entre hora punta de mañana y consumo de energía? (razonar y cuantificar).
  2) Dado que el día es lluvioso se considera la observación de hora
  punta 0.8/7 + 1/8 + 1/9: ¿qué conjunto borroso inferirá el sistema sobre
  la frecuencia de paso de trenes? Razonar detalladamente.
  3) ¿Cuál es la cardinalidad escalar del conjunto borroso resultante en la
  pregunta 2?
  Este ejercicio es el mismo problema que modela el ejemplo
  .clp "metro" con factores de certeza (BC_metro_cer.clp), visto desde la
  lógica borrosa.

EJERCICIO DE INFERENCIA BORROSA 4
  Regla: "Si la presión es grande y la temperatura alta, el consumo será
  elevado".
  Presión grande = {0.2/1 at., 0.5/3 at., 0.8/5 at.} (Universo: 1,3,5,7 at.)
  Temperatura alta = {0.3/70º, 0.9/95º} (Universo: 70º, 95º)
  Consumo elevado  = {0.2/10 kw., 0.4/20 kw., 0.8/30 kw.}
 (Universo: 10, 20, 30 kw/h)
  Motor de inferencia: T=min, ⊥=max, negación clásica, I(a,b)=max(1-a,b).
  Se observa que la presión es grande y la temperatura NO MUY ALTA. ¿Qué
  conjunto borroso inferirá el sistema experto sobre el consumo? ¿Cuál es
  su cardinalidad borrosa? Razonar con detalle.
  [OJO] El enunciado dice "cardinalidad borrosa"; en el curso se ha visto
  la cardinalidad ESCALAR (Σμ, apartado 2.2). "No muy alta" = 1-(alta)²
  (cercas semánticas: no + muy).

EJERCICIO DE INFERENCIA BORROSA 5
  Mismas características que el ejercicio 4 salvo: T(a,b)=max(0,a+b-1),
  ⊥(a,b)=min(a+b,1), I(a,b)=min(1,1-a+b), complemento clásico.
  Calor = {<20º/0.2, >20º y <32º/0.6, >32º/0.9}
  Aire acondicionado alto = {PosA/0.5, PosB/0.9}
  Reducir velocidad = {-10 km-h/0.3, -20 km-h/0.5, -30 km-h/0.8}
  Conocimiento: "Si hace mucho calor, poner el aire acondicionado alto,
  pero si se pone el aire acondicionado muy alto, reducir la velocidad".
  ¿Qué respuesta daría el sistema cuando la temperatura fuese de 36º?
  Razonar la respuesta y mostrar las operaciones llevadas a cabo.

EJERCICIO DE INFERENCIA BORROSA 6
  Regla: "Si los precios son altos [en el PDF 'grandes' aparece tachado y
  escrito a mano 'altos'], la demanda será grande".
  Precios altos  = {0.2/+0,2%, 0.5/+0,9%, 0.7/+1,3%}
  Demanda grande = {0.9/alta, 0.4/baja}
  Motor: T=min, ⊥=max, negación clásica, I(a,b)=max(1-a,b).
  Se observa que los precios son MUY ALTOS. ¿Qué conjunto borroso inferirá
  el sistema sobre la demanda? Razonar con detalle.

EJERCICIO DE CONTROL BORROSO 1 — Mamdani, 2 entradas X,Y
  Base de reglas (matriz: columnas X1,X2,X3; filas Y1..Y5; celda =
  conclusión Z-regla):
 X1 X2 X3
 Y1 Z1-r1 - Z1-r6
 Y2 - Z2-r3 -
 Y3 Z2-r2 Z2-r4 -
 Y4 - Z1-r5 Z3-r7
 Y5 - - Z3-r8
  (r1: X1∧Y1→Z1; r2: X1∧Y3→Z2; r3: X2∧Y2→Z2; r4: X2∧Y3→Z2; r5: X2∧Y4→Z1;
 r6: X3∧Y1→Z1; r7: X3∧Y4→Z3; r8: X3∧Y5→Z3.)
  Conjuntos borrosos (gráficas triangulares/trapezoidales, leídos del
  dibujo; valores aproximados):
 X (universo 0-6): X1 = 1 hasta ~1.5 y baja a 0 en 3; X2 triángulo
 1-3-5 (pico en 3); X3 sube de 3 a 4 (=1 en 4) y sigue en 1 hasta 6.
 Marcas del eje: 0,1,1.5,2,3,4,5,6.
 Y (universo 0-12): Y1 = 1 en 0 y baja a 0 en ~4; Y2 triángulo 2-4-6;
 Y3 triángulo 4-6-8; Y4 triángulo 6-8-10; Y5 sube de 8 a 12.
 Z (universo 0-50): Z1 = 1 en 0 y baja a 0 en ~20; Z2 triángulo
 10-25-40; Z3 sube de 30 a 50.
  Sensores: X=3.5 e Y=7.5. Se pide: (1) Representar gráficamente las
  reglas que se disparan. (2) Representar el conjunto borroso obtenido
  antes de desborrosificar. (3) Indicar núcleo y soporte del conjunto
  obtenido; ¿cuál es su α-corte α_0.25? (4) Desborrosificar utilizando
  TODOS los criterios que conozca (máximo, media del máximo, centro de
  gravedad). Explicar el resultado.
  [OJO] Los vértices exactos salen de un dibujo escaneado; comprobar sobre
  el PDF antes de usarlos en un cálculo de examen.

EJERCICIO DE CONTROL BORROSO 2 — los dos aviones (Barajas)
  Dos aviones, misma maniobra de aproximación para tomar tierra en Barajas,
  con los mismos sensores en las alas (V1) y en la cola (V2) (velocidad de
  paso del aire, para evaluar la sustentación) y el mismo regulador de
  potencia de motores, escala de 1 a 10.
  V1 y V2 (universo 0-6 m/seg; marcas 0..6): Baja = (0 1)(1 1)(3 0);
 Media = (1 0)(3 1)(5 0); Alta = (3 0)(5 1)(6 1).
  Potencia motores (universo 0-10): Muy poca = (0 1)(1 1)(3 0); Poca =
 (1 0)(3 1)(5 0); Media = (3 0)(5 1)(7 0); Alta = (5 0)(7 1)(9 0);
 Muy alta = (7 0)(9 1)(10 1).
  [Las definiciones exactas se han tomado del archivo real BC_ej18_fuz.clp,
 que coincide con el dibujo del PDF; el bloque 3.4 lo confirma.]
  AVION1: controlador Mamdani, desborrosificación por MEDIA DEL MÁXIMO.
 R1 V1 baja y V2 baja → potencia muy alta
 R2 V1 baja y V2 media → alta
 R3 V1 baja y V2 alta → media
 R4 V1 media y V2 baja → alta
 R5 V1 media y V2 media → media
 R6 V1 media y V2 alta → poca
 R7 V1 alta y V2 baja → media
 R8 V1 alta y V2 media → poca
 R9 V1 alta y V2 alta → muy poca
  AVION2: controlador Takagi-Sugeno; conclusión Pr = P0 + P1·V1 + P2·V2
 (formato de la tabla del PDF, columnas V1, V2, P0, P1, P2):
 R1 Alta  Alta 1.6  0.5  0.9
 R2 Media Alta 3.2  5.2  2.6
 R3 Baja  Alta 0.8  1.5  3.4
 R4 Alta  Media  0.7  0.2  0.4 (a mano: P0 → 0.8 y P2 → 1)
 R5 Media Media  2.4  0.6  0.9 (a mano: P0 → 0.6)
 R6 Baja  Media  1.9  0.5  2.3
 R7 Alta  Baja 2.6  1.3  0.6
 R8 Media Baja 0.6  1.5  0.9
 R9 Baja  Baja 1.6  0.4  4.2
  En un momento dado ambos aviones miden V1=4.5 y V2=3. ¿Qué potencia
  aplicará cada uno a los motores? Mostrar con detalle todos los cálculos.
  [OJO] En R4 y R5 hay correcciones manuscritas sobre los valores impresos
  (0.7→0.8, 0.4→1, 2.4→0.6). El PDF no aclara si las manuscritas sustituyen
  a las impresas. La fórmula de la conclusión (P0+P1V1+P2V2) es la forma
  lineal de Takagi-Sugeno de 2.8; el enunciado solo rotula las columnas
  P0, P1, P2. Ver el archivo BC_ej18_fuz.clp / BH_ej18_fuz.CLP (bloque 3.4),
  que modela la parte Mamdani con V1=4.5, V2=3.

EJERCICIO DE CONTROL BORROSO 3 — secado, Takagi-Sugeno
  Un ventilador regula su velocidad según la temperatura del producto
  (controlador borroso de Takagi-Sugeno). Universo de temperatura [0,70]°C.
  Temperatura (marcas 15,25,35,45,55): baja = 1 hasta 25 y baja a 0 en 35;
  media = triángulo 15-35-55 (pico en 35); alta = sube de 35 a 45 y 1
  después. [leído del dibujo]
  Base de reglas (Temperatura, p0, p1): R1 Alta 700 500; R2 Media 100 200;
  R3 Baja 100 50. (p0 y p1 son los coeficientes de la función consecuente:
  velocidad = p0 + p1·T.)
  Se observa un producto a 40°C. Se pide: (1) valores borrosificados de la
  observación; (2) representar gráficamente las reglas que se activan;
  (3) grado de aplicabilidad de cada regla activada; (4) calcular la
  velocidad del ventilador a la salida del controlador.

EJERCICIO DE CONTROL BORROSO 4 — válvula (enunciado manuscrito)
  Base de reglas (Tª, Presión, P0, P1, P2):
 R1 Baja  Grande  100  50  190
 R2 Media Grande  200  60  180
 R3 Alta - 300  70 0
 R4 Baja - 400  80 0
  Temperatura (eje en °C, marcas -70,-50,-40,-30,-10): Baja = 1 hasta -70
  y baja a 0 en -50; Media = triángulo -70, -40 (pico), -10; Alta sube
  desde -30 y llega a 1 (a la derecha de -10, mesetas). Presión (atm):
  "grande" sube de 0 en 3 a 1 en 6. Lectura: Tª = -15°C; P = 4 atm.
  Pregunta: ¿Válvula? (calcular la salida del controlador Takagi-Sugeno,
  de la forma P0 + P1·Tª + P2·P por regla, ponderada por los grados de
  aplicabilidad). [OJO] El escrito a mano es apenas legible en varios
  vértices; el enunciado no dice explícitamente el orden de las
  variables de las columnas P1 y P2 (se asume Tª y Presión, como en las
  columnas del antecedente).

EJERCICIO DE CONTROL BORROSO 5 — Mamdani con 3 entradas
  Controlador Mamdani con tres variables de entrada X1, X2, X3 y una de
  salida Y; desborrosificación por MEDIA DE LOS MÁXIMOS. Universo de X1,
  X2, X3: [0,10]; universo de Y: [0,6].
  Cinco conjuntos triangulares (a,b,c) sobre X1,X2,X3 (a=grado 0 a la
  izquierda, b=grado 1, c=grado 0 a la derecha):
 Muy bajo (0,0,2); Bajo (1,3,4); Normal (3,5.5,7); Alto (6,7.5,9);
 Muy alto (8,10,10)
  Tres conjuntos triangulares sobre Y: Poco (0,0,2); Medio (1,3,5);
  Mucho (4,6,6).
  Reglas: R1 X1 Bajo, X2 Normal, X3 Bajo → Y Mucho
 R2 X1 Normal, X2 Alto, X3 Muy alto → Y Poco
 R3 X1 Bajo, X2 Alto, X3 Bajo → Y Medio
  Observación: X1=3.5, X2=6.5, X3=3. Se pide: 1) valores borrosificados
  de las observaciones; 2) razonar el grado de aplicabilidad de cada regla
  activada; 3) Si se desea que ante estas observaciones se obtuviese un
  conjunto borroso de salida con máximo grado de pertenencia 0.5 y cuya
  desborrosificación fuese 5, ¿qué regla se debería añadir a la base de
  conocimientos? Razonar.
  [OJO] "Para definir la variable temperatura es Y" en el enunciado: Y es
  la variable de salida (rotulada "temperatura" por error de copia).

2.10 COMPLEMENTOS al bloque 2 (detalles de las 141 diapositivas de
 Logica_Borrosa no recogidos arriba; revisión página a página del PDF)
Historia: la lógica multivaluada de Łukasiewicz supone valores de
verdad en [0,1] como generalización de su lógica trivaluada; trabajos amplios de
Rosser y Rescher; en los años 30 se proponen lógicas multivaluadas para cualquier
número n≥2 de valores de verdad, racionales en [0,1]: {0=0/(n−1), 1/(n−1),
2/(n−1),..., (n−2)/(n−1), (n−1)/(n−1)=1}. La lógica borrosa incluye: PREDICADOS
borrosos (caro, alto, raro, peligroso), CUANTIFICADORES borrosos (mucho, parecido,
casi todo), VALORES DE VERDAD borrosos (muy cierto, más o menos cierto) y CERCAS
SEMÁNTICAS (semantic fences: muy, algo...). Tras 1965: profundización teórica
(Zadeh, Trillas, Dubois, Prade); desde 1975 aplicaciones, primeras con éxito en
control; Japón de gran penetración; frialdad en Europa y EE.UU. (críticas de Kalman
1972 y Mac Lane: "frivolidad de los conceptos y sin obtención de resultados"); en
Japón el éxito fue total (cámaras, lavadoras, ABS), casi todo en control; la llama
se mantuvo en Europa y EE.UU. y desde los 80, apoyada en el éxito japonés, se afianza.
Conceptos previos crisp: conjunto universal X; A⊆X; x∈A / x∉A.
Descripción: por LISTAS (A={a1..an}) o por PROPIEDADES/REGLAS (B={b | b tiene P1..Pm}).
FUNCIÓN CARACTERÍSTICA μA(x)=1 sii x∈A, 0 sii x∉A; μA: X→{0,1}. CARDINALIDAD |A| =
nº de elementos; CONJUNTO POTENCIA = familia de todos los subconjuntos de A, con
|P(A)|=2^|A|. Ejemplo "persona baja" (A: altura<1.70): a=1.80, b=1.75, c=1.71,
e=1.70, f=1.79 no pertenecen (μ=0); d=1.60, g=1.69, h=1.68, i=1.65 sí (μ=1).
Versión BORROSA del mismo ejemplo: μ(a)=0, μ(b)=0.4, μ(c)=0.8, μ(e)=0.9, μ(f)=0,
μ(d)=μ(g)=μ(h)=μ(i)=1 [dato tal cual de la diapositiva; ver [OJO] al final].
Funciones de pertenencia: "números reales próximos a cero":
μ(x)=1/(1+10x²); "muy próximos a cero": μ(x)=(1/(1+10x²))²; "próximos a un valor
a": μ(x)=1/(1+10(x−a)²). Aunque [0,1] es el rango habitual, cualquier conjunto con
ordenación total o parcial sirve: A: X→L, "conjuntos borrosos L-fuzzy (L = lattice)".
Ejemplo edad: X={5,10,20,30,40,50,60,70,80} (5 = menor de 5 años;
10 = entre 5 y menor que 10...). Tabla joven/adulto/mayor ya en 2.2. SOPORTE
Sop(A)={x∈X | μA(x)>0}; Sop(joven)={5,10,20,30,40,50}. ALTURA de Mayor=1; NÚCLEO de
Mayor={70,80}; "Joven, Adulto y Mayor son normalizados". α-CORTES: Joven0.2={5,10,20,
30,40}; Joven0.8={5,10,20}; Joven1={5,10}; el núcleo de un conjunto normalizado es
su α-corte de nivel 1. CONJUNTO NIVEL de A = conjunto de sus distintos α-cortes o
niveles α∈[0,1]: Λ_A={α | μA(x)=α para algún x∈X}.
Cardinalidad ESCALAR: |A|=Σ_{x∈X} μA(x); |Mayor|=0+0+0.1+0.2+0.4+0.6+0.8+1+1
=4.1. Cardinalidad BORROSA: conjunto borroso |A|'= Σ_{i=1..n} α_i / n_i donde α_i es
un α-corte de A y n_i el nº de elementos del universo con grado ≥ α_i; ejemplo:
|Mayor|' = 0.1/7 + 0.2/6 + 0.4/5 + 0.6/4 + 0.8/3 + 1.0/2. (Es la "cardinalidad
borrosa" que pide el Ejercicio de Inferencia Borrosa 4.)
Subconjunto: A⊆B sii μA(x)≤μB(x) ∀x (ej. Mayor ⊆ Adulto); igualdad: μA(x)=μB(x)
∀x. CONVEXIDAD crisp en R^n: para r,s∈A y λ∈[0,1], el punto t=(λ·ri+(1−λ)·si)∈A
(los puntos del segmento que los une pertenecen a A). Un conjunto borroso es
CONVEXO sii cada uno de sus α-cortes es convexo crisp: μA(λr+(1−λ)s) ≥ min[μA(r),
μA(s)] ∀r,s reales, λ∈[0,1] (figuras: convexo vs. NO convexo). NÚMERO BORROSO =
conjunto borroso convexo, normalizado y con función de pertenencia continua
(ejemplo: el número borroso "cero" con μ=1/(1+10x²)).
Operadores con ejemplos: complemento Ã=1−μA; "Mayor" =
{1/5,1/10,0.9/20,0.8/30,0.6/40,0.4/50,0.2/60} (complemento de Mayor);
Joven∪Mayor = 1/5+1/10+0.8/20+0.5/30+0.4/40+0.6/50+0.8/60+1/70+1/80;
Joven∩Mayor = 0.1/20+0.2/30+0.2/40+0.1/50. Los conjuntos borrosos se
operan como los crisp con negación 1−μ, unión max e intersección min; las
diapositivas 36-38 muestran una escala 0-1 con MÍN y MÁX como extremos y sobre
ellos las t-normas ("y"), las t-conormas ("ó") y, entre ambos, las "FUNCIONES DE
AGREGACIÓN" (OWA, medias...).
Principio de extensión — detalle: f:X→Y y A=μ1/x1+..+μn/xn ⇒
f(A)=μ'1/f(x1)+..+μ'n/f(xn). Si varios x van al mismo y: máximo (μ'1=max(μ1,..,μn)).
Si varias TUPLAS apuntan a un y: mínimo de los grados de la tupla, y máximo entre
tuplas: μ'1=max[min(μ11,μ21), min(μ13,μ23)]. Ejemplo 1 (2.3): B=0.5/p+0.9/q. Ejemplo
2 (dos variables): x1={a,b,c}, x2={x,y}, Y={p,q,r}; A1=0.3/a+0.9/b+0.5/c; A2=0.5/x+1/y;
las tuplas (a,x)→p, (a,y)→p, (b,x)→q, (b,y)→r, (c,x)→r, (c,y)→p [leído del diagrama];
B=f(A1,A2): μB(p)=max[min(0.3,0.5),min(0.3,1),min(0.5,1)]=0.5; μB(q)=min(0.9,0.5)=0.5;
μB(r)=max[min(0.5,0.5),min(0.9,1)]=0.9 ⇒ B=0.5/p+0.5/q+0.9/r.
Complemento borroso: función c:[0,1]→[0,1] con C1) c(0)=1, c(1)=0;
C2) monotonía: a≤b ⇒ c(a)≥c(b) (el PDF escribe "c(a) ≤ c(b)": la definición
correcta es NO creciente). C1 y C2 dan los complementos más generales, p.ej. el
UMBRAL c(a)=1 si a≤t, 0 si a>t, con t∈[0,1). Requisitos prácticos: C3) c continua;
C4) c involutiva: c(c(a))=a. Ejemplo continua pero NO involutiva: c(a)=0.5·(1+cos(πa)):
c(0.33)≈0.75 y c(0.75)≈0.15 (no vuelve a 0.33). Involutivos: clásico 1−a; SUGENO
c_λ(a)=(1−a)/(1+λa), λ∈(−1,∞) (curvas para λ=0, −0.5, −0.9, 10, 2); YAGER
c_w(a)=(1−a^w)^(1/w), w∈(0,∞) (curvas w=1, 2, 5, 0.5).
Intersección borrosa: T:[0,1]²→[0,1], μA∩B(x)=T[μA(x),μB(x)],
axiomas I1) T(a,1)=a (elemento unidad); I2) conmutativa; I3) monótona (a≤a', b≤b' ⇒
T(a,b)≤T(a',b')); I4) asociativa. Recomendados: I5) continua; I6) T(a,a)<a
"subidempotente" (el PDF escribe "≤"); una T-norma continua y subidempotente se
llama ARQUIMEDEA. Ejemplos: mínimo, producto a·b, Łukasiewicz max(0,a+b−1); CLASE
DE YAGER T_w(a,b)=1−min[1,((1−a)^w+(1−b)^w)^(1/w)]: T_1=1−min(1,2−a−b)=Łukasiewicz;
T_2=1−min(1,√((1−a)²+(1−b)²)); lím_{w→∞} T_w = min(a,b). Cadena de cotas:
max(0,a+b−1) ≤ a·b ≤ min(a,b).
Unión borrosa: ⊥ con U1) ⊥(a,0)=a (elemento cero); U2)
conmutativa; U3) monótona; U4) asociativa; recomendados U5) continua; U6) ⊥(a,a)>a
"superidempotente"; T-conorma continua superidempotente = ARQUIMEDEA. Ejemplos:
máximo; producto (suma probabilística) a+b−ab; Łukasiewicz min(1,a+b); clase de
Yager (no idempotentes) ⊥_w(a,b)=min[1,(a^w+b^w)^(1/w)]: ⊥_1=min(1,a+b);
⊥_2=min(1,√(a²+b²)); lím_{w→∞} ⊥_w = max(a,b). Cadena: max(a,b) ≤ a+b−ab ≤
min(1,a+b).
Relaciones borrosas — detalle: una relación crisp R(X1..Xn)⊆
X1×..×Xn es un conjunto por sí mismo (se le aplican los operadores de conjuntos); su
función característica vale 1 para las tuplas de la relación y 0 en otro caso;
relación entre dos conjuntos = BINARIA. Ejemplo "muy cerca" entre ciudades
{Cádiz, Sevilla, Ciudad Real, Madrid, Toledo} (orden C,S,CR,M,T), matriz crisp: C-
C=1, C-S=1, S-S=1, CR-CR=1, CR-T=1, M-M=1, M-T=1, T-T=1 (simétrica); versión
borrosa: C: (1, 0.9, 0.2, 0, 0); S: (0.9, 1, 0.8, 0, 0); CR: (0.2, 0.8, 1, 0.6, 0.9);
M: (0, 0, 0.6, 1, 0.9); T: (0, 0, 0.9, 0.9, 1). Representación matricial y gráfica de
una relación binaria borrosa (ejemplo X={x1..x6}, Y={y1..y5}): DOMINIO dom R(x) =
max_y μR(x,y) → 1/x1+0.4/x2+1/x3+0.4/x4+0.5/x5+0.2/x6; RANGO ran R(y)=max_x μR(x,y) →
0.9/y1+1/y2+1/y3+0.2/y4+0.5/y5; ALTURA h(R)=max_{x,y} μR(x,y)=1. Descomposición en
α-cortes: R=∪_{α∈Λ_R} α·R_α con μ_{αR_α}(x,y)=α·μ_{R_α}(x,y); ejemplo con conjunto
nivel {0, 0.4, 0.7, 0.9, 1}: R=0.4·R_0.4 ∪ 0.7·R_0.7 ∪ 0.9·R_0.9 ∪ 1·R_1 (R_0.4 y R_0.7
son relaciones crisp de la matriz).
Composición: en crisp R(X,Z)=P(X,Y)∘Q(Y,Z), con propiedades P∘Q ≠
Q∘P (no conmutativa), (P∘Q)⁻¹=Q⁻¹∘P⁻¹, (P∘Q)∘R=P∘(Q∘R) (asociativa). En borrosa: la
más extendida max-min μP∘Q(x,z)=max_y min[μP(x,y),μQ(y,z)]; alternativa max-producto
μP·Q(x,z)=max_y[μP(x,y)·μQ(y,z)]. Ejemplo 1 (P 4×3, Q 3×2): P: x1:(0.7,0.5,0), x2:
(1,0,0), x3:(0,1,0), x4:(0,0.4,0.3); Q: a:(0.6,0.8), b:(0,1), c:(0,0.9) [filas de Y=
{a,b,c}, columnas de Z={α,β}]; R=P∘Q (max-min): x1:(0.6,0.7), x2:(0.6,0.8), x3:
(0,1), x4:(0,0.4). Ejemplo 2 (P 3×3, Q 3×4): P: x1:(0.3,0.5,0.8), x2:(0,0.7,1), x3:
(0.4,0.6,0.5); Q: y1:(0.9,0.5,0.7,0.7), y2:(0.3,0.2,0,0.9), y3:(1,0,0.5,0.5); max-min:
x1:(0.8,0.3,0.5,0.5), x2:(1,0.2,0.5,0.7), x3:(0.5,0.4,0.5,0.6); max-producto:
x1:(0.80,0.15,0.40,0.45), x2:(1.00,0.14,0.50,0.63), x3:(0.50,0.20,0.28,0.54).
Sistema borroso: implantación: (a) programas EMBEBIDOS en
aplicaciones (la más común; C, C++, Python, Matlab, FuzzyCLIPS...); (b) programas
fuente cargados en CHIPS; (c) circuitería ANALÓGICA. Herramientas: Fuzzy toolbox
de MATLAB (MathWorks), FuzzyCLIPS (NASA), CubiCalc (Hyperlogic Corp.), TIL Shell
(Togai InfraLogic) y muchas más libres y de pago.
Construcción de conjuntos borrosos: participación de expertos:
preguntas directas (métodos directos) o preguntas más sencillas procesadas después
(métodos indirectos), con uno o varios expertos → cuatro métodos: directos con un
experto, directos con múltiples expertos, indirectos con un experto, indirectos con
múltiples expertos. Cada predicado simple de la regla se representa por un
conjunto borroso; el valor crisp de la variable pertenece con cierto grado al
conjunto que especifica la premisa. Cercas semánticas más usadas: Muy A=
A²; Más o menos A=A^0.5; No A=1−μ; No muy A=1−μ²; No más o menos A=1−μ^0.5.
Implicaciones — derivación de las familias: en lógica clásica
I(a,b)=a→b se puede escribir de varias formas equivalentes; sus extensiones no
son equivalentes: (1) I(a,b)=¬a∨b → I=⊥(c(a),b) (S-implicaciones); (2) I(a,b)=max{x∈
{0,1} | a∧x ≤ b} → I(a,b)=sup{x∈[0,1] | T(a,x)≤b} (R-implicaciones); (3) I(a,b)=a'∨
(a∧b) → ⊥(c(a),T(a,b)) (QL, ley de absorción); (4) I(a,b)=(a'∧b')∨b → ⊥(T(c(a),
c(b)),b). Con negación clásica: KLEENE-DIENES Ib=max(1−a,b) (la S-implicación más
pequeña, ⊥=max); REICHENBACH Ir=1−a+ab (⊥=a+b−ab); ŁUKASIEWICZ Ia=min(1,1−a+b) (⊥=
min(a+b,1)); Ib≤Ir≤Ia. R: GÖDEL Ig=1 si a≤b, b si a>b (T=min; la R-implicación más
pequeña); GOGUEN Ig'=1 si a≤b, b/a si a>b (T=producto); ŁUKASIEWICZ Ia=sup{x |
max(0,a+x−1)≤b}=min(1,1−a+b) (es a la vez S y R); Ig≤I≤Ia. QL: EARLY-ZADEH Im=max(1−a,
min(a,b)); KLIR Y YUAN Ip=1−a+a²b (T=producto, ⊥=a+b−ab).
SELECCIÓN de función de implicación: "un problema difícil, aún
sin resolver". Con la proposición condicional p: si x es A entonces y es B (R(x,y)=
I(A(x),B(y))), el MPG B'=A'∘R debe coincidir con el clásico cuando A'=A: B(y)=
sup_x min[A(x), I(A(x),B(y))] ∀ A y B. Otro criterio: que se mantenga el MODUS
TOLLENS: c(A(x))=sup_y min[c(B(y)), I(A(x),B(y))].
Ejemplo MPG y MTG: ya en 2.7 (Łukasiewicz; B'=0.9/y1+0.7/y2 y
A'=0.9/x1+0.9/x2+0.9/x3, por sup-min con R=1/x1y1+0.9/x1y2+1/x2y1+0.4/x2y2+1/x3y1+
0.8/x3y2). Detalle: B'(y2)=max[min(0.6,0.9),min(0.9,0.4),min(0.7,0.8)]=0.7.
Proposiciones borrosas — detalle: (1) no condicionada no
cualificada "p: v es F": F conjunto borroso en V; T(p)=μF(v); ejemplo con T (temp)
en 0-50°C: 18°C es "baja" en grado 0.4 y "normal" en grado 0.9. (2) no
condicionada cualificada "p: v es F es S": S = CALIFICADOR DE VERDAD borroso
(entre "absolutamente falso" y "absolutamente verdadero"); T(p)=S(F(v)); ejemplo:
"María es joven es muy cierto"; con 26 años María pertenece a joven en grado 0.87
(y "muy joven" en el gráfico se lee ≈0.36); T(p)=0.76 [valor que coincide con 0.87²=
0.757, es decir "muy cierto" ≈ cuadrado; el PDF solo dice que "depende no solo
del conjunto borroso sino de la fuerza de la verdad"]. (3) condicionada no cualificada
"p: Si x es A entonces y es B": R(x,y)=I[A(x),B(y)] son los valores de verdad;
ejemplo Łukasiewicz: A=0.1/x1+0.8/x2+1/x3, B=0.5/y1+1/y2 → R=1/x1y1+1/x1y2+0.7/x2y1+
1/x2y2+0.5/x3y1+1/x3y2; T(p)=1.0 en (x1,y1), 0.7 en (x2,y1). (4) condicionada
cualificada "Si x es A entonces y es B es S": se combinan los casos 3 y 2 (ej. "Si
la temperatura es alta, entonces el día será soleado es muy cierto").
Control: la teoría de control clásica se apoya en dos hipótesis:
A) el sistema a controlar es CONOCIDO y su conocimiento se recoge en un modelo con
parámetros identificables; B) el objetivo de control se especifica con fórmulas
matemáticas concisas. Al crecer la complejidad o ser difícil expresar el
comportamiento, las hipótesis fallan → nace el CONTROL EXPERTO (cálculo simbólico,
lógica heurística para reguladores simples o multivariables); la LB aporta el
tratamiento de la vaguedad y un mejor modelado. Primeros controladores borrosos en la
literatura: 1974; dos periodos: experimentos de laboratorio y prototipos, y
explosión comercial a finales de los 80. Aplicaciones: depuradoras de agua,
control de tráfico, pilotaje de barcos, hornos de cemento, lavadora con control
borroso (Matsushita Electrical), aire acondicionado (Mitsubishi Heavy Industry),
videocámaras de 8 mm (Sanyo), Bosch Eco-fuzzy, ABS/cruise control de Mazda y
Nissan. Observaciones: (a) se usan en entornos donde ya se ha trabajado
mucho con éxito (hay experiencia y fuente de información sobre las políticas de
control); (b) los sensores añadidos no son caros (no se necesita precisión
importante); (c) el tiempo de desarrollo suele ser menor que con control clásico.
Arquitectura: valores medidos → interfaz de borrosificación → lógica de
control (con base de conocimientos) → interfaz de desborrosificación → salida del
controlador → sistema controlado (lado BORROSO entre las dos interfaces; el resto NO
borroso).
Mamdani — detalle: las K reglas definen una FUNCIÓN A TROZOS
(h=φ(H1..Hn): si H1≈A^(1)_{i1,k} y..., h≈B_ik) "más que una inferencia propiamente
dicha". Ejemplo de conjuntos del ángulo (−90°,90°): negativo grande, negativo medio,
negativo pequeño, cero, positivo pequeño, positivo medio, positivo grande (nb, nm, ns,
az, ps, pm, pb). Tabla de reglas 7×7 con etiquetas (nb..pb) que "puede no estar
completamente llena". Desborrosificación: (i) CRITERIO DEL MÁXIMO: cualquier valor de Y
con máximo grado; VENTAJA: aplicable a conjuntos borrosos arbitrarios y cualquier
dominio de control; DESVENTAJA: no especifica cuál elegir; si se elige al azar el
controlador es NO DETERMINISTA y puede dar acciones de control DISCONTINUAS;
(ii) MEDIA DEL MÁXIMO: si Max(salida) no es vacío, valor medio del conjunto máximo;
puede dar acciones discontinuas (salta de un valor a otro a intervalos de máximo grado);
(iii) CENTRO DE GRAVEDAD: VENTAJA: comportamiento suave (continuo) y tiene en cuenta
las reglas por su grado de aplicabilidad; DESVENTAJA: difícil justificación semántica y
más tiempo de cálculo. Ejemplo: 3.9 = (0.4·1+0.4·3.5+0.6·4+0.6·6)/(0.4+0.4+0.6+0.6).
Takagi-Sugeno — detalle: el ejemplo del COCHE que sortea una curva
a velocidad constante: entradas e1 distancia a la esquina más cercana, e2 distancia al
borde interior, e3 dirección (ángulo) del coche, e4 distancia al borde exterior; salida
h = giro del volante. Dominios: X1,X2,X4∈[0,150] cm, X3∈[−90,90]°. Conjuntos:
e1: pequeño/medio/grande (puntos 30,50,60,70,90,140); e2: pequeño/grande (20,40,80);
e3: outwards/forward/inwards (−60,−30,−20,20,30,60); e4: pequeño (20,40). Reglas:
Rr: Si e1 es A y e2 es B y e3 es C y e4 es D Entonces m = P0 + P1·e1 + P2·e2 + P3·e3 + P4·e4
con A∈{small,medium,big}, B∈{small,big}, C∈{outwards,forward,inwards}, D∈{small}.
Base de 20 reglas (e1, e2, e3, e4 | P0, P1, P2, P3, P4; "-" = sin condición):
 R1 - - outwards pequeño | 3.000 0 0 −0.045 −0.004
 R2 - - forward pequeño | 3.000 0 0 −0.030 −0.090
 R3 pequeño pequeño outwards - | 3.000 −0.041 0.004 0 0
 R4 pequeño pequeño forward - | 0.303 −0.026 0.061 −0.050 0
 R5 pequeño pequeño inwards - | 0.000 −0.025 0.070 −0.075 0
 R6 pequeño grande outwards - | 3.000 −0.066 0 −0.034 0
 R7 pequeño grande forward - | 2.990 −0.017 0 −0.021 0
 R8 pequeño grande inwards - | 1.500 0.025 0 −0.050 0
 R9 medio pequeño outwards - | 3.000 −0.017 0.005 −0.036 0
 R10 medio pequeño forward - | 0.053 −0.038 0.080 −0.034 0
 R11 medio pequeño inwards - | −1.220 −0.016 0.047 −0.018 0
 R12 medio grande outwards - | 3.000 −0.027 0 −0.044 0
 R13 medio grande forward - | 7.000 −0.049 0 −0.041 0
 R14 medio grande inwards - | 4.000 −0.025 0 −0.100 0
 R15 grande pequeño outwards - | 0.370 0 0 −0.007 0
 R16 grande pequeño forward - | −0.900 0 0.034 −0.030 0
 R17 grande pequeño inwards - | −1.500 0 0.005 −0.100 0
 R18 grande grande outwards - | 1.000 0 0 −0.013 0
 R19 grande grande forward - | 0 0 0 −0.006 0
 R20 grande grande inwards - | 0 0 0 −0.010 0
Entradas del ejemplo: e1=10, e2=30, e3=0°, e4=50. Fuzzificación: e1=10 → small 0.8,
medium 0, big 0; e2=30 → small 0.25, big 0.167; e3=0 → outwards 0, forward 1, inwards
0; e4=50 → small 0. Solo R4 y R7 tienen α≠0: α4=min(0.8,0.25,1)=1/4; α7=min(0.8,0.167,1)=
1/6. Consecuentes: m4=0.303−0.026·10+0.061·30−0.050·0+0·50=1.873; m7=2.990−0.017·10+0·30−
0.021·0+0·50=2.820. Salida h=(1/4·1.873+1/6·2.820)/(1/4+1/6)=(3/5)·1.873+(2/5)·2.820=
2.2518. El PDF termina con la diapositiva "¡Hasta siempre Lotfi!" (in memoriam Zadeh).
[OJO] Erratas/imprecisiones de las diapositivas: (a) p.16: "el número 3 tiene grado
0.1 y el 1 grado 0.9" no corresponde a μ=1/(1+10x²) (da μ(1)=0.0909 y μ(3)=0.011;
0.9 y 0.1 serían aprox. μ(0.1) y μ(1)); (b) p.29: el "complemento de Mayor" mostrado
tiene 0.3/30 y 0.6/40, pero 1−μ_mayor da 0.8/30 y 0.6/40 [el segundo coincide]; (c) p.30:
Joven∩Mayor se escribe "1/20" (debe ser 0.1/20); (d) C2: "c(a)≤c(b)" es un error de
signo (monotonía decreciente); (e) p.13-15: "persona baja" con μ(1.70)=0.9 y μ(1.75)
=0.4 es una función de pertenencia elegida por el profesor, no derivada de una
fórmula; (f) p.98: "muy joven" = 0.36 no cuadra con 0.87² (=0.76), que es el valor
de T(p) de la p.99.

3. CLIPS Y FUZZYCLIPS (CLIPS_FUZZYCLIPS_OLIVAS_VIU, 45 págs. + 6 pares de .clp reales)
3.1 CLIPS: motor de reglas clásico
"Shell para la elaboración de Sistemas Expertos creada por la NASA
en 1986 (v6.1). C Language Integrated Production System. Sistema de
producción con encadenamiento hacia delante".
Nomenclatura: hechos=facts, reglas=rules, conjunto
conflicto=agenda, inferir=run. Sintaxis basada en LISP (todo entre
paréntesis).
Comandos de hechos: (facts), (assert <hecho>),
(retract <id>), (clear), (reset), (deffacts <nombre> ...).
Estructura de una regla:
  (defrule <nombre>
 [(declare (salience <n>))]
 (patrón_1) ... (patrón_N)
  =>
 (acción_1) ... (acción_N))
Variables locales con "?" (un campo) y "$?" (varios campos); variables globales con defglobal, ?*nombre*=valor, no
usables como parámetros de función.

3.2 FuzzyCLIPS: incertidumbre con Factores de Certeza
"Shell para la elaboración de Sistemas Expertos con incertidumbre
desarrollada a partir de CLIPS (6.10)... Contempla dos maneras de tratar
la incertidumbre que a su vez se pueden combinar: incertidumbre a base de
factores de certeza en reglas y hechos; incertidumbre a base de conjuntos
borrosos".
Hecho con CF: (hecho) CF <valor> (por defecto CF=1).
Regla con CF: (declare (CF <valor>)) dentro del defrule.
Combinación: producto del CF del antecedente por el CF de la regla; con
varios antecedentes se toma el mínimo antes de multiplicar por el CF de
la regla.
Ejemplo completo trazado paso a paso (coche, p.29-32, = BC/BH
coche_cer.clp): con motor=0.8 y luces=0.2 como hechos, y regla_1 CF=0.7,
se traza en vivo cómo (run 1) va derivando: f-3 (problema eléctrico)
CF 0.14 (0.2×0.7), luego se actualiza a CF 0.56 cuando regla_1 vuelve a
dispararse sobre motor=0.8 (0.8×0.7), etc.

3.3 FuzzyCLIPS: incertidumbre con conjuntos borrosos
deftemplate borroso, sintaxis exacta:
  (deftemplate X1
 0 7 ; universo [V_min, V_max]
 ( (baja (0 1) (2 0)) ; etiqueta + pares (valor grado)
 (media (1 0) (3 1) (5 0))
 (alta (3 0) (7 1)) ) )
Observación tipo singleton (valor "nítido" codificado como
triangular degenerado en el mismo punto): (X1 (4 0) (4 1) (4 0)).
"Se utiliza la regla de composición de inferencias con max-min. Se
utiliza por defecto. También se puede usar max-producto".
Funciones de desborrosificación con su sintaxis CLIPS exacta: (maximum-defuzzify <n>) — criterio del máximo;
(moment-defuzzify <n>) — centro de gravedad. Función de graficado:
(plot-fuzzy-value t * <min> <max> <n>).
[OJO] El PDF de clase NO cubre: slots tipados de deftemplate no-borroso,
deffunction, defclass/COOL, bind, ni funciones de pertenencia predefinidas
de FuzzyCLIPS más allá del formato de pares (valor grado) — no inventar
esta sintaxis si hace falta en un ejemplo. [ACTUALIZACIÓN 2ª edición] El MANUAL
de FuzzyCLIPS 6.10d (bloque 4) sí describe los slots FUZZY-VALUE, las funciones
estándar S/Z/PI, los modificadores, get-*, create-fuzzy-value, deffunction con
bind en ejemplos, etc. (defclass/COOL sigue sin cubrirse: solo se dice que las
instancias de objeto tienen CF=1.0).

3.5 COMPLEMENTOS al bloque 3 (texto del PDF CLIPS_FUZZYCLIPS y contenido
 íntegro de los .clp reales; revisión página a página)
CLIPS — detalle: sitio de descarga http://www.clipsrules.net/; es
"fácilmente embebible en aplicaciones C, C++...". Interfaz: se pueden abrir ventanas
para ver la base de hechos y la agenda (conjunto conflicto). Salir: (exit). HECHO =
información relevante que describe un evento o característica del entorno del SE;
puede tener un campo o varios (si tiene varios, el primero suele representar una
relación entre los restantes); todos se guardan en la lista de hechos (fact-list) en la
memoria de trabajo (MT) con un identificador único (timetag) que indica el orden de
entrada. Comandos (facts), (assert), (retract <id>), (clear) [elimina hechos y reglas],
(reset) [elimina hechos y restaura las condiciones iniciales: f-0 (initial-fact)],
(deffacts <nombre> <comentarios> <hechos>) [pasan a la MT tras un reset]. Ejemplo:
(reset) → f-0 (initial-fact); (assert (clase doctorado IA)) → <Fact-1>; (retract 1);
(assert (estudiar CLIPS)) → <Fact-2>; (clear). La base de conocimientos = reglas de
producción; se cargan con load (ficheros *.clp) y se guardan con save; comandos
(rules) y (agenda). Ejemplo de regla:
  (defrule inicio "Primera regla escrita en CLIPS" (initial-fact) =>
 (assert (ejecucion-terminada))
 (printout t "Disparo de la primera regla escrita en CLIPS" crlf))
tras (reset) la agenda muestra "0 inicio: f-0 / For a total of 1 activation" y (run)
imprime el mensaje.
Variables: "?" = un campo, "$?" = varios campos (van en la parte
izquierda). Ejemplo: reglas inicio (assert (alumno Juan Sanchez)) (assert (alumno
Antonio)); variable-local-1 (alumno ?x) imprime "El alumno que no tiene apellidos es:
Antonio" y asserta (regla-variable-local-1 disparada); variable-local-2 (alumno $?x)
(regla-variable-local-1 disparada) imprime "El alumno: (Juan Sanchez) esta en el sistema"
y "El alumno: (Antonio) esta en el sistema". Variables GLOBALES (defglobal ?*nombre* =
valor): accesibles por todas las reglas y funciones; pueden usarse en la parte izquierda
de reglas si no se usan para asignar valor y su cambio NO activa otras reglas; NO pueden
usarse como parámetros de funciones ni métodos. Ejemplo: (defglobal ?*nombre* =
Jose_Angel Olivas Varela); (deffacts profesores (profesor Jose_Angel Olivas Varela)
(profesor Francisco_Pascual Romero Chicharro)); regla inicio con (initial-fact),
(profesor ?nombre ?ape1 ?ape2) y (test (eq ?nombre ?*nombre*)) → imprime "El profesor de
IA es: Jose_Angel Olivas Varela".
FuzzyCLIPS — detalle: shell de libre distribución derivada de CLIPS
(6.10), sintaxis similar; dos maneras de tratar la incertidumbre combinables: factores
de certeza en reglas y hechos y conjuntos borrosos. Repositorio de la versión 6.31:
https://github.com/garydriley/FuzzyCLIPS631. Se arranca con fzclipswin.exe; conviene
abrir el Editor (File) para editar y cargar en memoria; Buffer → Load Buffer carga
hechos y reglas; (reset); Browse → watch (marcar reglas y hechos) para ver qué pasa;
(run 1) dispara regla a regla. FACTORES DE CERTEZA en [0,1] (0 total falsedad, 1 total
verdad): (fact) [CF valor], por defecto CF=1; regla: (declare (CF 0.95)); la
combinación hecho-regla es el PRODUCTO de la certidumbre del antecedente y de la
regla; con varios antecedentes se toma el MÍNIMO antes de multiplicar por el de la
regla; "como no se esperan CF negativos no hay combinaciones previstas para ello"
(diferencia con MYCIN de 1.3, que usa [−1,1]). Ejemplo: (animal tipo pajaro) con regla
CF 0.95 → (animal puede volar) CF 0.95. CONJUNTOS BORROSOS: se pueden definir por
pares o con formas predefinidas (ver manual, bloque 4); se define universo, etiquetas y
conjuntos y se usan en hechos y reglas como en CLIPS; el razonamiento usa la regla de
composición de inferencias max-min (por defecto; también max-producto). Tras
cargar reglas y hechos y hacer (reset), se hacen (run 1) hasta vaciar la agenda; para
dibujar el conjunto Y resultante se llama al hecho 4 (plot-fuzzy-value); defuzzificación:
(maximum-defuzzify 4) da 65 y (moment-defuzzify 4) da también 65.

3.6 CONTENIDO ÍNTEGRO de los 12 archivos .clp del curso (+ 2 zips)
ej_clips(1).zip = BH_frutas.clp, BC_coche.clp, BC_frutas.clp, BH_coche.clp
(4 archivos, 2.464 bytes, nov. 2006); ej_fuzzy_clips(1).zip = BC_coche_cer, BH_metro
cer, BC_metro_cer, BH_coche cer, BH_ejemplo_fuz, BC_ejemplo_fuz, BC_ej18_fuz, BH_ej18_fuz
(8 archivos, 3.401 bytes). Además CLIPSWin.exe (1 MB, 2006) y FuzzyClips.exe (1.2 MB,
2019) en la carpeta SESIONES. Convención: BC_ = base de conocimientos (reglas), BH_ = base
de hechos (deffacts).
(1) coche (CLIPS puro): BH: (deffacts hechos (motor no_arranca) (luces no_se_encienden)).
 BC: regla_1 (or (motor no_arranca) (luces no_se_encienden)) => (assert (problema
 electrico)); regla_2 (motor no_arranca) => (problema combustion); regla_3 (luces
 no_se_encienden) => (bateria en_mal_estado); regla_4 (bateria en_mal_estado)(problema
 combustion) => (revisar en_taller); regla_5 (problema electrico) => (revisar en_taller).
(2) coche_cer (con CF): igual, pero BH: (motor no_arranca) CF 0.8, (luces no_se_encienden)
 CF 0.2; reglas con (declare (CF ..)): regla_1 0.7; regla_2 0.2; regla_3 0.2; regla_4 0.1;
 regla_5 0.6.
(3) metro_cer: BH: (hora punta) CF 0.9; (dia laborable) CF 0.7. BC: regla_1 CF 0.9 (hora
 punta) => (frecuencia_paso_Metro alta) Y (gente_tiene prisa) [dos assert]; regla_2 CF 0.5
 (estacion_Metro llena_gente)(gente_tiene prisa) => (se_producen empujones_entrar_salir);
 regla_3 CF 0.3 (dia laborable) => (se_producen empujones_entrar_salir); regla_4 CF 0.7 (or
 (hora punta) (fin_de_mes)) => (estacion_Metro llena_gente); regla_5 CF 0.6
 (frecuencia_paso_Metro alta) => (se_producen empujones_entrar_salir).
 [DERIVADO — no está en el PDF, verificar ejecutando en FuzzyCLIPS]: regla_1 → frecuencia
 alta 0.81 y prisa 0.81 (0.9·0.9); regla_4 → llena_gente 0.63 (0.9·0.7); regla_2 →
 min(0.63,0.81)·0.5=0.315; regla_3 → 0.7·0.3=0.21; regla_5 → 0.81·0.6=0.486; los
 hechos repetidos se combinan por CF global = MÁXIMO (manual, 4.4): empujones =
 0.486 (el máximo de 0.315, 0.21, 0.486).
(4) frutas (CLIPS puro): BH: (deffacts hechos_1 (tipo_fruta de_arbol) (color morado)
 (semillas una)). BC (18 reglas): 1 (forma alargada)(color verde) => fruta banana; 2
 (forma alargada)(color amarillo) => banana; 3 (forma redonda)(diametro <4) => (fruta
 pera); 4 (forma alargada)(diametro <4) => (fruta pera); 5 (forma redonda)(diametro >4) =>
 (fruta de_arbol); 6 (semillas una) => (tipo_semilla pepita); 7 (semillas >1) =>
 (tipo_semilla multiple); 8 (tipo_fruta pera)(color verde) => (fruta sandia); 9 (tipo_fruta
 pera)(superficie suave)(color amarillo) => melón; 10 (tipo_fruta pera)(superficie
 rugosa)(color verde) => melón; 11 (tipo_fruta de_arbol)(color naranja)(tipo_semilla
 pepita) => albaricoque; 12 (...naranja)(multiple) => naranja; 13 (...rojo)(pepita) =>
 cereza; 14 (...naranja)(pepita) => melocotón; 15 (...rojo)(multiple) => manzana; 16
 (...verde)(multiple) => manzana; 17 (...morado)(pepita) => ciruela; 18 (fruta ?x) =>
 (printout t "La fruta es una " ?x crlf). Traza con los hechos del BH: regla_6 asserta
 (tipo_semilla pepita); regla_17 asserta (fruta ciruela); regla_18 imprime "La fruta es una
 ciruela".
 [OJO] Las reglas 3, 4 y 5 aseveran (fruta pera)/(fruta de_arbol), NO (tipo_fruta ...), y las
 reglas 8-17 exigen (tipo_fruta ...): la cadena forma→diámetro→tipo_fruta NO se
 encadena sola (el hecho (tipo_fruta de_arbol) lo pone el BH). Las reglas 11 y 14 tienen el
 mismo antecedente (naranja + pepita: albaricoque y melocotón) y las 15 y 16 dan manzana
 desde rojo o verde con semilla múltiple; también las reglas 3-4 conciertan "pera"
 para redondo/alargado con diámetro <4. Los patrones "(diametro <4)" son restricciones
 con literales tal como aparecen en el archivo.
(5) ejemplo_fuz (FuzzyCLIPS): deftemplate X1 y X2: universo 0 7; baja (0 1)(2 0); media (1 0)
 (3 1)(5 0); alta (3 0)(7 1). deftemplate Y: universo 0 100; poca (0 1)(25 1)(40 0); media
 (30 0)(50 1)(70 0); mucha (60 0)(80 1)(100 0). Reglas: r1 X1 baja, X2 baja → Y poca; r2 X1
 baja, X2 media → poca; r3 X1 media, X2 baja → media; r4 X1 alta, X2 media → mucha; r5 X1
 alta, X2 alta → mucha. BH: (X1 (4 0) (4 1) (4 0)) y (X2 (1.5 0) (1.5 1) (1.5 0)) (singletons X1=4,
 X2=1.5). [VERIFICADO CONTRA EL PDF] Fuzzificación: X1=4: baja 0, media (5−4)/2=0.5, alta
 (4−3)/4=0.25; X2=1.5: baja (2−1.5)/2=0.25, media (1.5−1)/2=0.25, alta 0. Disparan solo r3
 (min(0.5,0.25)=0.25 → Y media recortada a 0.25) y r4 (min(0.25,0.25)=0.25 → Y mucha
 recortada a 0.25). Unión por contribución global (máximo): media recortada a 0.25 = meseta
 [35,65] (sube de 30 a 50 y baja de 50 a 70: 0.25 en x=35 y x=65) y mucha recortada a 0.25 =
 meseta [65,95] (0.25 en x=65 y x=95); las dos mesetas se tocan en 65 → conjunto resultante
 (30 0)(35 .25)(95 .25)(100 0), un trapecio simétrico respecto a 65. Media de los máximos =
 (35+95)/2 = 65 (meseta: el caso ambiguo que discute el manual, 4.5/4.15) y centro de gravedad =
 65 por simetría: ambos coinciden con los resultados del PDF ((maximum-defuzzify 4) y
 (moment-defuzzify 4) dan 65).
(6) ej18_fuz (los dos aviones): BC: deftemplate V1 y V2: universo 0 6; baja (0 1)(1 1)(3 0); media
 (1 0)(3 1)(5 0); alta (3 0)(5 1)(6 1). potencia: universo 0 10; muy_baja (0 1)(1 1)(3 0); baja (1 0)
 (3 1)(5 0); media (3 0)(5 1)(7 0); alta (5 0)(7 1)(9 0); muy_alta (7 0)(9 1)(10 1). Reglas: r1 V1
 baja,V2 baja → muy_alta; r2 baja,media → alta; r3 baja,alta → media; r4 media,baja → alta; r5
 media,media → media; r6 media,alta → baja; r7 alta,baja → media; r8 alta,media → baja; r9
 alta,alta → muy_baja. BH: (V1 (4.5 0)(4.5 1)(4.5 0)) y (V2 (3 0)(3 1)(3 0)) (V1=4.5, V2=3).
 [DERIVADO — no está en el PDF] AVION1 (Mamdani, media del máximo): V1=4.5 → media 0.25, alta
 0.75, baja 0; V2=3 → media 1, baja 0, alta 0. Disparan r5 (media,media: min(0.25,1)=0.25 →
 potencia media recortada a 0.25) y r8 (alta,media: min(0.75,1)=0.75 → potencia baja
 recortada a 0.75). El máximo 0.75 se alcanza en [2.5,3.5] (baja recortada: sube de 1 a 3 y baja
 de 3 a 5): media de los máximos = 3.0. AVION2 (Takagi-Sugeno, con la forma m = P0+P1·V1+P2·V2):
 solo hay regla con α≠0 si V2 es media: R4 (V1 alta): α=0.75; R5 (V1 media): α=0.25 (R6, V1 baja: 0).
 Con los valores IMPRESOS (R4: 0.7, 0.2, 0.4; R5: 2.4, 0.6, 0.9): f4=0.7+0.2·4.5+0.4·3=2.8;
 f5=2.4+0.6·4.5+0.9·3=7.8 → potencia = (0.75·2.8+0.25·7.8)/(0.75+0.25) = 4.05. Con las
 correcciones MANUSCRITAS (R4: P0 0.8, P2 1; R5: P0 0.6): f4=0.8+0.9+3=4.7; f5=0.6+2.7+2.7=6.0 →
 potencia = 5.025. (El PDF no dice cuál de las dos versiones es la buena.)

4. MANUAL DE REFERENCIA FuzzyCLIPS 6.10d (amplía el bloque 3)
 (FuzzyCLIPS610d(1).pdf, "User's Guide", Bob Orchard, NRC Canada,
 Integrated Reasoning Group, octubre 2004 — 82 págs. — texto en INGLÉS)
Este bloque cubre lo que el bloque 3 declaraba "no cubierto"
(slots borrosos, funciones de pertenencia estándar S/Z/PI, modificadores,
deffunction/bind en ejemplos, funciones get-*, etc.). Las páginas citadas
son las del manual (numeración impresa; el PDF lleva +8 de desfase: la
pág. impresa 1 = pág. PDF 9). Los números de sección son los del manual.

4.1 Qué es y versiones (págs. i, 1-6)
FuzzyCLIPS = versión extendida de CLIPS (compatible con CLIPS 6.10)
que representa y manipula hechos y reglas BORROSOS. Maneja razonamiento
exacto, borroso (inexacto) y combinado: términos borrosos y normales se
mezclan libremente en reglas y hechos. Usa dos conceptos inexactos básicos:
DIFUSIÓN/BORROSIDAD (fuzziness) e INCERTIDUMBRE (uncertainty).
El uso de las extensiones es opcional: los programas CLIPS existentes
siguen ejecutándose bien.
Desarrollo: National Research Council of Canada (NRC), Instituto
de Tecnología de la Información, Bob Orchard. Idea original de Zenon
Sosnowski (CLIPS 4.3). CLIPS lo creó la NASA (Johnson Space Center). Existe
alternativa Java: FuzzyJ Toolkit + FuzzyJess (con Jess de Sandia).
Novedades v6.10d: (a) nuevas funciones para activar/
desactivar el cálculo automático de CF de los hechos afirmados en reglas:
(enable-cf-rule-calculation) / (disable-cf-rule-calculation) — por defecto
ACTIVADO. Motivo: con un contador (counter ?c) en reglas con CF (0.8, 0.6),
el CF del contador iba decayendo (1.0 → 0.8 → 0.64 → 0.384 → 0.2304) sin que
se quisiera; desactivando el cálculo justo antes del assert del contador,
el CF vuelve a 1.0 en cada iteración. (b) Corregido un fallo: un patrón NOT
con AND anidado, p.ej. (not (and (A) (B))), hacía caer FuzzyCLIPS antes de
la 6.10d.
[OJO] En 4.1.1 el manual escribe "enable-rule-cf-calculation" y en 6.9.4
"enable-cf-rule-calculation": misma función, nombre escrito de dos maneras
en el propio manual. El nombre del comando de la sección 6.9.4 es el del
índice (enable-cf-rule-calculation).

4.2 Teoría: borrosidad e incertidumbre
Motivación: en el mundo real hay conocimiento vago, impreciso,
incierto, ambiguo, inexacto o probabilístico. Los shells comerciales
suelen usar factores de certeza [Shortliffe, MYCIN], Bayes o Dempster-Shafer,
pero "no pueden manejar datos borrosos, que constituyen parte muy
significativa del lenguaje natural". Citados como sistemas con algún
razonamiento borroso, pero hechos a medida: Cadiag-2, Fault, FLOPS, FRIL,
SYSTEMZ-II, FLISP. La idea de CLIPS (escrito en C, portable, integrable)
guió esta extensión.
Borrosidad: ocurre cuando el límite de una información no está
claro (joven, alto, bueno, alto...). Conjunto borroso A en universo U con
función de pertenencia µA: U→[0,1]. Ejemplo "young" (Tabla 1, p.7):
edad 25→1.0, 30→0.8, 35→0.6, 40→0.4, 45→0.2, 50→0.0. Los grados de pertenencia
forman una DISTRIBUCIÓN DE POSIBILIDAD del término.
"somewhat young" = raíz cuadrada de los valores de "young"; los
modificadores (hedges) se asocian a funciones matemáticas.
Variable lingüística (borrosa) ↔ "términos primarios" (primary
terms): p.ej. agua_temperatura con {cold, warm, hot}. Ejemplo:
  (deftemplate age 0 120 years
 ( (young (25 1) (50 0))
 (old (50 0) (65 1)) ) )
  (deffacts fuzzy-fact (age young))
  (defrule one (Speed_error big) => (assert (Throttle_change small)))
donde young/big/small son términos borrosos y age/Speed_error/
Throttle_change son variables lingüísticas.
Incertidumbre: se representa con un número crisp de 0 a 1;
CF=1 → totalmente seguro; CF=0 → totalmente inseguro. Un hecho de
FuzzyCLIPS = hecho CLIPS + CF: (hecho) [CF factor]. Ej.: (prediction sunny)
CF 0.8; sin CF se asume 1.0. Solo los HECHOS tienen CF, las
instancias de objetos se tratan como CF=1.0 (nota 6, p.9).
CF también en reglas: (declare (CF 0.95)) en el defrule; si no se
declara, la regla vale 1.0. Borrosidad e incertidumbre pueden
coexistir: (Speed_error more_or_less zero) CF 0.9.

4.3 Técnicas de inferencia: reglas simples
Regla simple "if A then C  CFr"; hecho A' con CFf; conclusión C'
con CFc. Tres tipos según dónde haya objetos borrosos:
  - CRISP_ : el antecedente NO contiene objetos borrosos (aunque el
 consecuente sí).
  - FUZZY_CRISP : solo el antecedente es borroso.
  - FUZZY_FUZZY : antecedente y consecuente borrosos.
CRISP_: A' debe ser igual a A para disparar; C'=C;
  CFc = CFr · CFf (fórmula 2)
Ejemplo 4: regla (declare (CF 0.7)) (light_switch off) => (assert
(illumination_level dark)) con el hecho (light_switch off) CF 0.8 →
(illumination_level dark) CF 0.56 (=0.7·0.8).
FUZZY_CRISP: A' debe ser un hecho borroso con la MISMA
variable borrosa que A, y los conjuntos Fα (patrón) y F'α (hecho) NO tienen
que ser iguales pero SÍ deben solaparse. Ejemplo: (temperature high) y
(pressure high) NO casan (variables distintas); (pressure low) y (pressure
medium) casan si se solapan; (pressure low) y (pressure high) no. El umbral
mínimo de solape se controla con el ALPHA-VALUE (nota 8, p.12; por defecto
0.0 → cualquier solape casa). C'=C y:
  CFc = CFr · CFf · S
S = medida de similitud entre Fα y F'α, basada en Posibilidad P y
Necesidad N [Cayrol, Farency, Prade 1982]:
  S = P(Fα|F'α) si N(Fα|F'α) > 0.5
  S = (N(Fα|F'α) + 0.5) · P(Fα|F'α) en otro caso
  P(Fα|F'α) = max sobre u∈U de min[ µFα(u), µF'α(u) ]
  N(Fα|F'α) = 1 − P(F̄α|F'α), con F̄α el complemento: µF̄α(u)=1−µFα(u)
Si la similitud es alta, CFc ≈ CFr·CFf; si los conjuntos son idénticos S=1;
si no se solapan S=0 y el casamiento FALLA (la regla no entra en la agenda).
Ejemplo 5: regla con CF 0.7, hecho (fuzzy-fact fact1)
CF 0.8. Con P=0.6667 y N=1−P(complemento)=0.3333 (<0.5) → S =
(0.3333+0.5)·P; la figura 7 da S=(0.3333+0.5)*0.8 = 0.6667 (P(Fα|F'α)=0.8
en ese cálculo). Resultado: CFc = 0.7 · 0.8 · 0.6667 = 0.3733.
[OJO] El manual muestra en la Figura 6 "P=0.6667" (posibilidad del
complemento) y en la Figura 7 "P(Fα|F'α)=0.8" (posibilidad del propio
conjunto); son dos P distintas. El resultado final 0.3733 es el que se
usa.
FUZZY_FUZZY: antecedente y consecuente se conectan por
la relación borrosa R = Fα × Fc, con
  µR(u,v) = min[ µFα(u), µFc(v) ] ∀(u,v)∈U×V
(otros algoritmos en la literatura [15]). La conclusión se calcula con la
REGLA COMPOSICIONAL DE INFERENCIA de Zadeh: F'c = F'α ∘ R, es decir
  µF'c(v) = max_{u∈U} min[ µF'α(u), µR(u,v) ]
que se simplifica a µF'c(v) = min[ z, µFc(v) ] con
  z = max_u min[ µF'α(u), µFα(u) ]
(el conjunto conclusión se "recorta" a la altura z: MAX-MIN). Con
max-producto el conjunto conclusión se ESCALA multiplicando por z. La CF
de la conclusión: CFc = CFr · CFf (fórmula 2). Se elige el método con la
función de tipo de inferencia (por defecto max-min). Ejemplo 6: regla
(temperature hot) => (assert (temp_change little)), hecho (temperature
warm). El conjunto resultante es "???" (no describible con un término
lingüístico una vez recortado o escalado).
[OJO] En 5.3.1.3 el manual nombra la función "set-inference-type", pero
en 6.9.8 se llama "set-fuzzy-inference-type" (esta última es la del
comando).

4.4 Reglas complejas, contribución global, umbrales
Múltiples consecuentes: "if Antecedentes then C1 and C2...
and Cn" equivale a n reglas independientes con un solo consecuente.
Múltiples antecedentes con AND lógico: F'c = F'c1 ∩ F'c2
∩ ... ∩ F'cn (intersección = mínimo punto a punto) donde F'ci es el
resultado de la regla simple con el antecedente Ai. Si un patrón es crisp y
otro borroso, la conclusión es la del borroso. CF según el modelo MYCIN:
  CFc = min(CF'f1, CF'f2, ..., CF'fn) · CFr
CONTRIBUCIÓN GLOBAL: al afirmar un hecho borroso sobre
una variable que YA tiene un hecho borroso, ambos se combinan como
evidencia: Fg = Ff ∪ F'c (unión = máximo punto a punto). Las
incertidumbres se agregan: CFg = máximo(CFf, CFc). Por eso NO se aplica a
los hechos borrosos la "duplicación de hechos" de CLIPS estándar. En un
controlador borroso el usuario debe asegurar que TODAS las reglas que
contribuyen a la misma acción disparen antes de la desborrosificación:
mediante SALIENCE distinta o agrupándolas en un MÓDULO (ejemplos fzCmplr.clp
y fzCmpmod.clp; también el Apéndice A).
UMBRAL de CF (Threshold, p.18-20): se puede fijar un umbral de tal
modo que ninguna regla dispare si su CF calculado es menor que el umbral
(útil para cortar cadenas de reglas de certeza muy baja y ganar velocidad).
Por defecto umbral 0.0. CF calculado de la regla = CFrule · min(CF1,...,CFn)
con CFi los CF de los hechos que casan los n patrones del LHS.
Ejemplo 7: regla CF 0.5 sobre (fuzzy-fact fact-list-fact) CF 0.6 → 0.5·0.6
= 0.3; dispara solo si umbral ≤ 0.3. El consecuente borroso
(another-fuzzy-fact c2) recibe CF=0.3 (regla FUZZY_FUZZY), pero el crisp
(crisp-fact c1) recibe 0.5·0.6·S; con S=0.8 → 0.24.
Ejemplo 8: regla CF 0.9, (crisp1) CF 0.8, (fuzzy1 very few) sobre hecho
(fuzzy1 few) CF 0.7 con similitud 0.6: CF de la regla = 0.9·min(0.8,0.7) =
0.63 (dispara si umbral ≤0.63); CF de (crisp2) = 0.9·min(0.8, 0.7·0.6) =
0.378; CF de (fuzzy2 hot) = 0.9·min(0.8,0.7) = 0.63.
El CF calculado de una regla se evalúa cuando la regla es SELECCIONADA
para disparar y NO cuando entra en la agenda, porque los CF de los hechos
pueden cambiar por contribución global mientras la regla espera.
CF en el assert: (assert (some-consequent) CF 0.8). El CF
del assert se MULTIPLICA por el CF calculado según la naturaleza de la regla.
Ejemplo 10: regla CF 0.8, hecho (fact 1) CF 0.9: (assert (c1)) → 0.72
(=0.8·0.9); (assert (c2) CF 0.7) → 0.504 (=0.8·0.9·0.7); (assert (c3)) y
(c4) → 0.72. Útil para dar pesos a varios consecuentes. Fuera de una
regla (desde el prompt), solo se aplica la contribución global: si el hecho
no existe, CF = el indicado; si existe, CF = máximo(existente, indicado).

4.5 Desborrosificación
La inferencia devuelve un conjunto borroso; para control hace falta
un único valor: desborrosificación. FuzzyCLIPS ofrece dos algoritmos:
  - COG (centro de gravedad, "momento"): suave, salida continua; se le
 critica que da poco peso a consecuentes que coinciden y deberían
 reforzarse.
  - MOM (media de los máximos): menos suave pero más rápido (menos cálculo
 en coma flotante).
COG: x' = ∫ x·f(x)dx / ∫ f(x)dx. Como el conjunto son puntos unidos
por segmentos rectos, la integral se reduce a una suma:
  x' = Σ (x'i · Ai) / Σ Ai, con x'i el centro de gravedad local de cada
tramo (triángulo, rectángulo o trapecio) y Ai su área.
Ejemplo 11 (Fig. 12): áreas A1=1.0, A2=1.6, A3=0.6, A4=0.3 con centros
x'1=2.333, x'2=3.917, x'3=5.500, x'4=6.333 →
  x' = (2.333·1.0 + 3.917·1.6 + 5.5·0.6 + 6.333·0.3)/(1.0+1.6+0.6+0.3)
 = 3.943.
MOM: devuelve la coordenada x del punto donde se alcanza el máximo
de pertenencia; si hay varios máximos, la MEDIA de esas x: x'' = (Σ x''j)/J
(J = nº de máximos). Ejemplo 12: con el mismo conjunto de la Fig. 12 el MOM
da 3.0. AMBIGÜEDAD: si el máximo es una MESETA (infinitos puntos), promediar
los puntos x1'', x2'', x3'' da un valor quizá inesperado.
Sintaxis:
  (moment-defuzzify  ?<fact-var> | <integer> | <fuzzy-value>) ; COG
  (maximum-defuzzify ?<fact-var> | <integer> | <fuzzy-value>) ; MOM
Devuelven un número en coma flotante. El argumento puede ser una variable
de hecho, el número de hecho o un valor borroso. Ejemplo 33: hecho
(temperature warm) con COG=28 y MOM=32.5: (moment-defuzzify 1) devuelve
28.0; una regla con (bind ?t (maximum-defuzzify ?f)) imprime "Temperature
is 32.5".
moment-defuzzify puede quedar INDEFINIDO (conjunto de área cero:
valor crisp, o plano en 0.0): por defecto devuelve el PUNTO MEDIO del
universo de discurso (o el valor fijado con set-defuzzification-error-
value). Se comprueba con (is-defuzzify-value-valid): TRUE si el último
valor es válido (si no se llamó aún a ninguna defuzzify, devuelve TRUE);
solo moment-defuzzify puede devolver un valor por defecto inválido.
[OJO] El manual remite a "sección 5.9.14" para set-defuzzification-error-
value, pero esa función no aparece descrita en ninguna sección del
documento (solo se menciona en la nota 16, p.45). No inventar su sintaxis.

4.6 Definición de variables borrosas: deftemplate borroso
Sintaxis general:
  (deftemplate <name> ["<comentario>"]
 <from> <to> [<unit>] ; universo de discurso (from < to, reales)
 ( t1 ... tn ) ) ; lista de términos primarios
Ejemplo 13: (deftemplate water_flow 0 100 liters/sec ... ).
Un término primario es (<nombre> <descripción del conjunto>), y la
descripción es una de TRES formas:
  <singletons> | <standard> | <linguistic-expr>
(a) SINGLETONS: lista de pares (x µ) con x1≤x2≤...≤xn; los
puntos se unen con segmentos rectos y los valores intermedios se calculan
por INTERPOLACIÓN LINEAL; antes del primer punto µ=µ(x1), tras el último
µ=µ(xn); si un mismo x tiene varios valores, se toma el máximo.
Ejemplo 14: "few" en U=[0,9]: µ(0)=0, µ(1)=0, µ(2)=0.3, µ(3)=0.9, µ(4)=1,
µ(5)=0.8, µ(6)=0.5, µ(7..9)=0 → (few (1 0) (2 0.3) (3 0.9) (4 1) (5 0.8)
(6 0.5) (7 0)) dentro de (deftemplate group 0 9 ( ... )).
 Límites nítidos: valores x consecutivos iguales dan borde vertical. Si
hay más de tres puntos con el mismo x, solo se guardan tres (el cuarto
reemplaza al tercero); si dos puntos son idénticos, se descarta uno.
 Ejemplo 15: (three (3 0) (3 1) (3 0)) = el concepto crisp "3" como
conjunto borroso. Ejemplo 16: (weird (1 0)(1 1)(1 0)(3 0)(4 .25)(4 1)(4 .4)
(4 .5)(6 1)(8 0)): el punto (4 .4) se descarta.
(b) STANDARD: funciones estándar S, Z, PI (Π):
  S(u,a,c)=0 si u≤a; 2·((u−a)/(c−a))² si a<u≤(a+c)/2;
 1−2·((u−c)/(c−a))² si (a+c)/2<u≤c; 1 si u>c.
  Z(u,a,c)=1−S(u,a,c).
  Π(u,d,b)=S(u,b−d,b) si u≤b; Z(u,b,b+d) si u>b.
Formato: <standard> ::= (S a c) | (s a c) | (Z a c) | (z a c) | (PI d b) |
(pi d b) — mayúsculas/minúsculas indiferentes. Ejemplo 17:
  (deftemplate Tx "output water temperature" 5 65 Celsius
 ( (cold (z 10 26)) (OK (PI 2 36)) (hot (s 37 60)) ) )
FuzzyCLIPS convierte todo a singletons: elige 9 puntos equiespaciados
(valor ArraySIZE de fuzzypsr.h, modificable recompilando; más puntos =
más carga de cálculo; a menudo bastan 2 ó 3 puntos). Casos especiales:
si a=c en S o Z se usan 2 puntos: (S 10 10) → (10 0)(10 1); (Z 10 10) →
(10 1)(10 0). Si d=0 en PI se usan 3 puntos: (PI 0 10) → (10 0)(10 1)(10 0).
(c) LINGUISTIC EXPRESSION: usa términos definidos ANTES en el mismo
deftemplate + modificadores + and/or. Ejemplo 20:
  (deftemplate temperature 0 100 C
 ( (cold (z 10 26)) (hot (s 37 60)) (warm not [ hot or cold ]) ) )
En el Ejemplo 22 aparece (freezing extremely cold): usa un modificador
sobre un término previo, que es una expresión lingüística válida.

4.7 Slots borrosos en deftemplates estándar
Un "fuzzy deftemplate fact" es un hecho cuyo nombre de relación es
el de un deftemplate borroso: tiene un único slot con el valor borroso. Un
deftemplate NORMAL puede tener uno o varios slots borrosos:
  (slot <slotname> (type FUZZY-VALUE <fuzzy-deftemplate-name>))
Restricciones: NO se admiten otras opciones en ese slot (ni tipos múltiples
como INTEGER+FUZZY-VALUE, ni valor por defecto, ni cardinalidad); un slot
borroso solo guarda valores borrosos y debe tener valor. Ejemplo 21:
  (deftemplate person (slot name (type SYMBOL))
 (slot height (type FUZZY-VALUE fz-height))
 (slot weight (type FUZZY-VALUE fz-weight)))
  (defrule big-person (person (name ?n) (weight heavy) (height tall))
 => (printout t ?n " is a big person" crlf))
Ventaja: sin slots borrosos habría que definir un deftemplate borroso y
reglas por cada persona. Internamente todo hecho borroso se guarda como
(deftemplate t1 (slot GenericFuzzySlot (type FUZZY-VALUE t2))) (nota 14).

4.8 Modificadores (hedges) y expresiones lingüísticas
MODIFICADORES PREDEFINIDOS (tabla p.31; y = cada valor de
pertenencia; se pueden escribir en mayúsculas/minúsculas/mixto):
  not ................ 1 − y
  very ............... y²
  somewhat ........... y^0.333
  more-or-less ....... y^0.5
  extremely .......... y³
  above / below ...... (ver [12] Cox: desplazan el conjunto hacia mayores /
 menores valores; gráficas: "above" sube a 1 y se
 mantiene; "below" parte de 1 y decrece)
  intensify .......... y² si y∈[0,0.5]; 1−2(1−y)² si y∈(0.5,1]
  plus ............... y^1.25
  norm ............... normaliza: y = y·1.0/max-valor (el máximo pasa a 1.0)
  slightly ........... intensify( norm( plus A AND not very A ) )
"very A" aplica el modificador al conjunto completo A. Ejemplo 22: (deftemplate
temp 0 100 C ((cold (Z 20 40)) (hot (S 60 80)) (freezing extremely cold)))
y regla (temp not hot and not cold) => "It's such a pleasant day".
Modificadores DEFINIDOS POR EL USUARIO: con
  (add-fuzzy-modifier <modname> <modfunction>)
donde modfunction es una función de CLIPS o una deffunction que recibe un
float en [0,1] y devuelve un float (si sale de [0,1] se recorta a 0 ó 1).
Ejemplo 23: (add-fuzzy-modifier my-somewhat sqrt); (deffunction most-
extremely-fcn (?x) (** ?x 5)); (add-fuzzy-modifier most-extremely
most-extremely-fcn); luego (sort-of-high my-somewhat high) y
(incredibly-low most-extremely low) en el deftemplate. Se quitan con
(remove-fuzzy-modifier <modname>) (solo los añadidos con add-). Limitación:
así no se pueden definir above, below ni slightly. Para modificadores más
complejos hay que tocar el código C (fuzzymod.c: initFuzzyModifierList y
una función tipo veryModFunction que llama a concentrate_dilute(fv,2.0);
la función Yexpand añade puntos intermedios para que la exponenciación
tenga el efecto correcto en segmentos rectos).
EXPRESIONES LINGÜÍSTICAS: términos primarios + modificadores
+ AND/OR. BNF:
  <LExpr>  ::= <LTerm> | <LExpr> OR <LTerm>
  <LTerm>  ::= <modExpr> | <LTerm> AND <modExpr>
  <modExpr>::= MODIFIER <modExpr> | <element>
  <element>::= PRIMARY-TERM | [ <LExpr> ]
AND tiene MAYOR precedencia que OR; los modificadores son operadores
unarios de la MÁXIMA precedencia; se controla el orden con corchetes [ ]
que deben ir SEPARADOS por espacios (por el analizador de CLIPS). Así
"A or B and C or D" = "A or [ B and C ] or D". Ejemplos: "temperature very
hot or very cold", "height below tall and above short". La unión (OR) es el
máximo punto a punto, µC(x)=max(µA(x),µB(x)), y la intersección (AND) el
mínimo, µC(x)=min(µA(x),µB(x)) (notas 11 y 13, p.16 y 18).

4.9 Patrones borrosos en el LHS de las reglas
Formas de un patrón borroso en el LHS:
  ( fuzzy-variable-name <linguistic-expr> )
  ( fuzzy-variable-name ? )
  ( fuzzy-variable-name ?<var-name> )
  ( fuzzy-variable-name ?<var-name> & <linguistic-expr> )
  ( template-name <slot-description>+ ) ; con ≥1 slot borroso:
 ( fuzzy-slot-name <linguistic-expr> | ? | ?<var> | ?<var> & <linguistic-expr> )
Ejemplos: (defrule simple-LHS (group few) ...) con (deftemplate group 0 20
members ((few (3 1)(6 0)) (many (4 0)(6 1)))); regla con ?f <- (group very
few or very many) => imprime (get-u-units ?f); regla con (person (name ?n)
(ht ?h & very tall)) => imprime ?n y (maximum-defuzzify ?h) — donde ?h se
liga al VALOR BORROSO que casa con "very tall" y se puede pasar a funciones
como maximum-defuzzify o get-u-units. En el Ejemplo 26: (deftemplate height
0 8 feet ((short (Z 3 4.5)) (medium (pi 0.8 5)) (tall (S 5.5 6)))).

4.10 Hechos borrosos en deffacts y assert
deffacts extendido: acepta hechos borrosos y crisp mezclados y CF
opcional (por defecto 1.0). <fuzzy-template-RHS-pattern> ::=
(<fuzzy-template-name> <descripción del conjunto> [CF <cf> | <expresión>]).
La descripción puede ser expresión lingüística, estándar o singletons.
Ejemplo 27: (deffacts groupA (my_group (1 0)(5 1)(7 0)) (your_group (z 4 8))
(their_group (s (+ 1 1) 4)) (person (name ralph) (ht tall)));
(deffacts groupB (this_group (1 0)(5 1)(7 0)) CF 0.35 (that_group (pi 2
(+ 3 4))) CF (+ .2 .3)).
assert extendido: (assert (<crisp fact> | fuzzy-variable-name
<descripción> | template-name <slot-desc>+) [CF <cf>]). Ejemplos 28:
(assert (group few)), (assert (group (1 0)(5 1)(7 0))), (assert (group NOT
[ very few OR many ])), (assert (group (z 4 8))), (assert (person (name
john) (ht extremely tall))), (assert (person (name dan) (ht (pi 0 5.6)))),
(assert (temp (24 0)(25 1)(26 0))). Se admiten VARIABLES y FUNCIONES en la
descripción: (group (z ?minval ?maxval)), (group (z ?minval (+ ?maxval
2))), (group (?x1val 0)(?x2val 1)((+ ?x2val 1) 0.6)((sqr ?x2val) 0)).
También (assert-string "(group (z 4 8))") (Ejemplo 30).
CF en assert: constante 0.0–1.0 o EXPRESIÓN (variable o función que
devuelve 0–1): (assert (fact1) CF ?cf), (assert (fact3) CF (* 0.8 ?cf)),
(assert (fact5) CF (get-cf ?f)); (assert (group few) CF (+ 0.2 0.4)) → 0.6.
CF de regla: (declare (CF <0..1>)) igual que salience; puede ser
constante o expresión.

4.11 Comandos y funciones específicas de FuzzyCLIPS
Comandos normales de CLIPS que también sirven con hechos/plantillas
borrosos: facts, ppdeftemplate, list-deftemplates, undeftemplate,
ppdeffacts, list-deffacts, undeffacts.
Universo de discurso: (get-u X) → cadena "<from> - <to> <units>"
(o "<from> - <to>" sin unidades); (get-u-from X) → límite inferior (float);
(get-u-to X) → límite superior; (get-u-units X) → unidades (cadena; vacía si
no hay). X puede ser ?fact-var, nº de hecho, nombre de deftemplate borroso
o valor borroso. Ejemplo 36: deffunction "fuzzify" (?fztemplate ?value
?delta) que afirma un triángulo centrado en ?value con posibilidad 0 en
value±delta, acotado al universo, usando get-u-from/get-u-to, format,
assert-string; con (temp warm (30 0)(60 1)(90 0)) y (fuzzify temp 50 0.001)
la regla test imprime "Certainty Factor = 0.66667".
Conjunto borroso: (get-fs X) → conjunto entero en singletons
(cadena); (get-fs-length X) → nº de pares; (get-fs-x X i) y (get-fs-y X i)
→ coordenadas x / y del par i-ésimo (numerados de 0 a n−1); (get-fs-lv X)
→ valor lingüístico (p.ej. "very hot" para (temp very hot)); (get-fs-value
X <número>) → valor de pertenencia en ese x (p.ej. para OK (30 0)(60 1)
(90 0), (get-fs-value ?fact 50.0) = 0.6666667). Ejemplo 37: (temperature ???)
con ((0 0)(25 1)(40 0)) → (get-fs-x 2 1) = 25. "???" = conjunto no
expresable con términos/modificadores (singleton, o modificado por la regla
composicional).
CF: (get-cf ?fact-var | <integer>) → CF del hecho (float).
Cálculo de CF en reglas: (enable-cf-rule-calculation) y (disable-cf-rule-
calculation): deshabilitado → los hechos toman el CF indicado en el assert
(o 1.0) y NO se considera el CF de la regla ni de los hechos casados.
Umbral: (set-threshold <0..1>) (por compatibilidad también
"threshold"); (get-threshold) devuelve el umbral si está activo, 0.0 si no.
Evaluación del CF de reglas: (set-CF-evaluation when-defined |
when-activated) — análogo a set-salience-evaluation; when-defined (por
defecto) evalúa el CF de la regla al definirla/compilarla; when-activated
lo reevalúa también al activarse (entrar en la agenda). (get-CF-evaluation)
devuelve el ajuste.
Precisión de visualización: (set-fuzzy-display-precision <2..16>)
(defecto 4; clear NO lo reinicia); (get-fuzzy-display-precision).
Tipo de inferencia: (set-fuzzy-inference-type max-min | max-prod)
(defecto max-min; clear NO lo reinicia); (get-fuzzy-inference-type).
Alpha-value: (set-alpha-value <alpha>) — el casamiento de un
patrón borroso solo tiene éxito si el máximo del conjunto INTERSECCIÓN es
≥ alpha (defecto 0.0: el máximo debe ser >0). (get-alpha-value). Ejemplo 42:
con (temp low) y hecho (temp (pi 0 30)), la regla dispara con alpha 0.0 y
0.5, pero NO con 0.55 (el solape máximo entre low y (pi 0 30) vale 0.5).
Predicado: (fuzzyvaluep <arg>) → TRUE si es de tipo FUZZY-VALUE.
[OJO] El manual escribe "fuzzvaluep" en el título de 6.9.10 y
"fuzzyvaluep" en la sintaxis: la función es fuzzyvaluep.
Crear/operar valores borrosos: (create-fuzzy-value <fuzzy-
deftemplate> <descripción>) crea un valor borroso (términos, singletons o
estándar; p.ej. (create-fuzzy-value temp very hot or very cold)); (fuzzy-
union v1 v2) → "cold or hot"; (fuzzy-intersection v1 v2) → "cold and hot";
(fuzzy-modify <fuzzy-value> <modifier>) aplica cualquier modificador activo
(p.ej. extremely). Se puede hacer (assert (temp ?fv)) con ?fv un valor
creado.
Acceso a slot borroso: (get-fuzzy-slot ?fact-var|<integer>
[<slot-name>]); el slot de un hecho borroso de deftemplate se llama
'GenericFuzzySlot'.
Formato: el especificador %F de (format ...) imprime valores borrosos:
(format t "Value is '%F'%n" (get-fuzzy-slot 0)) → Value is 'cold'.
Gráfica ASCII: (plot-fuzzy-value <logicalName> <plot-chars>
<low-limit> <high-limit> <fuzzy-value>+): logicalName = router (t =
salida estándar); plot-chars = caracteres de trazado (uno por valor; si
faltan, se usa el último; ej. "*+."); low/high-limit = ventana en x (o nil
→ límites del universo); los valores a graficar deben pertenecer al MISMO
deftemplate. Ejemplos: (plot-fuzzy-value t * nil nil (create-fuzzy-value
temp hot)); con ventana (plot-fuzzy-value t * 20 70 ...).

4.12 Ejemplo simple simplTst.clp
Traza (load "simplTst.clp") define deftemplate speed_error,
speed_change, deffacts my_facts, reglas speed-too-fast, speed-ok, get-crisp-
value-and-print-rslt. Tras (reset): f-1 (speed_error zero) CF 0.90; se
activan speed-ok y speed-too-fast. (run): 1) speed-too-fast dispara → f-2
(speed_change ???) CF 0.63 (=0.9·0.7, regla FUZZY_FUZZY); 2) speed-ok
dispara → f-2 se retira y se reafirma como f-3 (contribución global: el
nuevo conjunto es la unión con el anterior); 3) get-crisp-value-and-print-
rslt: "Change speed by a factor of: 0.3553..." (defuzzificación). 3 reglas
disparadas.

4.13 Sistemas continuos
CLIPS termina cuando la agenda está vacía. Para sistemas en tiempo
real, run admite: (run n) hasta n reglas o agenda vacía; (run -1) hasta
agenda vacía; (run -2) para siempre (Control-C interrumpe); (run -n) con
n>2 hasta n reglas (permanece inactivo esperando eventos). (halt) termina en
cualquier momento. runstart/runstop: funciones externas ejecutadas al
entrar/salir del comando run (AddRunStartFunction / AddRunStopFunction;
remove...), útiles p.ej. para pausar un reloj simulado.

4.14 Funcionalidad CLIPS dentro de FuzzyCLIPS
modify y duplicate: devuelven FALSE con hechos borrosos de
deftemplate. Con hechos con slots borrosos, modify = retirar el hecho y
afirmar el nuevo; duplicate = los slots borrosos se AGREGAN (contribución
global), el hecho existente se retira y se afirma el nuevo (no se crea
duplicado, aunque fact-duplication esté apagado). load, save, bload, bsave,
load-facts, save-facts y constructs-to-c funcionan con hechos borrosos, CF.
CreateFact/GetFactSlot/PutFactSlot: requieren conocer estructuras internas.

4.15 Limitaciones y trabajo futuro
(a) maximum-defuzzify: para mesetas el promedio de puntos discretos
da resultados discutibles. Propuesta del autor: representar cada rango
continuo de máximos por su punto medio con un PESO = ancho del rango (un
máximo puntual, peso 0) y calcular x = Σ(xmax·peso)/Σ(peso) si algún peso
no es 0, o Σ xmax / n si todos son 0. Ejemplos: máximos en 1,3,5,7 →
(1+3+5+7)/4 = 4.0 (igual que el método actual); máximos en 1.5 (peso 1),
3 (0), 5 (peso 2), 8 (0) → (1.5·1+3·0+5·2+8·0)/(1+0+2+0) = 3.833 (el método
actual daría (1+2+3+4+6+8)/6 = 4.0). (b) El cálculo de CF puede ser difícil
de entender con reglas complejas: ¿se puede simplificar? (c) Mantenimiento
de verdad (construct "logical"): si dos reglas afirman (temp low) y (temp
medium) con dependencia lógica de (x) e (y), la contribución global deja
(temp low OR medium); al retirar solo uno de los soportes, el efecto de la
contribución NO se deshace. Alternativa propuesta: diferir la combinación
con una función (combine-evidence temp) o hacer que la desborrosificación
combine la evidencia internamente (una función por hecho y otra por
plantilla). (d) Hacer de FUZZY-VALUE un tipo estándar de CLIPS (poder
guardarlo también en objetos), requiere ayuda de NASA u otros.

4.16 Apéndice A — Ejemplo de la ducha (Shower)
Simula el flujo y temperatura del agua a la salida de una ducha y
un controlador borroso para mantenerlos en rango. Modelo: tuberías de volumen
cero; el agua se mezcla perfectamente en el punto X; tubería aislante
térmica perfecta; sin transferencia de calor entre X y la ducha. Ecuaciones:
  Tc∈[0,35]°C; Th>Tc; Th∈[0,100]°C
  Tx=(Fc·Tc+Fh·Th)/Fx; Fx=Fc+Fh; Px=30 kPa (presión atmosférica)
  Fc=vc(Pc−Px); Fh=vh(Ph−Px); vc,vh∈[0,1] posición de válvulas fría/caliente
  Pc, Ph dependen de consumos vecinos (riego, lavadora, lavavajillas) —
  cambios simulados.
Objetivos de control: (1) temperatura NUNCA >45°C ("generalmente
imposible"); (2) rara vez <15°C; (3) media 36°C con varianza pequeña;
(4) flujo medio 12 L/min con varianza pequeña; (5) mover poco las
válvulas. Bucle de control borroso: Proceso → parámetros de salida →
Fuzzificación → Controlador lógico borroso → Desborrosificación → acción
de control. Versión en texto (shwrNOUI.clp): (load "shwrNOUI.clp"), (reset)
y (run); pide temperatura, presión y posiciones de válvulas; para al llegar
a flujo 11–13 L/min y temperatura 34–38°C; ejemplo sugerido por Robert
Spring (Noranda Technology Centre).

== 5. ZADEH 1965 "Fuzzy Sets" (Information and Control 8, 338-353; artículo fundacional, Berkeley) ==
Resumen: conjunto borroso = clase de objetos con continuo de grados de pertenencia, dado por una función de pertenencia f_A(x)∈[0,1]; se extienden inclusión, unión, intersección, complemento, relación, convexidad; teorema de separación para conjuntos borrosos convexos SIN exigir disjunción. Motivación: clases sin criterios precisos de pertenencia ("mucho mayor que 1", "mujeres hermosas", "hombres altos", estrella de mar frente a "animal"); importantes en reconocimiento de patrones, comunicación y abstracción. Es un marco paralelo al de conjuntos ordinarios pero más general; la imprecisión viene de la ausencia de criterios de pertenencia, NO de variables aleatorias: la noción es "completamente no estadística".
DEFINICIONES: X espacio de puntos; A borroso con f_A:X→[0,1] (si solo 0/1 = conjunto ordinario). Rango general: conjunto parcialmente ordenado; si f_A se interpreta como verdad = lógica multivaluada continua en [0,1]. Ejemplo "números mucho mayores que 1": f(0)=0, f(1)=0, f(5)=0.01, f(10)=0.2, f(100)=0.95, f(500)=1.
- Vacío: f_A≡0. Igualdad: f_A=f_B ∀x. Complemento: f_A' = 1−f_A (1). Contención: A⊂B ⇔ f_A ≤ f_B (2).
- Unión C=A∪B: f_C(x)=Max[f_A,f_B] (3), f_C=f_A∨f_B (4); es el MENOR conjunto borroso que contiene a A y B; asociativa.
- Intersección: f_C=Min[f_A,f_B] (5), f_C=f_A∧f_B (6); es el MAYOR contenido en ambos; asociativa. Disjuntos si A∩B vacío.
- "Pertenecer" solo tiene sentido trivial (f>0). Con dos niveles α>β (0<β<α<1): x pertenece a A si f_A(x)≥α; no pertenece si ≤β; indeterminado si β<f_A<α → lógica trivaluada (Kleene 1952): T, F, U.
PROPIEDADES: De Morgan (A∪B)'=A'∩B' (7), (A∩B)'=A'∪B' (8); distributivas C∩(A∪B)=(C∩A)∪(C∩B) (9), C∪(A∩B)=(C∪A)∩(C∪B) (10); prueba por 1−Max[fA,fB]=Min[1−fA,1−fB] (11) y Max[fC,Min[fA,fB]]=Min[Max[fC,fA],Max[fC,fB]] (12) (6 casos de ordenación). Los conjuntos borrosos forman un RETÍCULO DISTRIBUTIVO con 0 y 1 (Birkhoff). Interpretación con TAMICES: fi∨fj = tamices en paralelo, fi∧fj = en serie; C=[(A1∪A2)∩A3]∪A4 (13) = red equivalente a un tamiz de mallas f_C(x).
OPERACIONES ALGEBRAICAS: producto AB: f_AB=f_A·f_B (14), AB⊂A∩B (15). Suma A+B: f_A+f_B (16), solo si f_A+f_B≤1 ∀x; suma dual A⊕B=(A'B')'=A+B−AB (Cover); en ordinarios ∩≡producto y ∪≡⊕ (= t-norma producto y su t-conorma). Diferencia absoluta |A−B|: |f_A−f_B|.
COMBINACIÓN CONVEXA: (A,B;Λ)=ΛA+Λ'B (17), f=f_Λ f_A+(1−f_Λ)f_B (18); A∩B⊂(A,B;Λ)⊂A∪B (19) por Min≤λf_A+(1−λ)f_B≤Max (20); si A∩B⊂C⊂A∪B existe Λ con f_Λ=(f_C−f_B)/(f_A−f_B) (21).
RELACIÓN BORROSA en X = conjunto borroso en X×X (ej. "x≫y": f(10,5)=0, f(100,10)=0.7, f(100,1)=1); n-aria: f_A(x1..xn). COMPOSICIÓN B∘A: f_{B∘A}(x,y)=Sup_v Min[f_A(x,v), f_B(v,y)] (=max-min); asociativa.
INDUCIDOS POR APLICACIONES: T:X→Y y B en Y induce A en X: f_A(x)=f_B(y) para y=T(x) (22). Recíproco (A en X, T no uno-a-uno): f_B(y)=Max_{x∈T⁻¹(y)} f_A(x) (23) → base del principio de extensión.
CONVEXIDAD (X=E^n): A convexo ⇔ Γα={x|f_A(x)≥α} convexo ∀α∈(0,1] (24) ⇔ f_A[λx1+(1−λ)x2] ≥ Min[f_A(x1),f_A(x2)] (25) (Berlekamp; no implica que f_A sea función convexa). TEOREMA: intersección de convexos es convexa. ACOTADO: Γα acotado ∀α>0. Lema: M=Sup f_A se alcanza "esencialmente" en algún x0. Estrictamente convexo: Γα estrictamente convexos; fuertemente convexo: f_A[λx1+(1−λ)x2] > Min (∀λ∈(0,1)); no se implican entre sí. NÚCLEO C(A)= puntos donde M se alcanza esencialmente; teorema: si A convexo, su núcleo es convexo; corolario: en E¹ con A fuertemente convexo el máximo es único.
SOMBRA: S_H(A) en E^{n−1}: f(x2..xn)=Sup_{x1} f_A(x1..xn); sombra de convexo es convexa; S_H(A)=S_H(B) ∀H ⇒ A=B (convexos); si solo A convexo ⇒ A=conv B.
TEOREMA DE SEPARACIÓN: clásico: convexos disjuntos → hiperplano separador. Grado de separación por H: D_H=1−M_H (M_H=Inf K_H, con f_A≤K_H a un lado y f_B≤K_H al otro); separabilidad D=1−M̄, M̄=Inf_H M_H (31-32). TEOREMA: A,B convexos y acotados en E^n con M=Sup Min[f_A,f_B] (grado máximo de A∩B) ⇒ D=1−M: el mayor grado de separación por un hiperplano es UNO MENOS el grado máximo de la intersección (casos M=Min(MA,MB) y M<Min(MA,MB)). Relevante para discriminación de patrones y optimización.
[No incluye MPG, implicación borrosa, control ni FuzzyCLIPS (posteriores, Zadeh 1973+).]

== 6. SOBRINO, PUENTE, OLIVAS "Extracting answers from causal mechanisms in a medical document" (Neurocomputing 135 (2014) 53-60) ==
Uso de cuantificadores/hedges borrosos y mapas cognitivos borrosos de Kosko para responder preguntas causales médicas. Pirámide de preguntas (menor→mayor complejidad): Yes/No → Where/When/Who → What/Which → How → Why. Objetivo: what = identificar la CAUSA de un efecto; how = seleccionar la parte de un MECANISMO (grafo causal) que relaciona causa-efecto; why = causas CENTRALES del mecanismo (el conocimiento profundo está en los nodos centrales). Se extrae de un documento ya recuperado (salta la fase de "document processing" de los sistemas Q/A). En medicina hay mecanismos, no leyes; las causas son complejas (no únicas) e imprecisas (no crisp; enfermedades de fronteras borrosas: esquizofrenia, bulimia, anorexia). Correlación≠causa (H. pylori–úlcera); poder causal de Cheng = diferencia de prob. del efecto con/sin causa = "propensión" (teórica, imprecisa). Causas de Aristóteles: MATERIAL, FORMAL, EFICIENTE (fuente primaria del cambio; la usada aquí), FINAL (estatua: metal, hombre orante, escultor, homenaje).
WHAT: un parser Flex+C detecta frases causales (cause, effect...) y hedges/cuantificadores borrosos → plantilla (nodo causa, relación con cuantificador, nodo efecto con hedge) → BD (tablas Concept y Relationship); Java automatiza. Respuesta: buscar el concepto; si preguntan causas → registros donde es EFECTO (cause_concept); si efectos → al revés; componer con "y" y modificadores; cuidar el conector ("cause": smoking causes lung cancer; "due to": lectura invertida). Ej. "What causes lung cancer?" → smoking, radon gas, tobacco use.
HOW: algoritmo recursivo de caminos entre causa X y efecto Y (profundidad máx. 8 nodos); se ordenan por relevancia con el enfoque MAX-MIN de Kosko: efecto INDIRECTO de un camino = MÍNIMO de los cuantificadores de sus enlaces (eslabón más débil); efecto TOTAL = MÁXIMO de los indirectos. Orden de cuantificadores P={eventually < can < about 85% < about 90% < provokes ≤ causes}. Ejemplo "How smoking causes death?": 5 caminos: I(n1..n9 con causes,causes,eventually,can,can,provokes)=eventually; otro=eventually; (about 90%,can,can,provokes)=can; (about 90%,can,can,can)=can; directo 85% → efecto total = max = 85%. Se traducen los 3 más relevantes.
WHY ("explicar el why explicando el how"; explanans/explanandum): causa primera + nodos RELEVANTES = alta CENTRALIDAD en el grafo (G=(V,E), C:V→ℝ). Medidas (grafo de 9 nodos): grado de salida (nodo1: 3/8 estándar; nodo4: 2/8; resto 1/8), CERCANÍA (closeness: 1/suma de distancias; estándar (n−1)/suma: nodo1 8/23, nodo4 8/15...), INTERMEDIACIÓN (betweenness: cuántos geodésicos pasan por el nodo; estándar ÷(n−1)(n−2)/2; nodo4=21/32=0.656; nodo5=0.334), AUTOVECTOR (eigenvector: importa la proximidad a nodos muy conectados; nodo1 0.999991, nodo2 0.004339, resto ≈0). Consenso (Obiedat): media aritmética de grado, cercanía e intermediación: nodo1 (0.375+0.348+0.25)/3=0.324; nodo4 (0.25+0.533+0.656)/3=0.480 → central = nodo4. Lego: causa primera + nodo central ("Because John was a smoker, causing lung cancer"); especialista: además nodos de mayor autovector posteriores al central (5 y 6; se descartan 1=causa raíz, 2 y 3 anteriores al central). Algoritmo why: localizar causa y efecto; centralidad de cada nodo; el mayor; los de mayor autovector; rechazar los de número menor que el central; ordenar y componer.
[OJO] Tabla de cercanía del artículo con estándares repetidos (nodos 1 y 2 → 8/23) y denominador de intermediación 32 en vez de (n−1)(n−2)/2=28. Trabajo futuro: redes serie, convergentes y divergentes. Autores: Sobrino (USC), Puente (ICAI-Comillas), Olivas (UCLM).

== 7. ROMERO-CÓRDOBA, OLIVAS et al. "An Application of Fuzzy Prototypes to the Diagnosis and Treatment of Fuzzy Diseases" (Int. J. Intell. Syst. 2016, DOI 10.1002/int.21836; grupo SMILe-UCLM) ==
CDSS (sistema de apoyo a la decisión clínica) para "enfermedades borrosas" (Sadegh-Zadeh): no diagnosticables por una prueba/síntoma concreto, síntomas comunes a otras; diagnóstico por EXCLUSIÓN. Aplicación: FIBROMIALGIA (crónica, dolor musculoesquelético generalizado, fatiga, sueño, sin causa conocida; diagnóstico clínico por exclusión + 18 puntos dolorosos ACR 1990) frente a polimiositis, artritis reumatoide, lupus, polimialgia reumática, hipotiroidismo (y dermatomiositis). Prevalencia 2-5%, 10× más mujeres; España 15% de consultas de reumatología. Cita de Zadeh: "síntomas y enfermedades son borrosos por naturaleza".
Razonamiento médico = conjeturas y refutaciones: GRADO DE CONFIRMACIÓN + GRADO DE REFUTACIÓN → GRADO DE CREDIBILIDAD. Teoría de semejanza con prototipos (Sadegh-Zadeh 2008): la clase "enfermedad" es una categoría irreducible con prototipos; hay que medir similitud. PROTOTIPO DEFORMABLE BORROSO (FDP) = confluencia de prototipos deformables de Bremermann (reconocimiento de patrones: clasificar según mínima energía de deformar el prototipo más cercano) y prototipos borrosos de Zadeh 1982 (un prototipo NO es un elemento: es reunión de ejemplares buenos, malos y frontera). DEFINICIÓN: FDP = COMBINACIÓN LINEAL de categorías prototípicas borrosas (tablas de atributos) con coeficientes = grados de pertenencia de la situación real a cada una (Olivas, tesis 2000). Aplicado a mantenibilidad de SW, tráfico, gestión documental, RI, incendios forestales. Rosch: un elemento pertenece si se parece al máximo representante; Zadeh: no todo miembro es buen representante; el prototipo es un esquema borroso con grados.
Diseño: base de conocimiento (prototipos con preguntas de signos/síntomas/pruebas) + motor de inferencia. Hechos del prototipo: RESOLUTIVOS (confirman/refutan; p.ej. TSH en hipotiroidismo), INDICATIVOS (hacen sospechar: caída de pelo, bradipsiquia, artralgias, astenia, letargia, parestesias), OTROS (impuestos por expertos); cada síntoma con rango e IMPORTANCIA (etiqueta lingüística/numérica; la debilidad muscular pesa más en hipotiroidismo que en fibromialgia). FUNCIÓN DE AFINIDAD: entradas "known/unknown/nonexistent"; mantiene vector de prototipos ordenado por afinidad; respuestas: valor conocido, sin responder, no concluyente. ALGORITMO (Fig. 4): para cada pregunta, ver en qué enfermedades afecta; si la respuesta encaja con el prototipo se SUMA valor según juicio experto, si no se RESTA; sin valor: puntuación según parámetros definidos (no se sabe / no evaluada); reordenar prototipos. Preguntas en 3 grupos (1 decisivas, 2 orientan sin confirmar, 3 menos significativas); las respuestas rellenan todos los prototipos que contienen la pregunta; se presentan las del prototipo más similar (grupo 1, luego 2, 3). Flujo: elegir preguntas→enviar/recibir→actualizar hechos y similitud→puntuar patrones→¿diagnosticado? (notificar→tratamiento→¿segunda opinión?). No se muestran las preguntas ya en la historia clínica electrónica.
Ejemplo (Tabla II, valores tras preguntas iniciales): Fibromialgia −0.28, Dermatomiositis −2.00, Lupus −0.22 (el mayor), Artritis reumatoide −0.64, Hipotiroidismo −0.78, Polimiositis −0.41, Polimialgia reumática −1.09. Se rechaza lupus (sin anti-ADN nativo) → artritis reumatoide → sospecha de hipotiroidismo (TSH, fatiga) → fibromialgia (alternativas por orden: hipotiroidismo, dermatomiositis, polimialgia). Evaluación: 10 pacientes del C.S. de Daimiel; 9 coincidencias y caso 7 (lupus/artritis) parcial: detectó artritis pero no lupus; "≈98%"; usabilidad buena.
[OJO] Erratas de numeración de secciones; el "98%" no cuadra con 10 pacientes; el PDF no da la fórmula numérica de la afinidad.

== 8. SERRANO-GUERRERO, OLIVAS, ROMERO, HERRERA-VIEDMA "Sentiment analysis: A review and comparative analysis of web services" (Information Sciences 311 (2015) 18-38) ==
Análisis de sentimientos (SA)=minería de opiniones. OPINIÓN = 5-tupla (e_j, a_jk, so_ijkl, h_i, t_l): entidad, aspecto, valor del sentimiento, portador, tiempo. Tipos: regulares (directas/indirectas), comparativas; explícitas/implícitas. Subjetividad ≠ sentimiento; emoción; mood. TAREAS: clasificación de sentimientos (positivo/negativo/neutro; escalas [−1,1] o estrellas; predicción de rating), de subjetividad (paso previo), resumen de opiniones (uno/varios documentos), recuperación de opiniones (relevancia+opinión), sarcasmo/ironía (la más difícil), género/autoría, spam de opinión. TÉCNICAS: aprendizaje automático (supervisado: SVM, Naive Bayes, Máxima Entropía; semi/no supervisado; híbridos; rasgos: términos/n-gramas y frecuencia, categoría gramatical, negaciones, dependencias sintácticas) y léxicos (basados en diccionario: WordNet→SentiWordNet, semillas + sinónimos/antónimos, no captan dominio; basados en corpus: LSA, frecuencia). 3 niveles: documento, oración, entidad/aspecto.
15 servicios web (rango de polaridad): AlchemyAPI [−1,1] (sentimiento direccional Sujeto-Acción-Objeto), Lymbix [−10,10] (8 categorías emocionales), Musicmetric (5 categorías), Openamplify [−1,+1], Opinion Crawl, Opendover (ontologías; [−9,9]), Repustate, Semantria ([−1,1], frases cerca de palabras buenas/malas), Sentiment140 (Stanford; sin puntuación; NB/MaxEnt/SVM), SentimentAnalyzer, SentiRate (11 categorías), Sentimetrix (GATE; 110M tuits), Uclassify (40.000 reseñas Amazon), ViralHeat, Wingify [0,1].
Medidas: accuracy = aciertos/total; precisión y recall por clase; ECM mse=(1/n)Σ(x_i−y_i)²; polaridades normalizadas a [−1,1] (<0 negativo, >0 positivo, 0 neutro); a nivel oración se agrega por media aritmética. Colecciones: Large Movie Review (1000 de test, sin neutras), Twitter (498 manuales: 177 neg, 182 pos, 139 neu), Amazon irónico (437: 289 pos, 20 neu, 128 neg; reseñas completas y solo oraciones irónicas).
Resultados: mejores exactitudes: películas SentimentAnalyzer 80.4% (Semantria 74.3, Uclassify 75.8, AlchemyAPI 73.6; peor SentiRate 30.7); tuits AlchemyAPI 62.5; Amazon SentimentAnalyzer 71.5 (Musicmetric 68.4); las oraciones irónicas sueltas rinden algo peor que las reseñas (menos contexto). MSE mejores: AlchemyAPI y Semantria 0.07 (películas). Debilidad común: textos NEUTROS. Mejores por aspecto: textos cortos: AlchemyAPI, Lymbix, OpenAmplify, Semantria, Wingify; largos: SentimentAnalyzer, AlchemyAPI, Semantria, Uclassify, Musicmetric; ironía: SentimentAnalyzer, Musicmetric, Uclassify, ViralHeat, AlchemyAPI. Experimento IMDb: ranking de 100 películas por SA de comentarios frente al de IMDb con correlación de Spearman R=1−6Σd_i²/(n³−n): SentimentAnalyzer 0.5, Lymbix 0.42, AlchemyAPI 0.36 ... Openamplify 0.16, Opinion Crawl 0.15.
Conclusión con enlace al curso: los servicios son demasiado simples (solo pos/neg/neutro) y no agregan puntuaciones de oraciones; podrían mejorarse con LÓGICA BORROSA (categorías más finas) y operadores de agregación OWA.

== 9. OLIVAS "La lógica borrosa y sus aplicaciones" (boletic, BOLE.TIC nº24, 2002; artículo divulgativo del profesor, español) ==
Resumen del propio curso; el ejemplo del ventilador = Ejercicio de Control Borroso 3 (2.9-bis) con solución; el del péndulo = Mamdani del bloque 2.8.
HISTORIA: Zadeh (Azerbaiyán 1921, Berkeley) a mediados de los 60; precedentes: Max Black 1937 "Vagueness: An exercise in Logical Analysis", Karl Menger 1942 "Statistical Metrics" y relaciones borrosas de indistinguibilidad (50s). Idea: el pensamiento humano usa ETIQUETAS. Lógica multivaluada (Łukasiewicz 1922; años 30: n valores racionales en [0,1]). T-normas: nacen de la desigualdad triangular de Menger (composición de distribuciones de probabilidad) y se revelan útiles para la intersección borrosa. Extensión: f crisp de puntos → subconjuntos borrosos. Implicación borrosa I:[0,1]²→[0,1]; sus extensiones NO son equivalentes entre sí.
REPRESENTACIÓN: la f. de pertenencia sale del experto (no de repetición de observaciones); adquisición: entrevistas y formularios. TERM-SET = conjunto finito, preferiblemente 7±2 términos. Ejemplo "altura" (universo 0-1 ≙ 130-230 cm), trapecios (a,b,c,d): E1 Bajísimo (0,0,0,0); E2 Muy bajo (0,0,0.05,0.1); E3 Bastante bajo (0.05,0.1,0.2,0.25); E4 Ligeramente bajo (0.15,0.25,0.4,0.5); E5 Normal (0.3,0.4,0.6,0.7); E6 Ligeramente alto (0.5,0.6,0.75,0.85); E7 Bastante alto (0.75,0.8,0.9,0.95); E8 Muy alto (0.9,0.95,1,1); E9 Altísimo (1,1,1,1).
RAZONAMIENTO APROXIMADO (Zadeh): la lógica clásica es caso especial; inferencia por REGLA DE INCLUSIÓN (hipótesis inferida si los mundos que satisfacen las premisas ⊆ los de la hipótesis); aporta VARIABLES con valores de verdad lingüísticos; CUANTIFICADORES lingüísticos entre ∀ y ∃ ("la mayoría" = subconjunto borroso); conocimiento PROTOTÍPICO/reglas por defecto (Reiter, Yager: "típicamente los pájaros vuelan"); LÓGICA POSIBILÍSTICA = base {T,F} con grados en [0,1]; verdadero Vp={1/T,0/F}, falso {0/T,1/F}, desconocido {1/T,1/F}. MPG: Regla "Si x es A entonces y es B", hecho "x es A'", conclusión "y es B'" con B'=A'∘R, B'(y)=sup_x min[A'(x),R(x,y)], R(x,y)=I(A(x),B(y)) (ej.: ciudad grande→tráfico muy denso; "la ciudad no es muy grande").
CONTROL: boom japonés desde 1987; 1974 Mamdani (máquina de vapor); 1980 F.L. Smidth (cementera, Dinamarca, primera implantación real); 1983 Fuji (depuradoras, Japón); 1987 OMRON/Yamakawa (primeros controladores comerciales); metro de Sendai 1987; aplicaciones: cámaras Sony/Sanyo/Canon, lavadoras Panasonic/Bosch eco-fuzzy, aire acondicionado Mitsubishi, ABS Mazda/Nissan, cambio automático Renault. Éxito por SIMPLICIDAD.
MAMDANI: reglas "Si h1 es A(1) y...y hn es A(n) entonces η es B", α_r=min{μ...}; salida de cada regla = conclusión cortada en α_r; unión por máximo; desborrosificación: valor dentro del máximo ([4°,6°]), media de máximos (5°), centro de gravedad (3.9°). Ejemplo: A=36°, θ̇=−2.25°/s; R1 (A pos. pequeño, B aprox. cero → F pos. pequeño): A pos. pequeño(36)=0.4 (=1 hasta ~22.5, 0 en 45), B aprox. cero triángulo −11.25,0,11.25 vale 0.8 → α=0.4, salida triángulo 0-2.5-5 cortado a 0.4; R2 (pos. medio, pico en 45, vale 0.6 en 36) → triángulo 2.5-5-7.5 cortado a 0.6; unión: 0→0.4 en x=1, meseta 0.4 hasta 3.5, sube a 0.6 en 4, meseta 0.6 hasta 6, 0 en 7.5. [OJO] el 3.9 sale del promedio ponderado de vértices (0.4·1+0.4·3.5+0.6·4+0.6·6)/2.0, no del centroide exacto.
TAKAGI-SUGENO: mismas particiones de entrada; sin partición de salida; f_r(x)=a1x1+...+anxn+a; η=Σα_r f_r/Σα_r; ventaja: sin desborrosificación; inconveniente: difícil obtener los coeficientes. EJEMPLO VENTILADOR: T∈[0,70]°C; baja=1 hasta 25→0 en 35; media triángulo 15-35-55; alta sube de 35 a 45. Reglas: R1 Alta p0=700,p1=500; R2 Media 100,200; R3 Baja 100,50 (v=p0+p1·T). T=40: alta 0.5, media 0.75, baja 0; f1=700+500·40=20.700; f2=100+200·40=8.100; v=(0.5·20.700+0.75·8.100)/(0.5+0.75). [OJO] el PDF imprime 14.760,6 pero da 13.140 (16.425/1.25); dibuja 0.8 para "media" pero (55−40)/20=0.75; y numera mal las reglas (dice R2 y R3 disparan). Calcular con 0.5 y 0.75 → 13.140.
INTERNET (FLINT 2001, Berkeley): computing with words, soft computing (LB+RN+computación evolutiva): buscadores conceptuales, perfiles de usuario, comercio electrónico (Mamdani: Soft Knowledge), Semantic Web, conceptual fuzzy sets de Takagi, agregación y clustering, ontologías, indexación conceptual, agentes, data mining.

== 10. INFORMES OBS BUSINESS SCHOOL (J.A. Olivas; contexto general, no técnico) ==
10.1 "IA, inteligencia computacional y análisis inteligente de datos" (2021). IA ≠ ML ≠ DL: en IA "nada es tan nuevo" (deep learning: años 40-50, algoritmos de aprendizaje 80-90; Random Forests de Breiman 2001; lógica borrosa igual que Zadeh 1965): cambió la potencia de cómputo, no los paradigmas (30 años sin nuevos). ML = escalar operaciones estadísticas simples a datos numéricos estructurados y normalizados (cuello de botella: la realidad no cabe en eso); además hay razonamiento, incertidumbre, causalidad, heurística, categorización, lenguaje natural, emociones, ingeniería del conocimiento, PLN, razonamiento aproximado. Los sistemas de IA deben combinar DATOS y CONOCIMIENTO humano del dominio (Mitchell 2019).
IA = simular comportamiento humano inteligente; ingeniería del conocimiento → Sistemas Basados en el Conocimiento (SBC; sistemas expertos desde los 80; reglas "si síntomas A,B,C entonces con probabilidad X enfermedad E"). Paradigmas de ML: analógico (razonamiento basado en casos), inductivo (árboles: ID3, CART, C4.5, See5, Random Forest), conexionista (RN), evolutivo (GA, PSO, gradiente estocástico), modelos gráficos probabilistas (bayesianos, Markov, Kalman, SVM). CLUSTERING (no supervisado; nítido o borroso por similitud: euclídea, coseno, borrosa): SOM/Kohonen, K-means, c-means, KNN, Mean shift, Dirichlet/LDA, gaussianos; extensiones borrosas: Fuzzy K-means, Fuzzy c-means, Isodata. CLASIFICACIÓN (supervisado): árboles, perceptrón multicapa con backpropagation, convolutivas, Hopfield, Adaline, deep learning; redes bayesianas, Naive Bayes, SVM.
SOFT COMPUTING (Zadeh): tolerante a imprecisión, incertidumbre y verdad parcial; modelo = mente humana; principio: trazabilidad, robustez, bajo coste. Componentes: LÓGICA BORROSA, REDES NEURONALES, RAZONAMIENTO PROBABILÍSTICO (incluye redes de creencias, GA, teoría del caos); son COMPLEMENTARIOS ("asociación", no mezcla); ej. sistemas NEUROBORROSOS (ABS y crucero Nissan/Mazda, lavadoras Bosch eco-fuzzy, aire Mitsubishi, estabilización de vídeo); alto cociente de inteligencia de máquina (IM). Razonamiento aproximado ⊂ inteligencia computacional/soft computing.
Analítica: BI operacional vs. analítica/táctica-estratégica; descriptiva (visualización), predictiva (regresión, CART, KDD/minería), series temporales (estacionarias/no; mínimos cuadrados, alisado exponencial; interpolación), PRESCRIPTIVA (varios escenarios = optimización: GA, metaheurísticas). PREDICCIÓN vs PRONÓSTICO: estimación/extrapolación de tendencia (habitantes de Madrid 2025) frente a anticipar un hecho puntual (quiniela 1-X-2, terremoto SÍ/NO), que rompe la tendencia y requiere técnicas cognitivas (expertos, relaciones causales). Crítica: la BI "transforma datos en información" (visualización) pero debe generar CONOCIMIENTO (DSS, recomendadores, series, segmentación); ir "a ciegas" con un algoritmo es un enfoque erróneo. Aplicaciones del grupo: fuzzy diseases (fibromialgia, AEPIA 2015), grafos causales en oncología (20 tipos de condicionales inglesas first/second/third), genogramas (riesgo de cáncer hereditario), incendios forestales, ingeniería del software, tráfico, historias clínicas (>300 documentos; resúmenes), metabuscadores ("monitores baratos" ↔ "pantallas no muy caras"), ciencias sociales. Análisis de sentimientos: resumen del bloque 8. Científico de datos: perfil multidisciplinar, equipos multidisciplinares, "martillo y clavos"; herramientas R, Python, Scala, Hadoop, Spark, Keras/TensorFlow. Conclusión: IA que emule el comportamiento racional humano, no solo estadística; no llamar "IA" a cualquier automatismo (reloj de pulsaciones, asistente de voz, persianas domóticas).
10.2 "IA, aprovechamiento inteligente de datos masivos con Ingeniería del Conocimiento: radicalización en redes y consecuencias económicas de la pandemia" (2023; Olivas, Montoro, Lorenzo). Definiciones: DATO = representación simbólica del valor de un atributo; INFORMACIÓN = datos organizados/visualizados (dashboards); CONOCIMIENTO = asimilación inteligente que permite anticiparse (ej. regla "si un paciente pasa >15 días en UCI probablemente se infecte con la bacteria x" → alerta temprana). "Deificación" de los datos: parciales, sesgados, con ruido e intencionalidad; "efecto embudo" (realidad→vector numérico estructurado, pérdida de representatividad); "caja del matemático" (más robusta la técnica → menos matices: la lógica clásica maneja ∀ y ∃ pero no "la mayoría", que además es contextual); los datos "no estructurados" no existen para las herramientas: hay que estructurarlos (TF-IDF, stop words, stemming; se pierde la semántica, p.ej. la ironía). Almacenamiento: SQL/NoSQL; bases documentales (MongoDB), gráficas (Neo4j), columna ancha (DynamoDB), clave-valor (HBase, Map-Reduce); nube (Colab); DATA LAKE.
METODOLOGÍA de 8 fases: viabilidad (test de Slagel); descripción (clasificación, segmentación, predicción, pronóstico, prescripción, estimación...); alcance; adquisición del conocimiento (entrevistas, emparrillados, casos tipo, Delphi, grupo nominal, brainstorming, veinte preguntas...); representación (taxonomía, ontologías, reglas); inferencia/razonamiento aproximado + ML; evaluación; documentación (datos y conocimiento interactúan, AAAI-MAKE).
EJEMPLO 1 (radicalización en redes): taxonomía con variables lingüísticas (rasgos conductuales, características personales, ambientales): principios radicales RP1 (ideales radicales), RP2 (legitimar terrorismo); incitación a la violencia IV1 (especificar lugar/fecha), IV2 (focalizar), IV3 (instigar). Base de conocimiento con reglas borrosas (números borrosos normalizados y convexos), MPG; entradas de Twitter: etiqueta + seguidores, likes, retweets. Sin datos etiquetados: ontología de dominio (12 temas; conceptos similares de ConceptNet, cercanos como reforzadores) construida con TF-IDF, LDA, gradiente integrado con LSTM y conocimiento experto. Tuit de ejemplo (9.737 seguidores, 35 RT, 238 likes): temas 1 y 5 → regla "T1 y T5 → RP1" → inferencia borrosa → "grado medio de radicalización con confirmación alta".
EJEMPLO 2 (covid-19 y bolsa): estadística/ML fallan en puntos de inflexión (FC Barcelona 2018 y 2019: 3-0 y eliminado); S&P500 −30% en 20 días; análisis técnico (hombro-cabeza-hombro, doble suelo/techo); epidemias 1981-2016; MSCI World +3.08% a 3 meses y +8.50% a 6; caída 24-feb a 19-mar-2020: S&P −29.55%, Dow −33.33%, Ibex −41.05%, FTSE MIB −43.88%... Conocimiento extraído (3 factores: gestión política, económica, sanitaria) como reglas: PIB alto/inversión alta/buena gestión sanitaria → recuperación a mediados de 2020; gestión sanitaria baja pero política alta → finales de 2020; turismo muy afectado (Italia, Francia) o México/Canadá → principios de 2021; gestión política baja (UK, Brasil) → principios de 2021; gestión económica baja (Rusia, Australia) → mediados de 2021.

== 11. TESIS DOCTORAL de J.A. Olivas "Contribución al estudio experimental de la predicción basada en categorías deformables borrosas" (UCLM, junio 2000; director Enric Trillas) ==
Teoría de PROTOTIPOS BORROSOS (Zadeh 1982), categorías prototípicas borrosas y deformables, KDD/DCPB, razonamiento borroso no monótono y marcos, aplicada al sistema experto INCEND-IA de predicción de incendios forestales en Lugo (Galicia). Partes útiles para el examen: cap. 2 y Apéndice 1.
INTRODUCCIÓN: IA ciencia experimental; Ingeniería del Conocimiento → Sistemas Basados en el Conocimiento (método más heurístico que algorítmico). En fenómenos CÍCLICOS una situación no se repite exactamente → conviene ADAPTAR (deformar) los prototipos al caso real (proceso inverso al habitual: asimilar el caso al prototipo). Los técnicos usan un "prototipo de comportamiento" con datos imprecisos e inciertos → lógica borrosa + teoría de prototipos. IA y LB: la lógica binaria dominó (Shannon: circuitos ↔ booleanos; LISP); Minsky y McCarthy vieron errado el "armamentarium" borroso; razonamiento de sentido común; razonamiento NO MONÓTONO (nueva información cambia conclusiones); marcos, reglas, redes semánticas usan lógica bivaluada; LB los extiende (razonamiento aproximado + lógica posibilística). Prototipo psicológico: gorrión de "pájaro"; Bremermann: prototipo deformable (reconocimiento de patrones, caracteres manuscritos como imitaciones distorsionadas). KDD (Fayyad): todo el proceso de descubrir conocimiento útil; Data Mining = un paso. Aportaciones: emparrillados borrosos, DCPB (modificaciones de ID3 y CART), base de conocimientos con marcos y razonamiento no monótono, Categorías Prototípicas Borrosas y Deformables, sistema en C++.
CAP. 2. PSICOLOGÍA DE LA CATEGORIZACIÓN: la información negativa se procesa peor (ambigua); conceptos conjuntivos se aprenden mejor que disyuntivos (Bruner); Rosch: concepto = prototipo con rasgos compartidos en distinto grado (gorrión 10, murciélago 5, pingüino 3). Seis cuestiones: categorías no arbitrarias (nivel básico de Rosch: acciones motoras similares, forma genérica, imagen mental); miembros NO equivalentes (representatividad: velocidad de proceso, orden de producción de ejemplos, cercas semánticas "técnicamente un pájaro", asimetría de similaridad, aprendizaje; Rosch y Mervis: más atributos comunes con su categoría ⇒ menos con otras); límites BORROSOS; abstracción (prototipos por tendencia central son los más simples); descomposición vs. holismo; atributos (características vs. dimensiones; separables vs. integrales; partes, físicos, relacionales, funcionales). Conclusiones: (1) categorías con estructura interna de grados de representatividad, (2) límites no nítidos, (3) relación estrecha entre clusters de atributos y categorías. Teoría "ingenua": pertenencia≠representatividad (autogiro vs Boeing 747); el prototipo no es el máximo representante (modelo de pasarela).
PROTOTIPO DE ZADEH (1982): (a) un objeto puede pertenecer completamente sin representar bien; (b) el prototipo es un ESQUEMA BORROSO, no un objeto; (c) prototipicalidad = grado. P(s1..sn) vago = distribución de posibilidad; ejemplares buenos, fronterizos y malos: P=Alto/{buenos}+Medio/{fronterizos}+Bajo/{malos}; PT(P)=Alto/PT(P buenos)+Medio/PT(P fronterizos)+Bajo/PT(P malos) (reunión, no valor simple).
CATEGORÍAS PROTOTÍPICAS BORROSAS: (1) categorías descubiertas por clustering jerárquico (emparrillados); resultados en tablas-marco (Prototipos Conceptuales); (2) tantas categorías como requiera el problema (partición sobre el DOMINIO, no sobre cada concepto; INFEDEC >200 enfermedades); (3) term-set con un número borroso por categoría sobre el dominio unidimensional (agregación con medias de parámetros normalizados); uno o varios CONTEXTOS guían el clustering.
KDD BORROSO: propiedades de un patrón: validez, novedad, utilidad, simplicidad, generalidad. Fuzzy clustering: Ruspini 69, unimodales (Gitman), covarianza borrosa (Gustafson), ISODATA (Dunn), FUZZY C-MEANS (Bezdek; convergencia, validez). CONTEXTOS: un atributo (A:Y→[0,1], p.ej. "evolución de la siniestralidad=escasa"), varios (A×B), lógicamente compuesto, relacional, de regresión. FUZZY C-MEANS: Q=Σ_{i=1..c}Σ_{k=1..N} u_ik²·||x_k−v_i||², U=[u_ik] matriz de partición (Σ_i u_ik=1, 0<Σ_k u_ik<N), c clusters, v_i prototipo; u_ik=1/Σ_j(||x_k−v_i||/||x_k−v_j||)²; v_i=Σ_k u_ik² x_k/Σ_k u_ik². CONTEXTUAL: el contexto f_k=A(k) (nivel de integración de x_k con el contexto) actúa de filtro: Σ_i u_ik=f_k y u_ik=f_k/Σ_j(||x_k−v_i||/||x_k−v_j||)²; si f<f' menos patrones en el contexto f'. Clustering en ESPACIO LINGÜÍSTICO INDUCIDO (marcas lingüísticas transforman el espacio; el clustering pasa a clasificación). Similaridad entre clusters de dos contextos: (Ω≡Π) media de (Ω_i≡Π_j); si (Ω≡Π) alta y (A1≡A2) baja hay que respetar la naturaleza relacional (no pasar a reglas); cuanto menor (Ω≡Π)→(A1≡A2) más se desaconseja describir los patrones de forma funcional.
DCPB (Descubrimiento de Conocimiento Prototípico Borroso): KDD modificado: datos→selección→preproceso→transformación→data mining→prototipos→conceptualización; el DM se guía por HEURÍSTICAS del preproceso y por CONTEXTOS A1..An, cada uno con sus clusters; modelo modular y TRANSPARENTE (no caja negra). La deformación se basa en la afinidad (como retropropagación del error).
PROTOTIPOS DEFORMABLES (reconocimiento de patrones): retícula discretizada; características (correlación con la retícula, máscaras, Fourier, momentos, topología, métricas); clases linealmente separables o no; diagnóstico médico como reconocimiento de patrones. IMPLEMENTACIÓN DE HODGES: e_i(objeto,p1..pn)=|objeto−prototipo_i(p1..pn)| (mínimo = mejor coincidencia); no pondera parámetros → FUNCIÓN DE DISTORSIÓN d(p1..pn) y AFINIDAD afin(objeto)=min_{p}(e_i+w·d) (afin(prototipo)=0; bajo = buena coincidencia); función de pertenencia μ("objeto")=1−afin("objeto")/max(afin). CATEGORÍA PROTOTÍPICA DEFORMABLE BORROSA = combinación lineal de categorías prototípicas borrosas con coeficientes = grados de pertenencia: C_real(w1..wn)=Σ_i µ_pi·|p_i(v1..vn)|; el caso real se representa como un MARCO.
RAZONAMIENTO BORROSO NO MONÓTONO (Castro y Trillas): conflicto entre "X es A" e "Y es B" cuando A∩B=∅ (proposición conflictiva "X es U"); función MEDIA m con A∩B≤m(A,B)≤A∪B. Tipos: por DEFECTO ("si X es estudiante entonces joven", salvo que se sepa lo contrario: m(B1,B2)=B1∩B2 si ≠∅, si no B2); comportamiento PROTOTÍPICO (sin información, valor borroso más común: casa de tamaño medio); asunciones de MÍNIMO COSTE (animal desconocido → muy peligroso); reglas borrosas COMPLEMENTARIAS (dos reglas en conflicto → media aritmética ponderada generalizada m(A,B)(x)=sup_a A(a)∧B((x−(1−p)a)/p), geométrica ponderada generalizada, o aritmética ponderada borrosa p·A(x)+(1−p)·B(x), p∈[0,1]).
CAP. 3-4. INCEND-IA: SIG (rejilla ráster de 1 km²) + ayuda a la decisión (predicción, redistribución de recursos); viabilidad con IDEAL (plausible, justificado, adecuado, éxito asegurado); Visual C++/MFC, Access. Datos: 3.204 incendios de Lugo 1991-92 (de ~12.000 de Galicia); preproceso (fechas como tipo Fecha, valores perdidos=0, 40 campos de recursos → PERSONAL y MEDIOS); CICLO = incendios en días consecutivos (se cierra con >2 días de diferencia) → 37 ciclos. La siniestralidad evoluciona como SIGMOIDE en 3 SECTORES (lento; alto crecimiento en nº; estabilización en nº con aumento de peligrosidad); prototipos escasa/mediana/altamente progresiva. Emparrillados: 7 construcciones (nº incendios, superficie arbolada, rasa, especialistas, brigadas, medios, días; escala 1-5); matriz de proximidad 37×37 con s=100−100·d/(D·n) (D=4, n=nº de construcciones), agrupando por el MÍNIMO de similitud → dendrograma. MEDIDA HEURÍSTICA: [1·sup.arbolada+0.5·sup.rasa]/100: <0.4 escasa, 0.4-1 mediana, ≥1 alta. Prototipos como NÚMEROS BORROSOS TRIANGULARES iguales: centros = medias de los casos que el experto asigna a cada prototipo (elevada 0.791, media 0.550, escasa 0.233); base = distancia de 0 al primer centro (si C1+C3<1, amplitud 1−C3). Factores de ciclo: sequedad estacional {Alta/0.95, Media/0.45, Baja/0.05}, intensidad de la lluvia {Llovizna/0.9, Tormenta/0.5, Borrasca/0.1}, influencia social {Mucha/0.85, Media/0.45, Escasa/0.05}. También ID3 (mayor decremento de ENTROPÍA) y CART (GINI, divisiones binarias, poda por tasa de ramificación).
PREDICCIÓN: día 1 del ciclo: M(f1,f2,f3)=media=r; grados µp1(r),µp2(r),µp3(r); afines = µ≠0; se DEFORMAN todas las afines: C_real=Σµ_pi|p_i| (ej. {Media 0.45, Tormenta 0.5, Mucha 0.85} → M=0.6 → µp1=0, µp2=0.82, µp3=0.28); si afinidad solo con "escasa"/"media" se multiplican los valores por el grado; con dos, media aritmética ponderada. Diario: factores virulencia del día anterior, sequedad local (prob. de ignición), influencia social {Alta/0.9, Baja/0.6}, previsión de lluvias (reduce los incendios provocados). Equiparación (pattern matching) en 2 fases: (1) SECTOR (no hay retroceso): comparar nº de incendios, especialistas, brigadas, medios, virulencia, sequedad con los intervalos del sector (disonancia → siguiente sector); influencia social ≠0 → aviso y se estanca la evolución (máximo local); previsión de lluvias → aviso; (2) DÍA dentro del sector por menor distancia. Retroalimentación diaria → error alto al inicio y cada vez menor. REDISTRIBUCIÓN de recursos: PUNTOS SIGNIFICATIVOS con relevancia y cobertura; cobertura=proximidad(1/dx o 1/dy)·movilidad; repetir: tomar el punto menos cubierto (α<umbral) y mover el recurso que más lo cubre; INTERBLOQUEO si los movimientos ciclan (soluciones: umbral=cobertura mínima y omitir el último movimiento, reducir el umbral y reejecutar, avisar al usuario); complejidad ≤ cuadrática (N·R·P).
CAP. 5-6. Verificación (modelos correctos; otro ingeniero) y validación (responde a su fin; expertos, casos de prueba, funcionamiento paralelo en la central de Lugo julio-septiembre; ciclo 6-18 agosto 1998): tendencia adecuada, desviaciones en los picos, ~80% de aciertos con los intervalos de análisis. Problemas teóricos y soluciones: notación de prototipo para información cíclica → Categorías Prototípicas Borrosas; descubrirlas → DCPB; formalizarlas → tabla-marco + número borroso; deformarlas → Categorías Prototípicas Deformables Borrosas (Bremermann); compararlas → equiparación de marcos con razonamiento borroso no monótono. INEFECTIVO: redes neuronales (Kohonen para prototipos; perceptrón multicapa no válido para ciclos dinámicos) y algoritmos genéticos (difícil codificar los datos). PARADOJA: cuanto mejor la predicción, peor la similitud con lo real (las medidas aconsejadas reducen los incendios). Aplicable a patrones cíclicos y a situaciones estáticas (diagnóstico).
APÉNDICE 1. Método de trabajo de un SBC: definición del problema, viabilidad (test de Slagel), adquisición del conocimiento (proceso paralelo; cuello de botella; fuentes: manuales, documentos, registros, presentaciones, visitas, expertos, directivos, usuarios), representación, implementación (prototipos incrementales). KDD (Fayyad): "proceso no trivial de identificar patrones válidos, nuevos, potencialmente útiles y comprensibles en datos". Algoritmo de DM = modelo (función: clasificación, clustering, resumen, secuencias...; representación) + criterio de preferencia + algoritmo de búsqueda.
EMPARRILLADOS (Repertory Grids; Kelly 1955, Personal Construct Theory): CONSTRUCCIONES (bipolares con escala 1-5) × ELEMENTOS. Ejemplo (O1..O6, 6 construcciones, escala 1,3,5): d(O1,O2)=16, d(O3,O4)=8, d(O2,O6)=22; s=100−100d/(D·n) (D=4,n=6): máximo O1-O4=92%; grupo (O1,O4) con similitud = MÍNIMO con sus miembros ((O1,O4)-O2=min(33,25)=25); luego (O2,O5) 75%, [(O1,O4),O6] 67%, [(O2,O5),O3] 58%, los dos grupos finales 8% → dendrograma con 2 clases; también se pueden comparar construcciones invirtiendo una.
INDUCCIÓN: entrenamiento supervisado (ejemplos con solución) vs no supervisado; sobreaprendizaje. CLS (Hunt 1966), ID3 (Quinlan 1986: de arriba abajo, divide y vencerás, conjuntos puros): entropía I(N)=−ΣP(N,Ci)log2P(N,Ci); ΔI(N,S)=I(N)−ΣP(Nh_i)I(Nh_i) (elegir el mayor); para clases X,Y,Z: I=−Σ(x/(x+y+z))log2(...), E(A)=Σ((x_i+y_i+z_i)/(x+y+z))·I(x_i,y_i,z_i), ΔI(A)=I−E(A); se para si impureza<Hmin. CART (Breiman 1984): solo divisiones BINARIAS; GINI I(t)=Σ_{i≠j}p(i|t)p(j|t) (sesgo hacia atributos con más valores) o TWOING (dos superclases; ineficiente); clase por pluralidad; PODA por mínimo coste-complejidad Rα(T)=R(T)+α·Tc(T) (Tc=nº de hojas).
RAZONAMIENTO NO MONÓTONO: Piolín (todas las aves vuelan; si es avestruz/pingüino/muerto se retira "vuela"); requiere razonamiento metanivel. TMS de Doyle 1979, ATMS de De Kleer 1986, lógicas por defecto (Reiter 1980), NEGACIÓN POR FALLO (Clark 78; hipótesis de mundo cerrado: lo no deducible se asume falso; Prolog; no monótono: si P pasa a ser deducible se retraen las consecuencias de ¬P; complección E1∨..∨En↔P), CIRCUNSCRIPCIÓN (McCarthy 1980). MARCOS (Minsky 1975): slots con dominios (ej. "Enfermedad gripal": fiebre, escalofríos, congestión, tratamiento, baja); atributos discriminantes e inferibles; colección o jerarquía de marcos; inferencia por marco pregunta + pattern matching (nítido o borroso) y síntesis; tras encajar se asumen por defecto los slots no dados; en jerarquías la no monotonía surge por EXCEPCIONES (A=a,B=b⇒C=c pero con E=e ⇒ C=k). RAZONAMIENTO APROXIMADO: como en boletic (lógica clásica caso especial; posibilística de Dubois y Prade: peso α∈[0,1] = cuánto se cree la proposición, escala ordinal, distinto de la probabilística de Nilsson). SIG: 5 componentes (hardware, software, datos, personas, métodos); vectorial vs ráster; geocodificación; tareas: carga, manipulación, administración, consulta y análisis (proximidad/"buffering", superposición), visualización.
APÉNDICES 2-3. Incendios forestales (contexto: 1994 peor año de España, 437.635 ha; causas 42.6% provocados; FUEGO: 9-12 satélites infrarrojos, detección ~15-18 min; LATUV: riesgo en celdas de 10×10 km por NDVI, 0-4). Otras aplicaciones del método: multisensor de SnO2 con 32 sensores (prototipos = 4 combustiones: maleza P1, arbustos P2, caducifolios P3, perennes P4 + estado normal; resistencia fraccional RF=(R_gas−R_aire)/R_aire; centros c_i=Σw_i·RF_i/32; triángulos solapados; ej. r=0.74 → µ(P2)=0.11, µ(P3)=0.82, µ(P4)=0.43 ⇒ P3 caducifolios) e INFEDEC 2.1 (diagnóstico y tratamiento de infecciones respiratorias; hipótesis = prototipos con grado de confirmación, de falsación y credibilidad; conjeturas y refutaciones de Popper).
[OJO] Con centros 0.233/0.550/0.791 y base 0.233, M=0.6 daría µ≈0.79 y ≈0.18 (no 0.82 y 0.28): el ejemplo no se reproduce exactamente. El factor de multiplicación para afinidad solo con "altamente progresiva" se corta en el PDF ("2−…").
"""

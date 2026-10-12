# PROPUESTA de subsección para MEMORIA_TFM.md (no integrada; para revisión del autor)

> Redactada el 2026-10-06 por Claude Code y revisada por Codex (ronda 45; sus 7 correcciones están aplicadas). Números tomados de `e20-puntos-debiles-v1/logs_ind/e20_pd/n96/` (N96_b0.json, N96_sintetico.json, N97_*.json, N98_*.json, N98D*.json) y del plan `TS-LIF 1000 NEURONAS/plans/PLAN_MEJORA_E20_A0C_LIBROS_v1.md`.
>
> - **Ubicación sugerida:** nueva subsección al final de §6.3 (6.3.12, o tras 6.3.6 renumerando).
> - **Añadidos asociados** (si se integra): una fila en el Apéndice A y una nota en el Apéndice C sobre la cohorte 2.
> - **Referencias nuevas:** Huang y Petukhina (2022); Moulin y Veeravalli (2019); Murphy (2022); Haykin (2009); Eliasmith y Anderson (2003); Peixeiro (2026). Hay que verificar el formato APA y los años con los PDF antes de citarlas.

#### 6.3.12. Hipótesis derivadas de la literatura de referencia y regularización de la lectura

Se revisaron seis libros de referencia en series temporales, inferencia estadística, aprendizaje automático y neurociencia computacional, y se derivaron hipótesis concretas para la lectura y las entradas de E20-A0C.
- Todas se preregistraron y se revisaron con un segundo sistema de IA antes de ejecutarse.
- Se evaluaron sin tocar los bloques reservados ni la prueba final congelada:
  - primero en el bloque de cribado de BTC (B0, 2019-10 → 2021-08; tercer uso, con el percentil 0,714 fijado para siete contrastes; B0 sigue siendo un cribado exploratorio por sus usos anteriores);
  - después en tramos de ETH y PAXG a 2 h que nunca se habían evaluado.

**Tabla 22.** Hipótesis de la literatura: diferencias de AUC [IC95], salvo H4, que mide acierto en el 20 % de mayor confianza [N96–N98].

| Hipótesis (fuente) | Sintético | BTC B0 | ETH | PAXG | Veredicto |
|---|---|---|---|---|---|
| H1: entrada $r_t/\tilde\sigma_t$ con GARCH en lugar de $r_t$ (Huang y Petukhina, cap. 6) | −0,0093 [−0,0187; −0,0021] | +0,0057 [−0,0005; +0,0121] | — | — | No pasa |
| H3: canal de régimen filtrado MS-AR + CUSUM (Huang y Petukhina, cap. 8; Moulin y Veeravalli, cap. 9) | +0,0223 [+0,0085; +0,0347] | +0,0092 [+0,0039; +0,0142] | −0,0002ᵃ | −0,0013ᵃ | No pasa (B0 < +0,010) |
| H4: salida moderada probit para la selección (Murphy, §10.5.2) | — | +0,0069ᵇ [−0,0069; +0,0245] | — | — | No pasa |
| H2: C elegida con validación temporal estricta, frente a C = 1e−3 (Murphy, §4.5.5; Haykin, ec. 2.27) | — | +0,0036 [+0,0010; +0,0062] | +0,0062 [−0,0008; +0,0141]ᶜ | +0,0096 [+0,0014; +0,0173]ᶜ | Regla reproducible |

ᵃ Añadir H3 a PAR (E20 + 62 indicadores + C22) en el tramo temprano de ETH y PAXG [N97].
ᵇ Diferencia de acierto en el 20 % de mayor confianza, no de AUC.
ᶜ Tramo medio (40–70 %) de ETH y PAXG: los mismos 62 canales con C = 1e−5 (la elegida por la regla) frente a C = 1e−3 [N98-D2, diagnóstico descriptivo].

**Resultados:**
- **Sustituir el retorno por la normalización GARCH degradó el control sintético y no superó la criba en BTC B0.**
  - En el sintético GARCH, la estimación recuperó la volatilidad (correlación 0,998), pero sustituir $r_t$ por $r_t/\tilde\sigma_t$ empeoró a E20.
  - Un cálculo previo explica el techo: con una señal lineal en unidades estandarizadas, el AUC (una medida de rangos) solo puede ganar ≈ 0,003 al normalizar, porque el signo del retorno se conserva (banco S1, semilla 96: oráculo 0,6136; ordenar por $r_t$, 0,6108; por $r_t/\sigma_{EWMA}$, 0,6134). Esto vale bajo ese modelo lineal; no es un límite general del AUC.
- **El canal de régimen funcionó en el sintético**, donde la dirección cambia de signo entre regímenes persistentes, pero en BTC B0 quedó por debajo del umbral preregistrado. En los tramos tempranos de ETH y PAXG no se detectó una mejora al añadir H3M a PAR.
- **En el diagnóstico de los tramos medios, el cambio de C reprodujo casi toda la mejora puntual frente a BASE; su IC excluyó cero solo en PAXG.**
  - Una validación temporal estricta dentro del entrenamiento, con todas las escalas recalculadas en el 80 % inicial, eligió C = 3e−4 en BTC y C = 1e−5 en los tramos medios de ETH y PAXG.
  - En esos tramos, cambiar C de 1e−3 a 1e−5 con los mismos 62 canales elevó el AUC +0,0062 y +0,0096 (el IC95 excluye cero solo en PAXG).
  - Añadir conjuntamente C22 y el cambio asociado del número de canales dejó diferencias de +0,0004 y −0,0003. Este control es descriptivo: no separa ambos efectos ni demuestra que la regla generalice.

**Comparación con el aprendizaje automático:** en los tramos medios, BASE con la C elegida quedó aproximadamente 0,004 AUC por debajo de GBM; en los tramos tempranos, la diferencia de V frente al mejor rival fue cercana a cero. Ningún brazo superó al aprendizaje automático.
- En el tramo temprano de ETH y PAXG fue no inferior con el margen práctico de 0,010: −0,0010 [−0,0070; +0,0054] y +0,0010 [−0,0091; +0,0083].
- En el tramo medio, la no inferioridad conjunta no se cumplió: ETH −0,0036 [−0,0087; +0,0012]; PAXG −0,0043 [−0,0113; +0,0024].

**Interpretación:** la literatura aportó una regla verificable para elegir C sin consultar la evaluación. Es una mejora de procedimiento que reduce la brecha con el aprendizaje automático, no una ventaja arquitectónica de la red espigante. Elegir una C menor implica mayor penalización relativa de los pesos en la lectura logística. Es coherente con la utilidad de restringir una lectura flexible ante señal débil, pero no estima la razón entre varianza del ruido y varianza a priori de los pesos ni demuestra ese mecanismo.

**Prueba futura:** la configuración con esta regla (PAR) quedó preregistrada como brazo único de una segunda cohorte forward de BTC.
- La cohorte son las 8 000 barras de 2 h posteriores a las de la prueba congelada del Apéndice C.
- El script, la huella del código y las pruebas sin valor de evidencia quedaron congeladas antes de que exista ningún dato de esa cohorte.
- El criterio es la no inferioridad práctica (cota inferior > −0,010) y la superioridad (Δ ≥ +0,010 con cota > 0).

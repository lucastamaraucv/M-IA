; Base de Conocimiento (reglas) — Asesor borroso de señales de trading BTC
; Actividad 1, Razonamiento Aproximado (VIU)
;
; 2 variables de entrada (RSI, VOLATILIDAD) borrosas con 3 etiquetas cada
; una, 1 variable de salida (SENAL) borrosa con 5 etiquetas, y 7 reglas
; Mamdani. Universo de RSI en pares (valor grado) sobre [0,100], de
; VOLATILIDAD sobre [0,20], de SENAL sobre [-10,10].

(deftemplate RSI
	0 100
	(
		(sobrevendido (0 1) (30 1) (50 0))
		(neutral (30 0) (50 1) (70 0))
		(sobrecomprado (50 0) (70 1) (100 1))
	)
)

(deftemplate VOLATILIDAD
	0 20
	(
		(baja (0 1) (5 1) (10 0))
		(media (5 0) (10 1) (15 0))
		(alta (10 0) (15 1) (20 1))
	)
)

(deftemplate SENAL
	-10 10
	(
		(vender_fuerte (-10 1) (-8 1) (-4 0))
		(vender (-8 0) (-4 1) (0 0))
		(mantener (-4 0) (0 1) (4 0))
		(comprar (0 0) (4 1) (8 0))
		(comprar_fuerte (4 0) (8 1) (10 1))
	)
)

(defrule R1
	(RSI sobrevendido)
	(VOLATILIDAD baja)
=>
	(assert (SENAL comprar_fuerte))
)

(defrule R2
	(RSI sobrevendido)
	(VOLATILIDAD alta)
=>
	(assert (SENAL comprar))
)

(defrule R3
	(RSI neutral)
=>
	(assert (SENAL mantener))
)

(defrule R4
	(RSI sobrecomprado)
	(VOLATILIDAD baja)
=>
	(assert (SENAL vender_fuerte))
)

(defrule R5
	(RSI sobrecomprado)
	(VOLATILIDAD alta)
=>
	(assert (SENAL vender))
)

(defrule R6
	(RSI sobrevendido)
	(VOLATILIDAD media)
=>
	(assert (SENAL comprar))
)

(defrule R7
	(RSI sobrecomprado)
	(VOLATILIDAD media)
=>
	(assert (SENAL vender))
)

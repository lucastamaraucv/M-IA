"""
App de bandeja del sistema (sin ventana de consola) que analiza archivos
con Claude Code.

- Solo lee archivos (PDF o imagen: png/jpg/jpeg/webp/bmp) que esten dentro
  de la carpeta PREGUNTAS (al lado de este script / del .exe).
- Mientras procesa, el icono de la bandeja cambia de color (sin lanzar
  notificaciones de Windows) para indicar el estado: naranja procesando,
  verde todo resuelto sin huecos, AMARILLO resuelto pero con al menos un
  hueco (una pregunta/ejercicio que no se logro capturar/resolver bien,
  visible como "Q<numero>: null" en el hover), rojo error, gris info.
- Al terminar, guarda el resultado en t.txt junto con los archivos que lo
  originaron (en PREGUNTAS/procesado o en la carpeta REPASAR de la sesion).
- Boton "RJ3" (Resolver Jupyter, Practica 3): resuelve el notebook real
  (.ipynb) de PRACTICA3_DIR identificando los ejercicios con la
  herramienta Read, escribiendo la solucion directamente en sus celdas
  con NotebookEdit y verificando el notebook COMPLETO con
  "nbconvert --execute".
- Boton "RJ3C": metodo ALTERNATIVO/redundante a RJ3 para resolver el
  MISMO notebook -- en vez de leerlo con Read, identifica que ejercicios
  atacar a partir de capturas de pantalla, pero el resultado final
  tambien queda escrito y verificado en el notebook real (mismo rigor
  que RJ3: script aislado + nbconvert del notebook completo). RJ3 y RJ3C
  comparten `_jupyter_answered`: ninguno pisa lo que el otro ya resolvio.
- Antes de que RJ3 o RJ3C toquen el notebook real, se guarda un backup
  con fecha/hora en PRACTICA3_DIR/backups (ver _backup_notebook): red de
  seguridad por si una edicion automatica sale mal.
- Verificacion CRUZADA (ver _verificar_notebook_independiente): despues de
  que Claude responde, la app misma (sin pasar por Claude) vuelve a correr
  nbconvert sobre el notebook. Si encuentra un error real, no se da el
  intento por exitoso: se le manda ese error de vuelta a Claude en el
  siguiente intento (mismos reintentos, sin gastar de mas) para que lo
  corrija, en vez de confiar en que su propio reporte sea correcto.
- Hover de RJ3/RJ3C (compartido, alimentado por los bloques "@@Qn@@" que
  ambos metodos devuelven ademas de editar el notebook): NO reacciona al
  mouse (pedido explicito del usuario); se navega ejercicio por
  ejercicio, pagina por pagina si el codigo es largo, solo con
  Ctrl+Alt+N (siguiente) y Ctrl+Alt+B (atras).
- No abre ninguna ventana de CMD (compilar con --windowed).

--- Buenas practicas / lecciones de este proyecto (no romper esto) ---
- pystray tiene UN SOLO icono para toda la app: no se puede pintar un
  color distinto por boton del menu. El estado se comunica siempre
  cambiando ICONS["busy"/"ok"/"error"/"info"] del icono compartido, no
  con texto (icon.title). No agregues mensajes de "resolviendo..." /
  "listo" en el title: el usuario solo quiere guiarse por el color.
- Al resolver un ejercicio (Jupyter u otro), nunca asumas que una
  celda/respuesta ya esta bien resuelta solo porque "tiene contenido"
  o "no tira error de sintaxis": hay que verificar el comportamiento
  real contra lo que pide el enunciado. Ver PROMPT_TEMPLATE_JUPYTER.
- Toda solucion se verifica con DOS pasadas de ejecucion real, nunca
  con trazarlo mentalmente: (1) script .py aislado por ejercicio, (2)
  notebook completo con "python -m nbconvert --execute --inplace"
  (simula "Run All"). Preferi siempre la solucion mas simple y directa.
- El Bash que usa Claude para verificar esta restringido a
  "Bash(python:*)" (nada de rm/del directo): para limpiar archivos
  temporales hay que hacerlo con python mismo
  (python -c "import os; os.remove(...)").
- Reintentos por caida de internet (JUPYTER_MAX_RETRIES) tienen que
  vivir en Python alrededor de la llamada a "claude --print", nunca en
  el prompt: si no hay conexion, el proceso ni arranca, Claude no
  puede reintentarse a si mismo.
- Al compilar con PyInstaller (--windowed --onefile --icon=logo.ico),
  logo.png tiene que quedar FISICAMENTE al lado del .exe (no va
  empaquetado adentro): BASE_DIR = dirname(sys.executable) cuando esta
  frozen, y LOGO_PATH se arma a partir de ahi.
- El mutex de instancia unica (SINGLE_INSTANCE_MUTEX_NAME) lo puede
  estar reteniendo una sesion de debug de VS Code corriendo este mismo
  .py (proceso "debugpy"), no solo otro .exe: si un build nuevo se
  cierra solo sin mostrar nada, revisar procesos python con ese
  mutex/ese script antes de asumir que el build esta roto.
- El icono de la bandeja tiene DOS modos de hover mutuamente excluyentes,
  elegidos por _active_hover_mode ("test" o "rj3c"), porque solo hay un
  icon.title para mostrar a la vez: el modo "test" (Manual N1/CAR/N2)
  cicla automaticamente cada HOVER_CYCLE_INTERVAL_SECONDS mientras el
  mouse permanece encima, y reinicia desde el primero cada vez que el
  mouse re-entra. El modo "rj3c" es DISTINTO a proposito (pedido
  explicito del usuario): el MOUSE NO HACE NADA (ni al entrar ni al
  quedarse encima), solo se navega con Ctrl+Alt+N/Ctrl+Alt+B (ver
  on_rj3c_siguiente/on_rj3c_atras/_avanzar_pagina_rj3c). No agregues de
  nuevo un avance por hover del mouse en este modo sin que el usuario lo
  pida: se saco a proposito porque le generaba avances no deseados.
- CAR y RJ3C YA NO scrollean de forma automatica (se saco _scroll_down a
  pedido explicito del usuario: el auto-scroll fallaba cuando el usuario
  movia el puntero rapido durante la captura). _capture_pages solo
  sondea la pantalla y guarda una imagen cuando detecta cambios reales;
  el usuario scrollea a mano con su propio mouse/teclado. No reintroducir
  mouse_event/keybd_event de scroll aca sin que el usuario lo pida de
  nuevo explicitamente.
- RJ3C tampoco simula clic+Ctrl+G antes de capturar (a diferencia de CAR,
  que si lo sigue haciendo): pedido explicito del usuario porque esa
  combinacion interfiere con el software que usa para RJ3C (se comporta
  como si fuera un atajo tipo Ctrl+F ahi). El usuario enfoca la ventana
  el mismo antes de apretar RJ3C. No le agregues _activar_ventana_antes_de_capturar()
  de vuelta a rj3c_task sin que lo pida.
"""

import os
import re
import sys
import glob
import shutil
import subprocess
import textwrap
import threading
import traceback
import time
import ctypes
from ctypes import wintypes
import concurrent.futures
from typing import Any

from PIL import Image, ImageGrab, ImageChops, ImageDraw, ImageStat
import pystray  # type: ignore[import-untyped]

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PREGUNTAS_DIR = os.path.join(BASE_DIR, "PREGUNTAS")
PROCESADO_DIR = os.path.join(PREGUNTAS_DIR, "procesado")
# PREGUNTAS_DIR/PROCESADO_DIR y el flujo que los usaba (find_question_files,
# move_to_procesado, PROMPT_TEMPLATE, resolve_task) quedaron SIN USAR desde
# que el boton "Manual N1" se repunto a MANUAL_DIR (texto) el 2026-09-09; se
# dejaron en el archivo sin borrar por si se quiere recuperar ese flujo.
REPASAR_DIR = os.path.join(os.path.dirname(BASE_DIR), "PRACTICA")
# Carpeta fija (fuera de BASE_DIR, al lado de PRACTICA) donde el usuario
# pega/guarda a mano archivos .txt con preguntas de examen. El boton
# "Manual N1" las analiza (con la misma logica de sesion acumulativa que
# CAR) en vez de capturar pantalla: no se crea si no existe, ya que es una
# carpeta que gestiona el usuario, no la app.
MANUAL_DIR = r"C:\Users\Lucas Tamara\Desktop\M IA\ALGORITMOS DE OPTIMIZACIÓN\MANUAL"
MANUAL_PROCESADO_DIR = os.path.join(MANUAL_DIR, "procesado")
MANUAL_VALID_EXTENSIONS = (".txt",)
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
LOG_FILE = os.path.join(BASE_DIR, "app.log")

# Resumen comprimido del material teorico del curso (Algoritmos de
# Optimizacion), leido UNA vez con open() normal de Python y embebido como
# texto plano al principio de cada prompt de preguntas (no via herramienta
# Read de Claude): asi Claude tiene siempre a mano la terminologia y el
# enfoque real de las clases antes de resolver cualquier pregunta.
CURSO_CONTEXT_PATH = os.path.join(BASE_DIR, "curso_algoritmos_optimizacion.md")

# Carpeta fija (fuera de BASE_DIR) donde viven los notebooks de la practica
# a resolver. A diferencia de PREGUNTAS, esta carpeta no se crea si no
# existe: es una carpeta de curso ya existente, no algo que gestione la app.
PRACTICA3_DIR = r"C:\Users\Lucas Tamara\Desktop\M IA\PYTHON PARA LA INTELIGENCIA ARTIFICIAL\PRACTICA\PRACTICA 4"

# Carpeta con el estilo de redaccion del usuario (estilo.txt), fuera de
# PRACTICA3_DIR, que Claude solo debe leer y aplicar cuando un ejercicio
# pide explicitamente una explicacion/justificacion en texto.
ESTILO_DIR = r"C:\Users\Lucas Tamara\Desktop\M IA\estilo"

# RJ3 y RJ3C editan el notebook REAL de PRACTICA3_DIR con NotebookEdit y
# despues lo ejecutan de punta a punta con nbconvert: si algo sale mal a
# mitad de una edicion automatica (una celda mal escrita, un nbconvert que
# se corta), no habia forma de recuperar la version de antes. Por eso,
# antes de tocar el notebook, se guarda una copia con fecha/hora aca (pedido
# explicito del usuario, mejora de "alto impacto" dado que ahora dos
# metodos con IA editan sin supervision su archivo real de la materia).
NOTEBOOK_BACKUPS_DIR = os.path.join(PRACTICA3_DIR, "backups")

ANSWER_FILENAME = "t.txt"
ANSWER_FILENAME_N2 = "t_n2.txt"

VALID_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".webp", ".bmp")
JUPYTER_EXTENSION = ".ipynb"

HOTKEY = "ctrl+alt+r"
REVIEW_HOTKEY = "ctrl+alt+9"  # avanza una pregunta/respuesta por pulsacion en el tooltip
# Mientras el puntero del mouse permanece sobre el icono de la bandeja, se
# recorre automaticamente una pregunta/respuesta cada HOVER_CYCLE_INTERVAL_SECONDS,
# en bucle, sin necesidad de pulsar Ctrl+Alt+9. Ver _icon_screen_rect().
HOVER_CYCLE_INTERVAL_SECONDS = 2.0
# El tooltip de la bandeja de Windows tiene un limite fisico de caracteres
# (128 WCHAR en el buffer NOTIFYICONDATA.szTip desde Windows 2000/XP, ver
# _paginas_rj3c): se deja un margen chico de seguridad en vez de ir al
# limite exacto. El hover de RJ3C muestra codigo, que puede ser largo, asi
# que lo que no entra en este limite se reparte en paginas (ver
# _paginas_rj3c/_avanzar_pagina_rj3c) en vez de truncarse: el codigo
# COMPLETO de cada ejercicio siempre se ve, pagina por pagina.
RJ3C_TOOLTIP_MAX_CHARS = 126
RJ3C_NEXT_HOTKEY = "ctrl+alt+n"  # avanza un ejercicio en el hover de RJ3C, sin
# depender de mover el mouse (mas preciso que entrar/salir del icono con el puntero).
RJ3C_PREV_HOTKEY = "ctrl+alt+b"  # retrocede un ejercicio en el hover de RJ3C
HOTKEY_POLL_SECONDS = 0.05  # frecuencia de sondeo del estado fisico de las teclas
VK_CONTROL = 0x11
VK_MENU = 0x12  # Alt
VK_R = 0x52
VK_9 = 0x39
VK_N = 0x4E
VK_B = 0x42
# Botones laterales del mouse como disparador alternativo: cuando el foco
# esta sobre una maquina virtual (VirtualBox, etc.) el teclado se captura
# a nivel de driver para el invitado y ningun atajo de teclado del host
# (ni por hook ni por sondeo de estado) llega a verse, pero los clics de
# mouse si pasan con normalidad.
VK_XBUTTON1 = 0x05  # boton lateral "atras" -> igual que Ctrl+Alt+R
VK_XBUTTON2 = 0x06  # boton lateral "adelante" -> igual que Ctrl+Alt+9
# Los botones laterales del mouse tambien son "atras/adelante" en cualquier
# navegador o el Explorador de Windows, asi que un solo clic no alcanza para
# disparar el atajo (se confundiria con navegacion normal): hacen falta DOS
# pulsaciones seguidas del mismo boton dentro de esta ventana de tiempo.
MOUSE_DOUBLE_PRESS_WINDOW_SECONDS = 0.5
CAPTURE_INTERVAL_SECONDS = 1.0  # frecuencia de sondeo de pantalla en _capture_pages
# mientras el usuario scrollea a mano (ya no hay scroll automatico, ver _capture_pages).
KEYEVENTF_KEYUP = 0x0002
VK_G = 0x47
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
# Antes de empezar a capturar, CAR simula Ctrl+G y despues un clic izquierdo
# en la posicion actual del cursor (pedido explicito del usuario, para
# activar/enfocar la ventana de la VM antes de scrollear). Como no se sabe
# que hace Ctrl+G en el software especifico de cada usuario, se deja
# documentado aca para poder ajustarlo facilmente si hiciera falta.
PRE_CAPTURA_ESPERA_SECONDS = 0.3  # pausa entre Ctrl+G, el clic y el inicio del scroll
MAX_CAPTURES = 60  # limite de seguridad si la pagina nunca deja de cambiar
STILL_FRAMES_TO_STOP = 2  # capturas seguidas sin cambios para asumir que llego al final
# Tolerancia de _same_image: diferencia promedio de intensidad de pixel (0.0
# a 1.0) por debajo de la cual dos capturas se consideran "la misma
# pantalla". Calibrado con evidencia real del 2026-09-09: pares de capturas
# confirmadas identicas por Claude midieron 0,0003%-0,95% de diferencia
# promedio (ruido de cursor/reloj/renderizado de VM). El margen se dejo
# DELIBERADAMENTE angosto (justo encima del 0,95% real): una prueba propia
# con un cambio de contenido chico pero realista (una sola linea de texto
# nueva) midio apenas 1,06%, muy cerca del ruido. Es preferible el costo
# menor de mandar alguna captura duplicada de mas a Claude (que igual la
# descarta sin inventar nada) que el costo mayor de tratar contenido nuevo
# real como "sin cambios" y perderlo en silencio.
SAME_IMAGE_DIFF_THRESHOLD = 0.01
SIN_CAMBIOS_AVISO = 2  # pulsaciones seguidas sin contenido nuevo antes de avisar que el scroll no avanza
START_DELAY_SECONDS = 3  # tiempo para posicionar el mouse sobre la ventana antes de empezar

EFFORT_N1 = "high"  # se aplica automaticamente en cada analisis
EFFORT_N2 = "xhigh"  # opcional, solo si el usuario lo pide desde el menu

# Si se manda demasiadas imagenes juntas en una sola llamada a "claude
# --print" (ej. 39 u 58, capturadas por REPASAR cuando el scroll fue lento)
# la peticion supera el limite de contexto y el CLI devuelve error sin
# mensaje util. Por eso las imagenes se envian en lotes.
BATCH_SIZE = 12
# Las imagenes de REPASAR se solapan entre si (son capturas consecutivas de
# scroll), asi que se repiten un par de imagenes entre lotes consecutivos
# para no cortar una pregunta justo en el borde entre dos lotes.
BATCH_OVERLAP_REPASAR = 2
# Los lotes se procesan en paralelo (varias llamadas a "claude --print" a
# la vez) para que una sesion grande no tarde N veces mas que una sola
# llamada; este numero limita cuantas llamadas simultaneas se lanzan como
# maximo, para no saturar la maquina ni la cuota de la API.
MAX_PARALLEL_BATCHES = 4

# Reintentos para el boton "Resolver Jupyter": en casa del usuario a veces
# se corta el internet a mitad de la llamada a "claude --print" (que
# necesita conexion para hablar con la API). Si la llamada falla, se
# reintenta el notebook completo varias veces con una espera entre
# intentos, en vez de marcar error a la primera caida de conexion.
JUPYTER_MAX_RETRIES = 6
JUPYTER_RETRY_DELAY_SECONDS = 30

# Timeout de cada llamada a "claude --print" para RJ3/RJ3C, mas largo que el
# generico de ask_claude (900s/15min, pensado para Manual N1/CAR/REPASAR que
# solo leen texto/imagenes). El trabajo de Jupyter es mucho mas pesado: leer
# el notebook entero, auditar cada celda, validar cada ejercicio en un
# script .py aislado, correr el notebook completo con Jupyter, escribir con
# NotebookEdit, y despues la verificacion independiente de la app -- puede
# superar los 15 minutos en un notebook grande sin que nada este realmente
# colgado.
JUPYTER_ASK_CLAUDE_TIMEOUT_SECONDS = 1800

# Verificacion INDEPENDIENTE del notebook (pedido explicito del usuario:
# control cruzado, no confiar solo en que Claude reporte haber verificado el
# mismo con su propio nbconvert dentro de la llamada). Despues de que
# Claude responde, la app misma -- con su propio subprocess.run, sin pasar
# por Claude -- vuelve a correr nbconvert sobre el notebook. Si encuentra un
# error real, NO se da por resuelto: se le manda ese error de vuelta a
# Claude en el proximo intento (dentro de los mismos JUPYTER_MAX_RETRIES/
# REPASAR_MAX_RETRIES, no consume reintentos aparte) para que lo revise y
# lo corrija especificamente, en vez de confiar en su propio reporte.
NBCONVERT_VERIFICATION_TIMEOUT_SECONDS = 600

# Reintentos para cada lote de Manual N1 / CAR / N2: fallas transitorias
# (caida momentanea de internet, o un fallo puntual al invocar el CLI) no
# deberian tirar rojo el icono ni perder un lote entero a la primera. La
# espera es mas corta que la de Jupyter porque este flujo es interactivo
# (el usuario esta esperando el resultado en el momento, no una tarea de
# fondo larga).
REPASAR_MAX_RETRIES = 3
REPASAR_RETRY_DELAY_SECONDS = 5

# --- Estructura tipica del examen/repaso: el numero de preguntas varia en
# cada sesion (puede ser 17, 20, o cualquier otra cantidad), asi que el
# prompt NO asume un total fijo. Lo que si se mantiene siempre es la mezcla
# de tipos de pregunta (opcion multiple + respuesta numerica con coma
# decimal), asi que eso se le recuerda a Claude en cada analisis.
QUESTION_STRUCTURE_NOTE = """Contexto de este examen/repaso: la cantidad total de preguntas varia en
cada sesion (no asumas un numero fijo de antemano), y suele haber una
mezcla de dos tipos:
- Preguntas de opcion multiple: hay que elegir UNA alternativa correcta
  (a, b, c, d...).
- Preguntas de respuesta numerica directa (sin alternativas): el
  resultado se escribe como numero, y los decimales van con COMA, nunca
  con punto (ejemplo correcto: 3,5 -- incorrecto: 3.5).
Identifica correctamente cuantas preguntas hay en total en las imagenes/
archivos que tienes y clasifica cada una segun corresponda.

Debajo del enunciado de cada pregunta (y de sus alternativas, si las
tiene) hay un espacio en blanco reservado para escribir la respuesta,
antes de que empiece la siguiente pregunta. Usa ese espacio en blanco
como señal visual para saber donde termina una pregunta y donde empieza
la siguiente: no fusiones dos preguntas distintas en una sola, ni cortes
una lista de alternativas a mitad asumiendo que ya empezo la pregunta
siguiente.

Antes de escribir la tabla resumen, revisa que no repetiste ni te
saltaste ningun numero de pregunta de los que aparecen en las imagenes/
archivos que tienes ahora (si esta sesion se dividio en varios lotes de
imagenes, es normal ver solo una parte de las preguntas en cada lote),
y que cada respuesta numerica usa coma decimal. No inventes preguntas
que no esten en las imagenes/archivos."""

SINGLE_INSTANCE_MUTEX_NAME = "RepasarMatematica_SingleInstanceMutex"
ERROR_ALREADY_EXISTS = 183

# Colores del distintivo de estado en el icono de la bandeja (en vez de
# notificaciones de Windows): naranja mientras procesa, verde al terminar
# bien, amarillo si termino bien pero con huecos (preguntas/ejercicios que
# no se lograron capturar/resolver, ver _detectar_huecos -- pedido
# explicito del usuario para distinguir "todo perfecto" de "revisa algo"),
# rojo si hubo error, gris para "nada que hacer".
COLOR_BUSY = (243, 156, 18, 255)
COLOR_OK = (39, 174, 96, 255)
COLOR_WARNING = (241, 196, 15, 255)
COLOR_ERROR = (192, 57, 43, 255)
COLOR_INFO = (127, 140, 141, 255)

ICONS = {}

PROMPT_TEMPLATE = """{curso_context}Eres un experto en matematicas para IA. Lee con la herramienta Read
cada uno de estos archivos (son las preguntas de un examen, en PDF y/o
imagen, posiblemente repartidas en varios archivos/paginas):

{file_list}

{question_structure_note}

IMPORTANTE - contexto de ejecucion: esta llamada corre de forma automatica
y SIN SUPERVISION humana en tiempo real (es una unica ejecucion de "claude
--print"; nadie va a leer ni responder ninguna pregunta que hagas en tu
respuesta). Por eso:
- NUNCA hagas una pregunta de seguimiento ni pidas confirmacion antes de
  proceder (nada de "Querés que resuelva igual las que se ven?"): no hay
  nadie que pueda contestarte, y una respuesta asi deja todo sin resolver.
- Si con los archivos que tenes podes identificar y resolver ALGUNA
  pregunta (aunque falten otras paginas o el resto del examen), resolvé
  esas igual y agregalas a la tabla resumen; nunca dejes una pregunta
  visible y resoluble sin resolver solo porque falta el resto.
- Si genuinamente NINGUN archivo tiene contenido nuevo o resoluble (por
  ejemplo, todos muestran la misma pantalla repetida sin avanzar),
  decilo en UNA sola frase breve, sin generar ninguna fila en la tabla
  resumen para eso, y sin hacer ninguna pregunta de seguimiento.

Antes de responder, revisa TODOS los archivos una primera vez y arma un
inventario mental de los numeros de pregunta distintos que aparecen (el
numero real impreso, no uno inventado por ti). Si un archivo esta
cortado o la pregunta continua en otro archivo/pagina, une el contenido
antes de resolverla.

Resuelve TODAS las preguntas del inventario, una por una. Para cada
pregunta:
1. Reproduce el numero y el enunciado real de la pregunta tal como
   aparece en el archivo (no escribas solo "Pregunta 1", "Pregunta 2":
   incluye el texto original de la pregunta, incluyendo formulas,
   exponentes, fracciones, subindices, etc. en notacion de texto plano
   equivalente, ej. x^2, sqrt(x), (a+b)/c).
2. Transcribe TODAS las alternativas/opciones de forma literal y
   completa (a, b, c, d, etc., en el mismo orden en que aparecen), sin
   resumirlas ni omitir ninguna aunque sean largas o tengan formulas, si
   el archivo las tiene.
3. Explica en profundidad por que esa alternativa es la correcta: desarrolla
   el procedimiento paso a paso, el concepto o principio matematico que
   se aplica, y por que las demas opciones son incorrectas cuando
   aplique. El objetivo es que quien lea la justificacion entienda el
   razonamiento completo y pueda llegar a la respuesta por si mismo, no
   que se limite a leer una etiqueta corta al final.

Antes de escribir la tabla resumen, verifica: que no repetiste ningun
numero de pregunta, que no te saltaste ninguno de los que viste en el
inventario, y que cada respuesta numerica usa coma decimal (no punto).

Al final, agrega una tabla resumen con EXACTAMENTE este formato (una
linea por pregunta, sin encabezado, sin texto antes ni despues, usando
"|" como separador):
1 | b
2 | d
3 | 3,5

Usa el numero de pregunta y la respuesta final corta (la letra de la
alternativa si es opcion multiple, o el resultado numerico/coma decimal
si no hay alternativas). No agregues nada mas en esa tabla (ni palabras
como "Pregunta" o "Respuesta", solo numero, "|", respuesta corta).
Responde en texto plano, listo para guardarse en un .txt.

No escribas ninguna frase introductoria ni de cierre (nada de "a
continuacion resuelvo...", "espero que te sirva", etc.). Empieza
directamente con la primera pregunta y termina en la tabla resumen.
"""

PROMPT_TEMPLATE_REPASAR = """{ra_context}{curso_context}Eres un experto en matematicas para IA. Lee con la herramienta Read
cada una de estas imagenes, en el orden dado (son partes consecutivas
de una misma pagina de preguntas; puede haber contenido repetido entre
imagenes consecutivas por el solapamiento):

{file_list}

{question_structure_note}

IMPORTANTE - contexto de ejecucion: esta llamada corre de forma automatica
y SIN SUPERVISION humana en tiempo real (es una unica ejecucion de "claude
--print"; nadie va a leer ni responder ninguna pregunta que hagas en tu
respuesta). Por eso:
- NUNCA hagas una pregunta de seguimiento ni pidas confirmacion antes de
  proceder (nada de "Querés que resuelva igual las que se ven?"): no hay
  nadie que pueda contestarte, y una respuesta asi deja todo sin resolver.
- Si con las imagenes que tenes podes identificar y resolver ALGUNA
  pregunta (aunque falten otras paginas o el resto del examen), resolvé
  esas igual y agregalas a la tabla resumen; nunca dejes una pregunta
  visible y resoluble sin resolver solo porque falta el resto.
- Si genuinamente NINGUNA imagen tiene contenido nuevo o resoluble (por
  ejemplo, todas muestran la misma pantalla repetida sin avanzar, o el
  scroll nunca avanzo), decilo en UNA sola frase breve, sin generar
  ninguna fila en la tabla resumen para eso, y sin hacer ninguna
  pregunta de seguimiento.

Antes de responder, revisa TODAS las imagenes una primera vez y arma un
inventario mental de los numeros de pregunta distintos que aparecen (el
numero real impreso, no uno inventado por ti), descartando las
repeticiones por solapamiento entre imagenes consecutivas. Si una
pregunta aparece cortada en una imagen y completa (o con mas contexto)
en la siguiente, usa la version mas completa.

Resuelve TODAS las preguntas del inventario, una por una. Para cada
pregunta:
1. Reproduce el numero y el enunciado real de la pregunta tal como
   aparece en la imagen (no escribas solo "Pregunta 1", "Pregunta 2":
   incluye el texto original de la pregunta, incluyendo formulas,
   exponentes, fracciones, subindices, etc. en notacion de texto plano
   equivalente, ej. x^2, sqrt(x), (a+b)/c).
2. Transcribe TODAS las alternativas/opciones de forma literal y
   completa (a, b, c, d, etc., en el mismo orden en que aparecen), sin
   resumirlas ni omitir ninguna aunque sean largas o tengan formulas, si
   la imagen las tiene.
3. Explica en profundidad por que esa alternativa es la correcta: desarrolla
   el procedimiento paso a paso, el concepto o principio matematico que
   se aplica, y por que las demas opciones son incorrectas cuando
   aplique. El objetivo es que quien lea la justificacion entienda el
   razonamiento completo y pueda llegar a la respuesta por si mismo, no
   que se limite a leer una etiqueta corta al final.

Antes de escribir la tabla resumen, verifica: que no repetiste ningun
numero de pregunta, que no te saltaste ninguno de los que viste en el
inventario, y que cada respuesta numerica usa coma decimal (no punto).

Al final, agrega una tabla resumen con EXACTAMENTE este formato (una
linea por pregunta, sin encabezado, sin texto antes ni despues, usando
"|" como separador):
1 | b
2 | d
3 | 3,5

Usa el numero de pregunta y la respuesta final corta (la letra de la
alternativa si es opcion multiple, o el resultado numerico/coma decimal
si no hay alternativas). No agregues nada mas en esa tabla (ni palabras
como "Pregunta" o "Respuesta", solo numero, "|", respuesta corta).
Responde en texto plano, listo para guardarse en un .txt.

No escribas ninguna frase introductoria ni de cierre (nada de "a
continuacion resuelvo...", "espero que te sirva", etc.). Empieza
directamente con la primera pregunta y termina en la tabla resumen.
"""


PROMPT_TEMPLATE_MANUAL = """{curso_context}Eres un experto en matematicas para IA. Lee con la herramienta Read
cada uno de estos archivos de texto (son preguntas de examen escritas o
pegadas a mano por el usuario, posiblemente repartidas en varios archivos):

{file_list}

{question_structure_note}

IMPORTANTE - contexto de ejecucion: esta llamada corre de forma automatica
y SIN SUPERVISION humana en tiempo real (es una unica ejecucion de "claude
--print"; nadie va a leer ni responder ninguna pregunta que hagas en tu
respuesta). Por eso:
- NUNCA hagas una pregunta de seguimiento ni pidas confirmacion antes de
  proceder (nada de "Querés que resuelva igual las que se ven?"): no hay
  nadie que pueda contestarte, y una respuesta asi deja todo sin resolver.
- Si con los archivos que tenes podes identificar y resolver ALGUNA
  pregunta (aunque falten otras o el resto del examen), resolvé esas
  igual y agregalas a la tabla resumen; nunca dejes una pregunta visible
  y resoluble sin resolver solo porque falta el resto.
- Si genuinamente NINGUN archivo tiene contenido nuevo o resoluble,
  decilo en UNA sola frase breve, sin generar ninguna fila en la tabla
  resumen para eso, y sin hacer ninguna pregunta de seguimiento.

Antes de responder, revisa TODOS los archivos una primera vez y arma un
inventario mental de los numeros de pregunta distintos que aparecen (el
numero real indicado en el texto, no uno inventado por ti). Si una
pregunta esta cortada o continua en otro archivo, une el contenido antes
de resolverla.

Resuelve TODAS las preguntas del inventario, una por una. Para cada
pregunta:
1. Reproduce el numero y el enunciado real de la pregunta tal como
   aparece en el texto (no escribas solo "Pregunta 1", "Pregunta 2":
   incluye el texto original de la pregunta, incluyendo formulas,
   exponentes, fracciones, subindices, etc. en notacion de texto plano
   equivalente, ej. x^2, sqrt(x), (a+b)/c).
2. Transcribe TODAS las alternativas/opciones de forma literal y
   completa (a, b, c, d, etc., en el mismo orden en que aparecen), sin
   resumirlas ni omitir ninguna aunque sean largas o tengan formulas, si
   el texto las tiene.
3. Explica en profundidad por que esa alternativa es la correcta: desarrolla
   el procedimiento paso a paso, el concepto o principio matematico que
   se aplica, y por que las demas opciones son incorrectas cuando
   aplique. El objetivo es que quien lea la justificacion entienda el
   razonamiento completo y pueda llegar a la respuesta por si mismo, no
   que se limite a leer una etiqueta corta al final.

Antes de escribir la tabla resumen, verifica: que no repetiste ningun
numero de pregunta, que no te saltaste ninguno de los que viste en el
inventario, y que cada respuesta numerica usa coma decimal (no punto).

Al final, agrega una tabla resumen con EXACTAMENTE este formato (una
linea por pregunta, sin encabezado, sin texto antes ni despues, usando
"|" como separador):
1 | b
2 | d
3 | 3,5

Usa el numero de pregunta y la respuesta final corta (la letra de la
alternativa si es opcion multiple, o el resultado numerico/coma decimal
si no hay alternativas). No agregues nada mas en esa tabla (ni palabras
como "Pregunta" o "Respuesta", solo numero, "|", respuesta corta).
Responde en texto plano, listo para guardarse en un .txt.

No escribas ninguna frase introductoria ni de cierre (nada de "a
continuacion resuelvo...", "espero que te sirva", etc.). Empieza
directamente con la primera pregunta y termina en la tabla resumen.
"""


PROMPT_TEMPLATE_JUPYTER = r"""Eres un agente especialista en Python, refactorizacion y verificacion
cientifica de codigo. Tu objetivo es auditar, corregir y completar el
siguiente notebook de Jupyter. Leelo con la herramienta Read:

{notebook_path}
{feedback_note}

Contexto academico: este es un ejercicio de practica de un curso, sin
nota ni evaluacion formal. El profesor autorizo explicitamente el uso
de IA para analizar y corregir el codigo, y pidio resolver estos
ejercicios (de anios anteriores, compartidos por companieros de
cursadas pasadas, sin calificacion asociada) para reforzar el
aprendizaje. Procede a resolverlo con rigor tecnico, sin dudar ni
tratarlo como una evaluacion con peso academico.

Formato de estos ejercicios: es un Jupyter Notebook (.ipynb) con los
enunciados de los ejercicios y posibles archivos adjuntos. El espacio
de respuesta es obligatoriamente dentro de ese mismo notebook, en las
celdas que estan habilitadas para tal fin (nunca en un archivo aparte
ni en tu respuesta de texto libre). Puede que cada apartado indique un
valor en puntos de esa pregunta: es solo informativo, no cambia como
resolver el ejercicio ni le da mas o menos prioridad a ninguno.

Usa toda tu capacidad de razonamiento en cada ejercicio: no resuelvas
en piloto automatico ni apliques una receta generica. Antes de
escribir codigo, leele el enunciado con atencion completa las veces
que haga falta hasta entender con precision que contexto plantea, que
pide exactamente que el codigo haga, y que forma o tecnica exige (si
exige alguna). El notebook puede traer cualquier tipo de problema:
listas, matrices, diccionarios, texto/strings, recursividad,
clases/POO, archivos, matematica, estructuras de datos, o cualquier
otro; no asumas de antemano el tipo de problema ni la forma que va a
tener la solucion, dejate guiar unicamente por lo que ese enunciado en
particular describe. Andá ejercicio por ejercicio, uno a la vez, sin
apurarte a la siguiente celda hasta haber entendido y resuelto bien la
actual.

# Fase 1: recopilacion de contexto
Antes de abrir el notebook, revisa con Read si en esta misma carpeta
hay algun archivo .txt (ademas del notebook) con contexto adicional
que indique que hacer en cada ejercicio. Si existe, leelo primero; sus
indicaciones tienen prioridad si aclaran algo que el notebook deja
ambiguo. Si no hay ningun .txt, segui solo con lo que dice el
notebook.

Recorre TODAS las celdas del notebook en estricto orden secuencial y
asocia cada enunciado (en celdas markdown o en comentarios dentro de
celdas de codigo) con la celda o celdas de codigo que deben contener
su solucion.

La relacion entre enunciado y celdas de codigo NO es siempre "un
enunciado, una celda": lee el contenido real antes de asumir nada.
Un mismo problema puede venir dividido en varias celdas de codigo
consecutivas que dependen entre si (por ejemplo una celda define una
funcion/clase y la celda siguiente la usa o la prueba, o el enunciado
tiene partes "a)", "b)", "c)" cada una en su propia celda pero
compartiendo variables o resultados de las anteriores): en ese caso
todas esas celdas son UN SOLO ejercicio y hay que resolverlas como
una unidad coherente, respetando ese estado compartido entre ellas.
En otros casos, celdas consecutivas que a simple vista se ven
parecidas son en realidad ejercicios distintos e independientes
(cada uno con su propio enunciado, aunque no haya mucho texto
separandolos): ahi no hay que mezclar variables ni logica de un
ejercicio en el otro. Guiate por señales explicitas del propio
notebook (numeracion de ejercicios, encabezados markdown, si el
codigo de una celda referencia nombres definidos en una celda
anterior, etc.) para decidir en cada caso si estas ante un ejercicio
dividido en varias celdas o ante varios ejercicios distintos.

Si un enunciado NO tiene ninguna celda de codigo debajo (el notebook
no dejo un espacio en blanco para la respuesta, a diferencia de otros
ejercicios del mismo notebook que si lo tienen), NUNCA lo saltees ni
lo des por resuelto solo porque "no hay donde escribir": esa celda
faltante la vas a crear vos mismo en la Fase 3 con NotebookEdit
(edit_mode="insert"), inmediatamente despues de la celda del
enunciado, y ahi mismo resolves el ejercicio. La ausencia de una
celda de respuesta no es nunca una razon valida para dejar un
ejercicio sin resolver ni para que el resultado final indique exito
sin haberlo resuelto.

# Fase 2: protocolo de validacion empirica (en un script .py aparte)
Para que cada solucion quede respaldada con confianza, sin asumir
nada, se hacen exactamente DOS comprobaciones de ejecucion real (no
una sola): esta Fase 2, en un script .py aislado por ejercicio, y mas
adelante la Fase 4, ejecutando el notebook .ipynb completo con
Jupyter. Ninguna reemplaza a la otra: la Fase 2 es rapida y aisla cada
ejercicio para iterar, la Fase 4 confirma que tambien funciona en el
notebook real, en el orden real, con el resto de las celdas.

El criterio SIEMPRE es el mismo, sin importar el tipo de problema que
tenga la celda: primero entende con precision que es lo que el
enunciado pide que el codigo reciba, calcule, transforme o devuelva, y
despues juzga la celda contra ESE objetivo, no contra si "se ve
completa" o "tiene texto". Una celda puede estar vacia o con
placeholder ("# TODO", "pass", "...", etc.), tener un error de
sintaxis (no se ejecutaria tal cual esta), tener un error de logica
(corre sin romperse pero no hace lo pedido, o lo hace mal en algunos
casos), no existir directamente (el enunciado no tiene ninguna celda
de codigo debajo, ver Fase 1), o ya estar correcta y completa. No
asumas de antemano cual de estos casos es: puede haber cualquiera,
varios a la vez, o ninguno.

Cada ejercicio es distinto y puede fallar por motivos completamente
distintos: no asumas de antemano que el problema tipico es de
mutabilidad/aliasing (.copy()) solo porque fue el caso en algun
ejercicio anterior. Puede ser eso, o un error de indices, una
condicion mal planteada, un tipo de dato incorrecto, un calculo mal
hecho, un caso borde no contemplado, o cualquier otra cosa. Leele el
enunciado de CADA ejercicio con atencion y analizalo por su propio
contexto especifico, sin aplicar una lista fija de sospechosos
habituales.

Para decidirlo, NO te bases en trazar el codigo mentalmente: usa la
herramienta Bash para ejecutarlo de verdad con python (por ejemplo
escribiendo un script temporal .py y corriendolo con "python"). Esa
ejecucion es solo para verificar el comportamiento antes de decidir
que hacer; podes hacerla en un script aparte, no hace falta que sea
igual al notebook. Proba como minimo casos estandar (las entradas
normales descritas en el enunciado) y casos de borde (listas/
estructuras vacias, un solo elemento, tipos mixtos, etc.), y ademas
cualquier otra propiedad que el enunciado de ESE ejercicio puntual
exija (por ejemplo, si pide no alterar los datos de entrada, comproba
que no se muten por referencia; si pide un orden especifico,
comprobalo; etc.). Al terminar de verificar, borra cualquier script
temporal .py que hayas creado para esto (solo tenes permiso de correr
comandos que empiecen con "python", asi que borralo con python mismo,
por ejemplo: python -c "import os; os.remove('script_temporal.py')").
No dejes archivos .py sueltos en la carpeta del notebook. Compara el
resultado real de la ejecucion, no lo
que te "parece" que deberia dar, contra lo que el enunciado pide.

# Fase 3: edicion final compatible con Jupyter
Una vez validada la solucion, usa la herramienta NotebookEdit para
escribirla en la celda correspondiente del notebook. Ese codigo lo va
a ejecutar despues el estudiante ahi mismo, como celda de Jupyter (no
como script de consola independiente), asi que tiene que ser 100%
compatible con eso: prohibido incluir "if __name__ == '__main__':",
comandos magicos ("%" o "!"), "sys.argv", o llamadas interactivas como
input() que esperen la terminal.

Antes de elegir como resolverlo, revisa si el enunciado exige una
tecnologia, estructura de datos o tecnica puntual (por ejemplo:
"usa listas", "resuelvelo con matrices/listas anidadas",
"implementa con diccionarios", "usa recursividad", "usa una libreria
especifica como numpy o pandas", "no uses funciones built-in como
sorted()/sum()/max()", "hazlo con comprension de listas", etc.). Si
existe una exigencia asi, es una restriccion dura: la solucion tiene
que cumplirla si o si, aunque exista una forma mas corta que la
ignore. Dentro de esa restriccion, elegi la mejor solucion posible
(la mas clara y correcta), no cualquier cosa que la cumpla a medias.

Si el enunciado NO exige nada puntual en ese sentido, preferi siempre
la solucion mas directa y simple que resuelva correctamente lo que
pide, no la mas larga ni la mas sofisticada: si hay una forma corta y
una forma mas elaborada que logran lo mismo, elegi la corta. No
agregues funciones auxiliares, clases, abstracciones ni validaciones
extra que el enunciado no pidio: la mejor solucion es la que resuelve
el problema con la menor cantidad de codigo razonable, facil de leer
para un estudiante.

Al final de la celda de cada ejercicio, agrega 1 o 2 lineas de codigo
real (no un comentario de texto) que invoquen la solucion con un caso
de ejemplo concreto y muestren el resultado con print(), siguiendo el
contexto del problema (si devuelve dos listas, print(listaint,
listastr); si es un valor formateado, imprimi ese valor formateado;
etc.), para que al correr la celda (Shift+Enter) el estudiante vea de
inmediato el resultado real en la salida. Esto aplica siempre, haya
hecho falta corregir la celda o ya estuviera bien. No agregues
comentarios que identifiquen que el codigo fue revisado o corregido
por una IA (nada de "# Revisado por IA", "# Corregido por IA", ni
similares): la unica evidencia debe ser el print() ejecutable.

Por defecto NO agregues ningun comentario dentro del codigo (ni
explicando la solucion, ni el bug que corregiste, ni nada por el
estilo): enfocate unicamente en que el codigo resuelva lo que pide el
ejercicio, con la linea de print() al final como unica adicion visible
(mostrando las variables relevantes con el resultado de la solucion).
La UNICA excepcion es si el enunciado de ESE ejercicio puntual pide
explicitamente comentar o documentar el codigo (por ejemplo "comenta
tu codigo", "documenta la funcion"): en ese caso si agregas los
comentarios que pide, breves y solo en lo que no sea obvio. Se
objetivo con lo que cada enunciado pide especificamente, no apliques
una regla pareja a todos los ejercicios sin fijarte que pide cada uno.

Solo si el enunciado de un ejercicio pide EXPLICITAMENTE una
explicacion o justificacion en texto (por ejemplo "explica el
codigo", "justifica la solucion", "argumenta tu respuesta"), ademas de
resolverlo en codigo revisa con Read si existe este archivo:
C:\Users\Lucas Tamara\Desktop\M IA\estilo\estilo.txt
Si existe, redacta esa explicacion en la celda markdown
correspondiente siguiendo el estilo que describe ese archivo (tono,
estructura, conectores, espanol latinoamericano). Si el ejercicio NO
pide una explicacion en texto, no hace falta leer ni aplicar este
archivo: segui enfocado puramente en resolver el codigo con su
print(), sin agregar explicaciones que nadie pidio. No borres celdas
existentes, no modifiques celdas que no correspondan a un ejercicio
(imports generales, celdas de configuracion, etc.), y no agregues
celdas de resumen ni de cierre ni texto introductorio en ninguna
celda. Fuera de la excepcion explicada en la Fase 1 (crear la celda
de codigo faltante cuando un enunciado no tiene ninguna), no crees
celdas nuevas.

# Fase 4: verificacion final ejecutando el notebook completo
El estudiante va a abrir este notebook en Jupyter y usar "Run All"
(ejecutar todas las celdas de punta a punta, en orden, en un unico
kernel). Que cada ejercicio funcione aislado en un script separado (Fase
2) no garantiza eso: puede haber dependencias entre celdas, variables
compartidas, o algo que solo se rompe en ese orden real de ejecucion.

Por eso, despues de terminar de revisar/corregir TODAS las celdas del
notebook con NotebookEdit, hace esta verificacion final una sola vez
(no por cada ejercicio individual): ejecuta el notebook COMPLETO con
Jupyter de verdad usando Bash, con:
python -m nbconvert --to notebook --execute --inplace "<ruta del notebook>"
Esto corre todas las celdas en orden real, tal como haria "Run All", y
graba los resultados de ejecucion en el propio notebook.

Si falla (una celda tira una excepcion al ejecutarse en ese orden),
leele el error, identifica en cual celda/ejercicio esta el problema
real, corregilo con NotebookEdit, y volve a correr el mismo comando
nbconvert. Repeti esto hasta que el notebook entero se ejecute sin
errores de punta a punta. No des por terminado el notebook hasta que
esta verificacion final pase limpia.

# Fase 5: resumen para la app (fuera del notebook, en tu respuesta de texto)
Ademas de todo lo anterior, cuando termines de resolver y verificar el
notebook completo, agrega al FINAL de tu respuesta de texto (esto NO va
en ninguna celda del notebook, ni es una celda de resumen: es una
respuesta de texto aparte, para que una app externa la lea) un bloque
por cada ejercicio que resolviste, con EXACTAMENTE este formato (sin
comillas invertidas ni bloques markdown, sin texto antes ni despues de
cada bloque):
@@Q<numero>@@
<codigo Python final que quedo en la celda de ese ejercicio, tal cual,
incluyendo el print() de ejemplo>
@@FIN@@

Usa como <numero> el mismo numero/identificador real del ejercicio tal
como aparece en el enunciado (incluidos los puntos si el enunciado usa
sub-numeracion como "1.1", "1.2", "1.3"; si el notebook no numera los
ejercicios, numeralos vos mismo en el orden en que aparecen, empezando
en 1). Un bloque por ejercicio, nunca combines el codigo de varios
ejercicios en un solo bloque. No incluyas comentarios que repitan el
enunciado ni sentencias "import" dentro del bloque (asumi que ya estan
en el notebook): solo el codigo de la solucion. No escribas ninguna
otra explicacion en texto libre fuera de esos bloques."""


PROMPT_TEMPLATE_RJ3C = r"""Eres un agente especialista en Python, refactorizacion y verificacion
cientifica de codigo. Tu objetivo final es resolver ejercicios del
notebook REAL ubicado en esta ruta (vas a leerlo y escribirle con Read/
NotebookEdit mas abajo):

{notebook_path}

A diferencia del boton "RJ3" de esta misma app (que identifica que
ejercicios resolver leyendo ese notebook directamente), aca la fuente de
que ejercicio(s) atacar en esta pasada son estas capturas de pantalla
del mismo notebook (el usuario fue scrolleando; puede haber contenido
repetido entre imagenes consecutivas por el solapamiento):

{file_list}

RJ3 y este metodo (RJ3C) son dos formas INDEPENDIENTES/redundantes que
el usuario usa para resolver el MISMO notebook, por si una le falla a la
otra (por ejemplo si Read sobre el archivo no capta bien algo que si se
ve claro en pantalla, o al reves). Por eso el resultado final de este
metodo tiene que quedar escrito y verificado en el MISMO archivo real de
arriba, con el mismo rigor que RJ3 -- nunca en un archivo aparte.
{feedback_note}

Contexto academico: son ejercicios de practica de un curso, sin nota ni
evaluacion formal. Procede a resolverlos con rigor tecnico.

IMPORTANTE - contexto de ejecucion: esta llamada corre de forma
automatica y SIN SUPERVISION humana en tiempo real (es una unica
ejecucion de "claude --print"; nadie va a leer ni responder ninguna
pregunta que hagas en tu respuesta). Por eso:
- NUNCA hagas una pregunta de seguimiento ni pidas confirmacion antes de
  proceder: no hay nadie que pueda contestarte.
- Si con las imagenes que tenes podes identificar y resolver ALGUN
  ejercicio (aunque falten otras paginas), resolvelo igual.
- Si genuinamente NINGUNA imagen tiene contenido nuevo o resoluble (por
  ejemplo, todas muestran la misma pantalla repetida sin avanzar),
  decilo en UNA sola frase breve, sin generar ningun bloque para eso, y
  sin hacer ninguna pregunta de seguimiento.
{extra_note}

# Fase 1: identificar que ejercicio(s) atacar (desde las imagenes)
Revisa TODAS las imagenes (en el orden dado) y arma un inventario mental
de los numeros/identificadores de ejercicio distintos que aparecen (el
numero real mostrado en pantalla, incluidos los puntos si hay
sub-numeracion como "1.1", "1.2", "1.3"), descartando repeticiones por
solapamiento entre imagenes consecutivas. Si un ejercicio aparece
cortado en una imagen y completo (o con mas contexto) en la siguiente,
usa la version mas completa.

Para CADA ejercicio del inventario, ANTES de tocar nada: transcribi para
vos mismo (paso interno de verificacion, nunca para el bloque final del
final de tu respuesta) el enunciado EXACTO tal como aparece en la
imagen -- nombres de columnas/variables, condiciones, operaciones
pedidas, valores, unidades, todo literal, sin parafrasear ni completar
de memoria lo que "probablemente" dice. Esto es para anclarte al
contenido REAL de la captura (alta fidelidad) y no resolver un problema
levemente distinto al que realmente se pide por una lectura apurada.

# Fase 2: cruzar con el notebook real
Lee con la herramienta Read el notebook real ({notebook_path}) para
ubicar, por numeracion/enunciado, la celda de codigo que corresponde a
cada ejercicio de tu inventario. Para cada uno:
- Si esa celda YA tiene una solucion correcta y completa para lo que
  pide el enunciado transcripto (verificalo de verdad ejecutandola, no
  lo asumas por "tener contenido"), no la toques ni la reescribas: pasa
  al siguiente ejercicio de tu inventario.
- Si la celda esta vacia, incompleta, con un placeholder, o resuelve
  algo distinto a lo que pide el enunciado transcripto, seguí con la
  Fase 3 para ESE ejercicio.
- Si el ejercicio no tiene ninguna celda de codigo correspondiente en el
  notebook (no dejo espacio), no te frenes: resolvelo igual en la Fase 3
  y crea la celda con NotebookEdit (edit_mode="insert") inmediatamente
  despues de la celda del enunciado.

# Fase 3: resolver y verificar en aislado
Para cada ejercicio que si haga falta resolver (nuevo o incorrecto):
1. Con la transcripcion de la Fase 1 como base, entende con precision
   que pide el enunciado: que recibe, calcula, transforma o devuelve el
   codigo. No apliques una receta generica.
2. Escribe la solucion completa en codigo Python real y correcto,
   respetando cualquier restriccion que el enunciado exija (estructura
   de datos, tecnica, libreria especifica, prohibicion de ciertas
   funciones built-in, etc.). Si no exige nada puntual, preferi siempre
   la solucion mas simple y directa, sin funciones auxiliares ni
   abstracciones de mas.
3. Verificala ejecutandola de verdad con la herramienta Bash (python) en
   un script temporal -- nunca la traces mentalmente: proba casos
   estandar (las entradas normales del enunciado) y casos de borde
   razonables para ese ejercicio puntual. Agrega ahi los "import" que
   necesites para esa verificacion aislada. Al terminar, borra el script
   temporal con python mismo (el Bash disponible esta restringido a
   comandos que empiecen con "python": por ejemplo
   python -c "import os; os.remove('script_temporal.py')").

# Fase 4: escribir en el notebook real
Con la solucion ya verificada en aislado, escribila en la celda
correspondiente del notebook real con la herramienta NotebookEdit (nunca
en un archivo aparte). Tiene que ser 100% compatible con Jupyter:
prohibido "if __name__ == '__main__':", comandos magicos ("%"/"!"),
sys.argv, o input(). Agrega al final 1 o 2 lineas que invoquen la
solucion con un caso de ejemplo y muestren el resultado con print(), para
que se vea de inmediato que funciona al correr la celda. Por defecto NO
agregues ningun comentario (ni explicando la solucion ni nada por el
estilo), salvo que el enunciado de ESE ejercicio puntual pida
explicitamente comentar/documentar/explicar el codigo -- en ese caso, si
existe C:\Users\Lucas Tamara\Desktop\M IA\estilo\estilo.txt, leelo con
Read y segui ese estilo para la explicacion. No borres celdas
existentes ni toques celdas que no correspondan a un ejercicio de esta
pasada.

# Fase 5: verificacion final del notebook completo
Una vez que terminaste de escribir TODOS los ejercicios de esta pasada
(no por cada uno individualmente), ejecuta el notebook COMPLETO de
verdad con Jupyter usando Bash:
python -m nbconvert --to notebook --execute --inplace "{notebook_path}"
Esto corre TODAS las celdas del notebook en orden real -- las que
acabas de escribir y las que ya estaban de antes (resueltas por RJ3 o
por una pasada anterior de este mismo metodo) -- tal como haria
"Run All". Si falla, identifica en que celda esta el problema real,
corregila con NotebookEdit, y volve a correr el mismo comando nbconvert.
Repeti hasta que el notebook entero se ejecute sin errores de punta a
punta. No des nada por terminado hasta que esta verificacion final pase
limpia.

# Fase 6: resumen para la app (fuera del notebook, en tu respuesta de texto)
Al final de tu respuesta de texto (esto NO va en ninguna celda del
notebook: es una respuesta de texto aparte, para que una app externa la
lea), agrega un bloque por cada ejercicio que resolviste o confirmaste
en esta pasada, con EXACTAMENTE este formato (sin comillas invertidas ni
bloques markdown, sin texto antes ni despues de cada bloque):
@@Q<numero>@@
<codigo Python final que quedo en la celda de ese ejercicio, tal cual,
incluyendo el print() de ejemplo>
@@FIN@@

Usa como <numero> el mismo identificador real del ejercicio (incluidos
los puntos si el enunciado usa sub-numeracion como "1.1", "1.2"). Un
bloque por ejercicio, nunca combines el codigo de varios ejercicios en
un solo bloque. No incluyas comentarios que repitan el enunciado ni
sentencias "import" dentro del bloque (asumi que ya estan en el
notebook): solo el codigo de la solucion. No escribas ninguna otra
explicacion en texto libre fuera de esos bloques (nada de "a
continuacion resuelvo...", "espero que te sirva", etc.). Empieza
directamente con el primer bloque y termina en el ultimo."""


LOG_MAX_BYTES = 5 * 1024 * 1024  # al superarlo, app.log pasa a app.log.1 (se guarda 1 copia)


def log(message: str) -> None:
    """Escribe en app.log. Si se llama dentro de un `except` con un mensaje
    que empieza con "ERROR", agrega el traceback completo: sin eso el log
    solo decia p.ej. "string too long (137, maximum length 128)" sin indicar
    que linea ni que cadena lo provoco. Nunca lanza excepciones (se usa
    dentro de los propios manejadores de error)."""
    try:
        if message.startswith("ERROR") and sys.exc_info()[0] is not None:
            message += "\n" + traceback.format_exc().rstrip()
        message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        if os.path.isfile(LOG_FILE) and os.path.getsize(LOG_FILE) > LOG_MAX_BYTES:
            os.replace(LOG_FILE, LOG_FILE + ".1")
        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
            f.write(message + "\n")
    except Exception:
        pass


_curso_context_cache = None


def _load_curso_context() -> str:
    """Lee CURSO_CONTEXT_PATH una sola vez (se cachea en memoria) y arma el
    bloque de contexto que se antepone a cada prompt de preguntas. Si el
    archivo no existe todavia (por ejemplo una instalacion vieja sin el
    .md), devuelve "" sin romper el flujo: Manual N1 y CAR tienen que seguir
    funcionando igual, solo que sin ese contexto extra."""
    global _curso_context_cache
    if _curso_context_cache is not None:
        return _curso_context_cache
    try:
        with open(CURSO_CONTEXT_PATH, "r", encoding="utf-8") as f:
            contenido = f.read()
    except OSError as exc:
        log(f"No se pudo leer el contexto del curso ({CURSO_CONTEXT_PATH}): {exc}")
        _curso_context_cache = ""
        return _curso_context_cache
    _curso_context_cache = (
        "CONTEXTO DEL CURSO (resumen verificado del material de clase de Algoritmos de "
        "Optimizacion; usalo como referencia de terminologia, definiciones y enfoque tal "
        "como se ensenaron, pero segui resolviendo cada pregunta con rigor propio: si algo "
        "puntual de una pregunta no coincide con este resumen, prioriza resolver "
        "correctamente el problema planteado por sobre repetir literalmente el resumen):\n\n"
        + contenido
        + "\n\n---\n\n"
    )
    log(f"Contexto del curso cargado desde {CURSO_CONTEXT_PATH} ({len(contenido)} caracteres)")
    return _curso_context_cache


_ra_context_cache = None


def _load_ra_context() -> str:
    """Arma (una sola vez, cacheado) el bloque de base de conocimiento de
    Razonamiento Aproximado que se antepone al prompt de CAR
    (PROMPT_TEMPLATE_REPASAR). El texto va EMBEBIDO en el modulo
    base_conocimiento_ra.py (PyInstaller lo empaqueta dentro del .exe: no
    depende de ningun archivo externo). Si el import fallara, devuelve ""
    sin romper el flujo. Solo la usa la plantilla de CAR: el resto de las
    plantillas no tienen el placeholder {ra_context} y str.format ignora
    el kwarg."""
    global _ra_context_cache
    if _ra_context_cache is not None:
        return _ra_context_cache
    try:
        from base_conocimiento_ra import BASE_CONOCIMIENTO_RA as contenido
    except Exception as exc:
        log(f"No se pudo cargar la base de conocimiento RA embebida: {exc}")
        _ra_context_cache = ""
        return _ra_context_cache
    contenido = contenido.strip()
    _ra_context_cache = (
        "BASE DE CONOCIMIENTO - RAZONAMIENTO APROXIMADO (resumen teorico completo del curso: "
        "modelos de incertidumbre, logica borrosa, CLIPS/FuzzyCLIPS y material complementario). "
        "Leela ANTES de responder: si una pregunta es de ese tema, usa esta base como fuente "
        "principal de definiciones, formulas, terminologia y enfoque tal como se ensenaron, "
        "pero segui resolviendo cada pregunta con rigor propio: si algo puntual de la pregunta "
        "no coincide con la base (o la base marca un [OJO] de errata), prioriza resolver "
        "correctamente el problema planteado. Si la pregunta es de otro tema, ignorala:\n\n"
        + contenido
        + "\n\n---\n\n"
    )
    log(f"Base de conocimiento RA embebida cargada ({len(contenido)} caracteres)")
    return _ra_context_cache


def find_question_files() -> list:
    if not os.path.isdir(PREGUNTAS_DIR):
        os.makedirs(PREGUNTAS_DIR, exist_ok=True)
        return []
    files = []
    for path in sorted(glob.glob(os.path.join(PREGUNTAS_DIR, "*"))):
        if os.path.isfile(path) and path.lower().endswith(VALID_EXTENSIONS):
            files.append(path)
    return files


def find_manual_files() -> list:
    """Archivos .txt que el usuario coloco a mano en MANUAL_DIR (boton
    "Manual N1"), todavia sin analizar. A diferencia de PREGUNTAS_DIR, esta
    carpeta no se crea automaticamente si no existe todavia, ya que
    MANUAL_DIR es una ruta fija fuera de BASE_DIR (igual que PRACTICA3_DIR/
    ESTILO_DIR): el usuario la gestiona el mismo."""
    if not os.path.isdir(MANUAL_DIR):
        return []
    files = []
    for path in sorted(glob.glob(os.path.join(MANUAL_DIR, "*"))):
        if os.path.isfile(path) and path.lower().endswith(MANUAL_VALID_EXTENSIONS):
            files.append(path)
    return files


def move_manual_to_procesado(files: list) -> list:
    """Analogo a move_to_procesado pero para MANUAL_DIR/procesado: mueve
    cada archivo .txt ya analizado para que una pulsacion posterior de
    "Manual N1" nunca vuelva a mandarlo (asi la sesion acumulativa de texto
    no depende de que Claude recuerde que preguntas ya respondio, a
    diferencia de CAR, donde la misma pantalla se puede volver a
    capturar)."""
    os.makedirs(MANUAL_PROCESADO_DIR, exist_ok=True)
    destinos = []
    for path in files:
        destino = os.path.join(MANUAL_PROCESADO_DIR, os.path.basename(path))
        if os.path.exists(destino):
            nombre, ext = os.path.splitext(os.path.basename(path))
            destino = os.path.join(MANUAL_PROCESADO_DIR, f"{nombre}_{time.strftime('%Y%m%d_%H%M%S')}{ext}")
        try:
            shutil.move(path, destino)
            destinos.append(destino)
        except OSError as exc:
            log(f"No se pudo mover {path} a procesado: {exc}")
            destinos.append(path)
    return destinos


def find_jupyter_files() -> list:
    if not os.path.isdir(PRACTICA3_DIR):
        log(f"PRACTICA3_DIR no existe: {PRACTICA3_DIR}")
        return []
    files = []
    for path in sorted(glob.glob(os.path.join(PRACTICA3_DIR, "*" + JUPYTER_EXTENSION))):
        if os.path.isfile(path):
            files.append(path)
    return files


def _backup_notebook(notebook_path: str) -> str:
    """Copia `notebook_path` a NOTEBOOK_BACKUPS_DIR con fecha/hora ANTES de
    que RJ3/RJ3C lo toquen con NotebookEdit/nbconvert: red de seguridad
    para poder recuperar la version de antes si una edicion automatica sale
    mal. Se llama una vez por notebook en cada pasada de RJ3 o RJ3C (no
    borra backups viejos: son livianos, unos KB cada uno). Si falla
    (permisos, disco lleno), se loguea pero NO frena la resolucion -- no
    tener un backup puntual es preferible a que el usuario no pueda
    resolver el notebook por eso. Devuelve la ruta del backup creado (o ""
    si fallo), para que quien la llama pueda restaurar desde ahi si hace
    falta (ver uso en resolve_jupyter_task)."""
    try:
        os.makedirs(NOTEBOOK_BACKUPS_DIR, exist_ok=True)
        nombre, ext = os.path.splitext(os.path.basename(notebook_path))
        destino = os.path.join(NOTEBOOK_BACKUPS_DIR, f"{nombre}_{time.strftime('%Y%m%d_%H%M%S')}{ext}")
        shutil.copy2(notebook_path, destino)
        log(f"Backup del notebook guardado en {destino}")
        return destino
    except OSError as exc:
        log(f"ERROR: no se pudo guardar backup de {notebook_path} antes de editarlo: {exc}")
        return ""


def _verificar_notebook_independiente(notebook_path: str) -> str:
    """Corre nbconvert de forma INDEPENDIENTE de Claude (la app misma, con
    su propio subprocess.run) para confirmar que el notebook ejecuta sin
    errores de punta a punta -- control cruzado en vez de confiar solo en
    que Claude reporte haberlo verificado el mismo dentro de su propia
    llamada (pedido explicito del usuario). Devuelve "" si el notebook
    corrio limpio, o el texto del error real (para mandarselo de vuelta a
    Claude en el proximo intento) si fallo o se colgo."""
    try:
        resultado = subprocess.run(
            ["python", "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace", notebook_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=NBCONVERT_VERIFICATION_TIMEOUT_SECONDS,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
    except subprocess.TimeoutExpired:
        return f"nbconvert no termino en {NBCONVERT_VERIFICATION_TIMEOUT_SECONDS} segundos (se corto)."
    if resultado.returncode == 0:
        return ""
    detalle = (resultado.stderr or resultado.stdout or "codigo de salida " + str(resultado.returncode)).strip()
    return detalle[-2000:]


# Tolerante a las variantes reales con que Claude escribe la tabla resumen:
# "2 | b", "| 2 | b |" (tabla Markdown), "**2** | b", "2. | b", "P2 | b",
# "Pregunta 2 | b", con backticks, y respuestas largas (antes el limite de 40
# caracteres y el formato estricto descartaban la fila EN SILENCIO y la
# pregunta aparecia como "faltan preguntas" aunque estuviera en t.txt).
SUMMARY_LINE_RE = re.compile(
    r"^(?:(?:pregunta|preg\.?|p)\s*)?(\d{1,3})\s*[.)]?\s*\|\s*(.{1,200}?)$",
    re.IGNORECASE,
)


def _limpiar_linea_resumen(linea: str) -> str:
    linea = linea.strip().replace("**", "").replace("`", "")
    linea = linea.strip("| \t")
    return linea.strip()


def parse_summary(respuesta: str) -> list:
    """Extrae pares (numero, respuesta) de la tabla resumen final ('N |
    respuesta') que se le pide a Claude en el prompt, para mostrarlos en
    el hover con ctrl+alt+9 sin tener que abrir t.txt.

    Se queda con el ULTIMO bloque de lineas consecutivas que parecen filas
    del resumen (la tabla va al final): asi una tabla de verdad o de
    pertenencia dentro de una explicacion ("| 1 | 0,5 | 0,3 |") no se
    confunde con respuestas. Las lineas en blanco, los encabezados
    ("N | Respuesta") y los separadores Markdown ("|---|---|") no cortan
    el bloque."""
    bloques = []
    actual = []
    for linea in respuesta.splitlines():
        limpia = _limpiar_linea_resumen(linea)
        if not limpia or re.fullmatch(r"[-:| ]+", limpia) or re.match(r"(?i)^(n|n°|nro|#|pregunta)\s*\|", limpia):
            continue
        m = SUMMARY_LINE_RE.match(limpia)
        if m:
            resp = m.group(2).strip().strip("|").strip()
            if resp and "|" not in resp:
                actual.append((str(int(m.group(1))), resp))
                continue
        if actual:
            bloques.append(actual)
            actual = []
    if actual:
        bloques.append(actual)
    return bloques[-1] if bloques else []


RJ3C_SUMMARY_BLOCK_RE = re.compile(r"@@Q([0-9]+(?:\.[0-9]+)*)@@\s*\n(.*?)\n@@FIN@@", re.DOTALL)


def parse_rj3c_summary(respuesta: str) -> list:
    """Extrae pares (numero, codigo) de los bloques delimitados '@@Qn@@ ...
    @@FIN@@' que pide PROMPT_TEMPLATE_RJ3C, uno por cada ejercicio de
    codigo resuelto a partir de las capturas de pantalla. A diferencia de
    parse_summary (respuesta corta tipo 'letra'/numero), aca la 'respuesta'
    es el codigo Python completo de la solucion, potencialmente multilinea.
    El numero acepta sub-numeracion con puntos (ej. "1.1", "1.2", "1.3"),
    porque los notebooks de practica suelen dividir un ejercicio en varias
    partes numeradas asi en vez de un unico entero por ejercicio."""
    pares = []
    for m in RJ3C_SUMMARY_BLOCK_RE.finditer(respuesta):
        pares.append((m.group(1), m.group(2).strip()))
    return pares


def _numero_ejercicio_sort_key(numero: str) -> tuple:
    """Convierte un identificador de ejercicio como '3' o '1.2' en una
    tupla de enteros comparable ((3,) o (1, 2)) para poder ordenarlos
    numericamente aunque tengan sub-numeracion con puntos (RJ3C), igual
    que los identificadores simples de CAR/Manual N1 (numero entero
    unico). Nunca lanza excepcion: una parte no numerica cae al final."""
    partes = []
    for parte in str(numero).split("."):
        try:
            partes.append(int(parte))
        except ValueError:
            partes.append(float("inf"))
    return tuple(partes)


def chunk_files(files: list, batch_size: int = BATCH_SIZE, overlap: int = 0) -> list:
    """Divide `files` en lotes de a lo sumo `batch_size`, para no mandarle a
    Claude Code de una sola vez mas imagenes de las que su contexto puede
    manejar (eso es lo que causaba "claude --print devolvio error" con 39+
    imagenes). `overlap` repite las ultimas N imagenes de un lote como
    primeras del siguiente, util en REPASAR donde las capturas de scroll ya
    se solapan entre si y una pregunta podria quedar cortada en el borde."""
    if len(files) <= batch_size:
        return [files]
    batches = []
    start = 0
    n = len(files)
    while start < n:
        end = min(start + batch_size, n)
        batches.append(files[start:end])
        if end >= n:
            break
        start = end - overlap
    return batches


def merge_summaries(pares_por_lote: list) -> list:
    """Une los pares (numero, respuesta) de varios lotes en una sola lista,
    ordenada por numero de pregunta/ejercicio, sin duplicar numeros
    repetidos (pueden repetirse por el solapamiento entre lotes; se
    conserva la primera aparicion -- asi RJ3C nunca muestra dos veces el
    mismo ejercicio aunque su codigo haya aparecido en imagenes de mas de
    un lote). Usa _numero_ejercicio_sort_key para poder ordenar tanto
    numeros simples (CAR/Manual N1: "3") como sub-numerados con puntos
    (RJ3C: "1.2")."""
    vistos = {}
    for pares in pares_por_lote:
        for numero, resp in pares:
            vistos.setdefault(numero, resp)
    return sorted(vistos.items(), key=lambda par: _numero_ejercicio_sort_key(par[0]))


def move_to_procesado(files: list) -> list:
    """Mueve los archivos ya analizados a PREGUNTAS/procesado para que un
    Manual N1 posterior (por accidente) no los vuelva a analizar y gaste
    cuota de nuevo. Devuelve la lista de rutas nuevas (mismo orden que
    `files`), para poder actualizar el prompt guardado para N2."""
    os.makedirs(PROCESADO_DIR, exist_ok=True)
    destinos = []
    for path in files:
        destino = os.path.join(PROCESADO_DIR, os.path.basename(path))
        if os.path.exists(destino):
            nombre, ext = os.path.splitext(os.path.basename(path))
            destino = os.path.join(PROCESADO_DIR, f"{nombre}_{time.strftime('%Y%m%d_%H%M%S')}{ext}")
        try:
            shutil.move(path, destino)
            destinos.append(destino)
        except OSError as exc:
            log(f"No se pudo mover {path} a procesado: {exc}")
            destinos.append(path)
    return destinos


def _build_status_icon(base_image: Image.Image, color: tuple) -> Image.Image:
    """Copia el logo con un pequeño distintivo circular de color en la
    esquina inferior derecha, para mostrar el estado sin notificaciones."""
    icon_img = base_image.convert("RGBA").copy()
    w, h = icon_img.size
    badge_d = max(1, int(min(w, h) * 0.42))
    badge = Image.new("RGBA", (badge_d, badge_d), (0, 0, 0, 0))
    ImageDraw.Draw(badge).ellipse((0, 0, badge_d - 1, badge_d - 1), fill=color)
    icon_img.paste(badge, (w - badge_d, h - badge_d), badge)
    return icon_img


def load_status_icons(base_image: Image.Image) -> None:
    ICONS["idle"] = base_image
    ICONS["busy"] = _build_status_icon(base_image, COLOR_BUSY)
    ICONS["ok"] = _build_status_icon(base_image, COLOR_OK)
    ICONS["warning"] = _build_status_icon(base_image, COLOR_WARNING)
    ICONS["error"] = _build_status_icon(base_image, COLOR_ERROR)
    ICONS["info"] = _build_status_icon(base_image, COLOR_INFO)


def on_review_next(icon: Any, item=None) -> None:
    """Hotkey ctrl+alt+9: cada pulsacion avanza y muestra una pregunta/
    respuesta del ultimo analisis en el tooltip del icono (Q1, luego Q2,
    etc.), hasta completarlas todas. Se ve al pasar el mouse por encima
    del icono de la bandeja (no es un aviso emergente)."""
    global _review_index
    if not _last_summary:
        icon.title = "Sin resultados aun"
        log("Ctrl+Alt+9: sin resultados todavia, no hay nada para mostrar.")
        return
    if _busy.is_set():
        log("Ctrl+Alt+9: hay un analisis en curso: el tooltip puede sobreescribirse enseguida con el estado de esa tarea.")
    if _review_index >= len(_last_summary):
        icon.title = "Repaso completo"
        _review_index = 0
        return
    numero, resp = _last_summary[_review_index]
    icon.title = f"em023.dll.nup {numero}: {resp}"
    log(f"Ctrl+Alt+9: mostrando pregunta {numero} ({_review_index + 1}/{len(_last_summary)}) en el tooltip.")
    _review_index += 1


def _envolver_linea_larga(linea: str, max_chars: int) -> list:
    """Envuelve una linea de codigo mas larga que `max_chars` en varias
    sub-lineas partiendo en puntos naturales (espacios -- que en Python
    caen justo despues de comas, operadores, parentesis con argumentos,
    etc., via textwrap.wrap) en vez de cortarla a la mitad de una
    expresion con "..." y perder el resto (pedido explicito del usuario:
    "asegurar que se muestren bien las respuestas"). Las sub-lineas
    conservan la indentacion original de la linea, para que se sigan
    viendo como parte de la misma sentencia. `break_long_words=True` es
    el respaldo para el caso raro de una sola "palabra" (ej. un string
    literal larguisimo sin espacios) mas larga que el ancho disponible."""
    indentacion = linea[: len(linea) - len(linea.lstrip(" "))]
    contenido = linea.strip()
    ancho_disponible = max(10, max_chars - len(indentacion))
    partes = textwrap.wrap(contenido, width=ancho_disponible, break_long_words=True, break_on_hyphens=False)
    if not partes:
        return [linea]
    return [indentacion + parte for parte in partes]


def _paginas_rj3c(codigo: str, numero: str) -> list:
    """Filtra el codigo de un ejercicio (mismo filtro de respaldo de
    siempre: sin comentarios/imports, ver PROMPT_TEMPLATE_RJ3C), envuelve
    (no trunca) las lineas mas largas que el presupuesto (ver
    _envolver_linea_larga) y reparte todo en "paginas" -- cada una entera
    dentro del presupuesto de caracteres del tooltip -- SIN perder nunca
    codigo: asi se puede ver la respuesta COMPLETA de un ejercicio, pagina
    por pagina, sin ningun "..." que se coma parte de una expresion.
    Conserva la indentacion tal cual la escribio Claude (solo se saca el
    trailing whitespace con rstrip, NO el leading con strip): asi un
    if/for con lineas anidadas se ve anidado en el tooltip, en vez de
    "aplanado" a un solo nivel (pedido explicito del usuario). El
    presupuesto reserva espacio fijo para un sufijo tipo " (12/34): " (2
    digitos de pagina, generoso) para no tener que recalcular la
    paginacion segun cuantas paginas termine habiendo."""
    lineas_utiles = []
    for linea in codigo.splitlines():
        contenido = linea.strip()
        if not contenido:
            continue
        if contenido.startswith("#") or contenido.startswith("import ") or contenido.startswith("from "):
            continue
        lineas_utiles.append(linea.rstrip())
    if not lineas_utiles:
        return ["(sin codigo visible)"]
    presupuesto = max(10, RJ3C_TOOLTIP_MAX_CHARS - len(f"Q{numero}") - len(" (99/99): "))

    lineas_expandidas = []
    for linea in lineas_utiles:
        if len(linea) > presupuesto:
            lineas_expandidas.extend(_envolver_linea_larga(linea, presupuesto))
        else:
            lineas_expandidas.append(linea)

    paginas = []
    actual = []
    largo = 0
    for linea in lineas_expandidas:
        extra = len(linea) + (1 if actual else 0)  # +1 por el "\n" previo
        if actual and largo + extra > presupuesto:
            paginas.append("\n".join(actual))
            actual, largo = [], 0
            extra = len(linea)
        actual.append(linea)
        largo += extra
    if actual:
        paginas.append("\n".join(actual))
    return paginas


def _mostrar_pagina_rj3c(icon: Any, ejercicio_idx: int, pagina_idx: int) -> None:
    """Actualiza icon.title con la pagina `pagina_idx` del ejercicio
    `ejercicio_idx` de _rj3c_summary (ambos con wrap-around via modulo) y
    deja _rj3c_hover_index/_rj3c_pagina_index apuntando ahi. Punto unico
    compartido por los TRES disparadores del hover de RJ3C (entrar el
    mouse al icono, Ctrl+Alt+N, Ctrl+Alt+B) via _avanzar_pagina_rj3c."""
    global _rj3c_hover_index, _rj3c_pagina_index
    ejercicio_idx = ejercicio_idx % len(_rj3c_summary)
    numero, codigo = _rj3c_summary[ejercicio_idx]
    paginas = _paginas_rj3c(codigo, numero)
    pagina_idx = pagina_idx % len(paginas)
    _rj3c_hover_index = ejercicio_idx
    _rj3c_pagina_index = pagina_idx
    sufijo = f" ({pagina_idx + 1}/{len(paginas)})" if len(paginas) > 1 else ""
    icon.title = f"Q{numero}{sufijo}: {paginas[pagina_idx]}"


def _avanzar_pagina_rj3c(icon: Any, direccion: int) -> None:
    """Avanza (direccion=+1) o retrocede (direccion=-1) UNA PAGINA dentro
    del ejercicio actual, para poder ver su respuesta completa sin
    truncarla: solo pasa al ejercicio siguiente/anterior cuando se
    agotan las paginas del actual (pedido explicito del usuario: "mostrar
    toda la respuesta de Q1 y luego pasar a Q2"). `_rj3c_hover_index ==
    -1` es el estado inicial ("nada mostrado todavia"): +1 arranca en el
    primer ejercicio/primera pagina, -1 arranca en el ultimo
    ejercicio/ultima pagina."""
    if not _rj3c_summary:
        icon.title = "RJ3C: sin resultados aun"
        return
    n = len(_rj3c_summary)
    if _rj3c_hover_index == -1:
        ejercicio_idx = 0 if direccion > 0 else (n - 1)
    else:
        numero, codigo = _rj3c_summary[_rj3c_hover_index]
        paginas_actual = _paginas_rj3c(codigo, numero)
        nueva_pagina = _rj3c_pagina_index + direccion
        if 0 <= nueva_pagina < len(paginas_actual):
            _mostrar_pagina_rj3c(icon, _rj3c_hover_index, nueva_pagina)
            return
        ejercicio_idx = (_rj3c_hover_index + direccion) % n
    if direccion > 0:
        _mostrar_pagina_rj3c(icon, ejercicio_idx, 0)
    else:
        numero, codigo = _rj3c_summary[ejercicio_idx]
        ultima_pagina = len(_paginas_rj3c(codigo, numero)) - 1
        _mostrar_pagina_rj3c(icon, ejercicio_idx, ultima_pagina)


def on_rj3c_siguiente(icon: Any, item=None) -> None:
    """Hotkey Ctrl+Alt+N: avanza manualmente una pagina en el hover de
    RJ3C, sin depender de mover el mouse (mas preciso que entrar/salir del
    icono con el puntero, que puede fallar si el mouse se mueve rapido)."""
    if not _rj3c_summary:
        icon.title = "RJ3C: sin resultados aun"
        log("Ctrl+Alt+N: sin resultados de RJ3C todavia, no hay nada para mostrar.")
        return
    _avanzar_pagina_rj3c(icon, +1)
    log(
        f"Ctrl+Alt+N: mostrando ejercicio {_rj3c_hover_index + 1}/{len(_rj3c_summary)} "
        f"(pagina {_rj3c_pagina_index + 1}) de RJ3C en el tooltip."
    )


def on_rj3c_atras(icon: Any, item=None) -> None:
    """Hotkey Ctrl+Alt+B: retrocede manualmente una pagina en el hover de
    RJ3C."""
    if not _rj3c_summary:
        icon.title = "RJ3C: sin resultados aun"
        log("Ctrl+Alt+B: sin resultados de RJ3C todavia, no hay nada para mostrar.")
        return
    _avanzar_pagina_rj3c(icon, -1)
    log(
        f"Ctrl+Alt+B: mostrando ejercicio {_rj3c_hover_index + 1}/{len(_rj3c_summary)} "
        f"(pagina {_rj3c_pagina_index + 1}) de RJ3C en el tooltip."
    )


def _key_down(vk: int) -> bool:
    return bool(ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000)


class _GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8),
    ]


class _NOTIFYICONIDENTIFIER(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("hWnd", ctypes.c_void_p),
        ("uID", ctypes.c_uint),
        ("guidItem", _GUID),
    ]


def _cursor_pos() -> tuple:
    point = wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def _icon_screen_rect(hwnd):
    """Devuelve (left, top, right, bottom), el rectangulo en pantalla que
    ocupa el icono de la bandeja, usando Shell_NotifyIconGetRect (shell32,
    disponible desde Windows 7). pystray identifica su icono con uID=0: su
    intento de usar id(self) como uID (kwarg "hID" al construir
    NOTIFYICONDATAW) nunca llega a aplicarse porque el campo real del struct
    se llama "uID", no "hID", y ctypes ignora en silencio kwargs que no
    coinciden con ningun campo (verificado leyendo pystray._win32 y
    probando el comportamiento de ctypes.Structure directamente). Devuelve
    None si el icono todavia no tiene ventana creada (arranque) o si la
    consulta falla."""
    if not hwnd:
        return None
    identifier = _NOTIFYICONIDENTIFIER(cbSize=ctypes.sizeof(_NOTIFYICONIDENTIFIER), hWnd=hwnd, uID=0)
    rect = wintypes.RECT()
    hresult = ctypes.windll.shell32.Shell_NotifyIconGetRect(ctypes.byref(identifier), ctypes.byref(rect))
    if hresult != 0:
        return None
    return (rect.left, rect.top, rect.right, rect.bottom)


def _habilitar_menu_oscuro(hwnd) -> None:
    """Pedido explicito del usuario: su Windows ya esta en modo oscuro,
    pero el menu contextual nativo del icono de la bandeja (Manual N1/CAR/
    RJ3/RJ3C/Ver/Salir) seguia viendose claro. pystray dibuja ese menu con
    TrackPopupMenu (un menu Win32 clasico), y esos menus NO siguen el modo
    oscuro del sistema automaticamente: hay que avisarle a Windows
    explicitamente, con la misma tecnica que usa el Explorador de archivos
    para sus propios menus oscuros.

    Usa SetPreferredAppMode/FlushMenuThemes de uxtheme.dll -- funciones NO
    documentadas oficialmente por Microsoft (solo accesibles por numero de
    ordinal, sin firma publica en los headers de Windows), pero una tecnica
    estable y bien conocida desde Windows 10 1903 en adelante (la misma que
    usan Windows Terminal y otras apps). SetWindowTheme (esa si documentada)
    aplica el tema oscuro puntualmente a la ventana oculta que usa pystray
    para el menu. Al ser en parte no documentada, TODO esto va en
    try/except: si falla (Windows viejo, o Microsoft cambia los ordinales
    en el futuro), el menu simplemente se queda claro, sin romper nada mas
    de la app."""
    try:
        uxtheme = ctypes.WinDLL("uxtheme", use_last_error=True)
        set_preferred_app_mode = uxtheme[135]  # SetPreferredAppMode (sin firma publica)
        set_preferred_app_mode.argtypes = [ctypes.c_int]
        set_preferred_app_mode.restype = ctypes.c_int
        set_preferred_app_mode(1)  # 1 = AllowDark
        flush_menu_themes = uxtheme[136]  # FlushMenuThemes (sin firma publica)
        flush_menu_themes()
        if hwnd:
            uxtheme.SetWindowTheme.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR]
            uxtheme.SetWindowTheme.restype = ctypes.c_long
            uxtheme.SetWindowTheme(hwnd, "DarkMode_Explorer", None)
        log("Modo oscuro del menu de la bandeja habilitado (uxtheme, API no documentada de Windows).")
    except Exception as exc:
        log(f"No se pudo habilitar el modo oscuro del menu (se sigue viendo con el tema claro): {exc}")


def _hotkey_watcher(icon: Any) -> None:
    """Sondea el estado fisico de las teclas en vez de usar un hook global
    de teclado: dentro de una maquina virtual, el software de VM instala
    su propio hook para reenviar las teclas al huesped y puede "tragarse"
    el evento antes de que un hook de otra app (como el que usaba la
    libreria keyboard) llegue a verlo, aunque la tecla si se presiono en
    el host. GetAsyncKeyState lee el estado real de la tecla y no depende
    de esa cadena de hooks, asi que el atajo sigue funcionando aunque el
    foco este sobre la ventana de la VM.

    Los botones laterales del mouse (atras/adelante) necesitan DOS
    pulsaciones seguidas dentro de MOUSE_DOUBLE_PRESS_WINDOW_SECONDS para
    disparar el atajo: un solo clic de esos botones es tambien "atras" o
    "adelante" en cualquier navegador o el Explorador de Windows, asi que
    con un solo clic se confundiria con navegacion normal y dispararia
    REPASAR/revisar por accidente.

    Todo el cuerpo del loop esta protegido con try/except: si una sola
    iteracion lanza una excepcion inesperada, se loguea y se sigue
    sondeando, en vez de que el hilo completo muera en silencio y deje los
    atajos sin funcionar hasta reiniciar la app.

    Ademas, mientras el puntero del mouse permanece FISICAMENTE sobre el
    icono de la bandeja (Shell_NotifyIconGetRect + GetCursorPos, sin
    depender de ningun callback de hover de pystray porque no expone
    ninguno), en el modo "test" (_active_hover_mode) se recorre
    automaticamente una pregunta/respuesta cada HOVER_CYCLE_INTERVAL_SECONDS,
    en bucle, sin que haga falta presionar Ctrl+Alt+9. Usa su propio
    indice (hover_index), separado de _review_index (el de Ctrl+Alt+9),
    para que ambos mecanismos no se pisen entre si. Se pausa mientras hay
    un analisis en curso (_busy) para no competir por icon.title con los
    mensajes de estado de esa tarea. En el modo "rj3c" el mouse NO hace
    nada (pedido explicito del usuario): ver el bloque
    `if mouse_en_icono ... and _active_hover_mode != "rj3c"` mas abajo.

    Ctrl+Alt+N / Ctrl+Alt+B navegan manualmente por el hover DEDICADO de
    RJ3C, pagina por pagina (_rj3c_hover_index/_rj3c_pagina_index viven a
    nivel de modulo, no aca, ver on_rj3c_siguiente/on_rj3c_atras/
    _mostrar_pagina_rj3c).

    Ademas, la PRIMERA vez que icon._hwnd deja de ser None (recien al
    arrancar, pystray tarda un toque en crear esa ventana) se llama una
    unica vez a _habilitar_menu_oscuro para que el menu contextual del
    icono siga el modo oscuro de Windows del usuario."""
    r_was_down = False
    nine_was_down = False
    n_was_down = False
    b_was_down = False
    mouse_back_was_down = False
    mouse_fwd_was_down = False
    ultimo_click_atras = 0.0
    ultimo_click_adelante = 0.0
    mouse_estaba_en_icono = False
    hover_index = 0
    ultimo_avance_hover = 0.0
    menu_oscuro_aplicado = False

    while True:
        try:
            if not menu_oscuro_aplicado:
                hwnd_actual = getattr(icon, "_hwnd", None)
                if hwnd_actual:
                    _habilitar_menu_oscuro(hwnd_actual)
                    menu_oscuro_aplicado = True
            mods_down = _key_down(VK_CONTROL) and _key_down(VK_MENU)
            r_down = mods_down and _key_down(VK_R)
            nine_down = mods_down and _key_down(VK_9)
            n_down = mods_down and _key_down(VK_N)
            b_down = mods_down and _key_down(VK_B)
            mouse_back_down = _key_down(VK_XBUTTON1)
            mouse_fwd_down = _key_down(VK_XBUTTON2)
            ahora = time.monotonic()

            disparar_repasar = r_down and not r_was_down
            if mouse_back_down and not mouse_back_was_down:
                if ahora - ultimo_click_atras <= MOUSE_DOUBLE_PRESS_WINDOW_SECONDS:
                    disparar_repasar = True
                    ultimo_click_atras = 0.0
                else:
                    ultimo_click_atras = ahora

            disparar_revisar = nine_down and not nine_was_down
            if mouse_fwd_down and not mouse_fwd_was_down:
                if ahora - ultimo_click_adelante <= MOUSE_DOUBLE_PRESS_WINDOW_SECONDS:
                    disparar_revisar = True
                    ultimo_click_adelante = 0.0
                else:
                    ultimo_click_adelante = ahora

            disparar_rj3c_siguiente = n_down and not n_was_down
            disparar_rj3c_atras = b_down and not b_was_down

            if disparar_repasar:
                _start_task(icon, repasar_task)
            if disparar_revisar:
                on_review_next(icon)
            if disparar_rj3c_siguiente:
                on_rj3c_siguiente(icon)
            if disparar_rj3c_atras:
                on_rj3c_atras(icon)

            mouse_en_icono = False
            rect = _icon_screen_rect(getattr(icon, "_hwnd", None))
            if rect:
                cx, cy = _cursor_pos()
                left, top, right, bottom = rect
                mouse_en_icono = left <= cx <= right and top <= cy <= bottom

            recien_entro = mouse_en_icono and not mouse_estaba_en_icono
            if recien_entro:
                # Recien entro al icono: arranca el recorrido desde la
                # primera pregunta (modo "test" unicamente: el modo "rj3c"
                # ignora por completo el mouse, pedido explicito del
                # usuario -- ahi solo navegan Ctrl+Alt+N/Ctrl+Alt+B).
                hover_index = 0
                ultimo_avance_hover = 0.0

            if mouse_en_icono and not _busy.is_set() and _active_hover_mode != "rj3c":
                if not _last_summary:
                    icon.title = "Sin resultados aun"
                elif ahora - ultimo_avance_hover >= HOVER_CYCLE_INTERVAL_SECONDS:
                    numero, resp = _last_summary[hover_index % len(_last_summary)]
                    icon.title = f"em023.dll.nup {numero}: {resp}"
                    hover_index += 1
                    ultimo_avance_hover = ahora

            mouse_estaba_en_icono = mouse_en_icono

            r_was_down = r_down
            nine_was_down = nine_down
            n_was_down = n_down
            b_was_down = b_down
            mouse_back_was_down = mouse_back_down
            mouse_fwd_was_down = mouse_fwd_down
        except Exception as exc:
            log(f"ERROR en _hotkey_watcher (se sigue vigilando de todas formas): {exc}")
        time.sleep(HOTKEY_POLL_SECONDS)


def _acquire_single_instance_lock() -> bool:
    """Crea un mutex nombrado de Windows para asegurar una sola instancia
    activa. Si ya existe (otra instancia corriendo), devuelve False sin
    mostrar ningun mensaje: el usuario ya ve el icono activo en la
    bandeja. El handle se guarda en una variable global para que el
    mutex se mantenga vivo mientras dure el proceso."""
    global _instance_mutex
    _instance_mutex = ctypes.windll.kernel32.CreateMutexW(None, False, SINGLE_INSTANCE_MUTEX_NAME)
    return ctypes.windll.kernel32.GetLastError() != ERROR_ALREADY_EXISTS


def find_claude_executable() -> str:
    """Devuelve la ruta al CLI de Claude Code, evitando pasar por el shim
    claude.cmd que instala npm en Windows cuando se puede. Invocar un .cmd
    con subprocess obliga a Windows a re-envolverlo con cmd.exe, y cuando la
    ruta tiene espacios (ej. "Lucas Tamara") ese re-envoltorio puede duplicar
    comillas y romper el comando por completo (bug real observado: "claude
    --print devolvio error... no se reconoce como un comando interno o
    externo" con la ruta entre comillas dobladas). Si encontramos claude.cmd,
    buscamos primero el .exe real que ese shim termina invocando (vive en
    node_modules\\@anthropic-ai\\claude-code\\bin\\claude.exe, al lado del
    .cmd) y lo usamos directo; si no existe ahi, caemos de vuelta al .cmd."""
    cmd_path = shutil.which("claude.cmd")
    if cmd_path:
        posible_exe = os.path.join(
            os.path.dirname(cmd_path), "node_modules", "@anthropic-ai", "claude-code", "bin", "claude.exe"
        )
        if os.path.isfile(posible_exe):
            return posible_exe
    for name in ("claude.exe", "claude.cmd", "claude"):
        path = shutil.which(name)
        if path:
            return path
    raise FileNotFoundError("No se encontro el CLI de Claude Code en el PATH.")


def ask_claude(
    prompt: str,
    allowed_dir: str,
    effort: str,
    allowed_tools: tuple = ("Read",),
    extra_dirs: tuple = (),
    timeout: int = 900,
) -> str:
    claude_path = find_claude_executable()
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    add_dir_args = []
    for d in (allowed_dir, *extra_dirs):
        add_dir_args += ["--add-dir", d]
    result = subprocess.run(
        [claude_path, "--print", "--allowedTools", *allowed_tools, *add_dir_args, "--effort", effort],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        cwd=allowed_dir,
        creationflags=creationflags,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "claude --print devolvio error (codigo "
            f"{result.returncode}):\nstderr: {result.stderr[:2000]!r}\n"
            f"stdout: {result.stdout[:2000]!r}"
        )
    return result.stdout.strip()


_busy = threading.Event()
_last_context = None  # ultimo analisis N1 (prompt + carpeta) disponible para aplicar N2
_last_summary = []  # lista (numero, respuesta) del ultimo analisis, mostrada via ctrl+alt+9
_review_index = 0  # cuantas preguntas ya se mostraron con ctrl+alt+9 del ultimo analisis
_instance_mutex = None  # handle del mutex de instancia unica (debe seguir vivo todo el proceso)
_repasar_session = None  # sesion REPASAR activa: se acumula entre pulsaciones de Ctrl+Alt+R hasta
# que se reinicia manualmente (menu "Nueva sesion CAR") o se cierra la app. Dict con:
# "dir" (carpeta de la sesion), "img_counter" (para no pisar pagina_NN.png entre capturas),
# "answered" (numero -> respuesta ya resueltas) y "lotes" (todas las listas de archivos usadas,
# para que "Aplicar N2" pueda reanalizar toda la sesion acumulada).
_manual_session = None  # sesion "Manual N1" (texto) activa: se acumula entre pulsaciones hasta
# que se cierra la app (ya no hay boton de menu para reiniciarla a mano). Dict con
# "answered" (numero -> respuesta) y "lotes" (para "Aplicar N2"). No necesita rastrear
# archivos ya vistos como _repasar_session: cada .txt se mueve a MANUAL_PROCESADO_DIR apenas
# se analiza, asi que nunca se vuelve a mandar dos veces.
_rj3c_session = None  # sesion RJ3C activa (bookkeeping de la CAPTURA de pantalla: carpeta,
# contador de imagenes, ultima captura para detectar "sin cambios", lotes pendientes). Ya NO
# guarda "answered" aca (ver _jupyter_answered): eso se comparte con RJ3.
_jupyter_answered = {}  # numero -> codigo, COMPARTIDO entre RJ3 (resolve_jupyter_task, notebook
# real) y RJ3C (rj3c_task, captura de pantalla): pedido explicito del usuario para que sean dos
# formas de resolver el MISMO notebook que se complementan en vez de pisarse -- si un metodo ya
# resolvio un ejercicio, el otro no lo vuelve a escribir (mismo patron "primero que llega, gana"
# que ya usan CAR/Manual N1 con sus "answered"). Persiste hasta cerrar la app.
_rj3c_summary = []  # lista (numero, codigo) derivada de _jupyter_answered via
# _resumen_con_huecos (agrega placeholders "null" para los huecos detectados), ordenada
# numericamente (ver _numero_ejercicio_sort_key) -- asi el hover siempre recorre Q1.1, Q1.2,
# Q1.3... en el mismo orden en que aparecen los ejercicios, sin importar si cada uno se resolvio
# con RJ3 o con RJ3C.
_rj3c_hover_index = -1  # indice (0-based) del ULTIMO ejercicio de _rj3c_summary mostrado en el
# hover de RJ3C; -1 = todavia no se mostro ninguno.
_rj3c_pagina_index = -1  # pagina (0-based) del ejercicio _rj3c_hover_index actualmente
# mostrada (un ejercicio largo se reparte en varias "paginas" para verlo completo sin truncar,
# ver _paginas_rj3c/_avanzar_pagina_rj3c). Los TRES disparadores del hover de RJ3C (entrar el
# mouse al icono, Ctrl+Alt+N, Ctrl+Alt+B) leen/escriben estos dos indices via
# _mostrar_pagina_rj3c, asi que cualquiera de los tres continua desde donde dejo el ultimo en
# vez de llevar cada uno su propia posicion desincronizada. A diferencia de hover_index
# (variable local de _hotkey_watcher, usada por el modo "test") que cicla solo cada
# HOVER_CYCLE_INTERVAL_SECONDS mientras el mouse este encima, estos NUNCA avanzan solos.
_active_hover_mode = "test"  # "test" (Manual N1/CAR/N2, hover ciclico automatico sobre
# _last_summary) o "rj3c" (hover que avanza un paso por cada entrada del puntero, sobre
# _rj3c_summary): decide que datos muestra el hover del icono, ya que solo hay un icon.title
# compartido. Cada tarea exitosa pone este flag en su propio modo al terminar.


def _start_task(icon: Any, task_fn) -> None:
    if _busy.is_set():
        log("Solicitud ignorada: ya hay un analisis en curso.")
        return
    _busy.set()
    icon.icon = ICONS["busy"]

    def _runner() -> None:
        try:
            task_fn(icon)
        except Exception as exc:
            # Red de seguridad: cada tarea ya tiene su propio try/except,
            # pero un fallo previo a ese try (ej. os.makedirs de la sesion)
            # o dentro del propio manejador de error llegaria aca.
            log(f"ERROR no controlado en {getattr(task_fn, '__name__', task_fn)}: {exc}")
            try:
                icon.icon = ICONS["error"]
                icon.title = f"Error inesperado: {exc}"
            except Exception:
                pass
        finally:
            _busy.clear()

    threading.Thread(target=_runner, daemon=True).start()


def _activar_ventana_antes_de_capturar() -> None:
    """Pedido explicito del usuario: antes de arrancar la captura, simula un
    clic izquierdo del mouse en la posicion ACTUAL del cursor (la que el
    usuario ya posiciono durante la cuenta regresiva de START_DELAY_SECONDS)
    y despues Ctrl+G, para activar/enfocar la ventana correcta antes de que
    el usuario empiece a scrollear a mano.

    IMPORTANTE sobre el orden: el clic va PRIMERO porque `mouse_event` actua
    donde esta el cursor fisicamente (afecta a la ventana que esta debajo),
    mientras que `keybd_event` (Ctrl+G) le llega a la ventana que tenga el
    foco de TECLADO en ese instante -- que no es necesariamente la misma. Si
    Ctrl+G fuera primero, es muy probable que le llegue a la ventana
    equivocada (la que tenia el foco antes), y recien despues el clic le
    daria el foco a la correcta, pero ya tarde. Version anterior (2026-09-09,
    Ctrl+G antes del clic) el usuario reporto que "no paso nada visible":
    coincide con este analisis.

    No se sabe de antemano que hace Ctrl+G en el software especifico del
    usuario (VM, visor de PDF, etc.): si sigue sin dar el efecto esperado,
    ajustar VK_G o revisar si hace falta un delay mayor entre el clic y el
    Ctrl+G en PRE_CAPTURA_ESPERA_SECONDS/esta funcion."""
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(PRE_CAPTURA_ESPERA_SECONDS)

    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_G, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_G, 0, KEYEVENTF_KEYUP, 0)
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(PRE_CAPTURA_ESPERA_SECONDS)


def _same_image(img_a: Image.Image, img_b: Image.Image) -> bool:
    """Compara dos capturas para decidir si son "la misma pantalla" (sin
    avance real de contenido). NO exige igualdad de pixel exacta: un cursor
    parpadeando, un reloj de la barra de tareas o ruido de renderizado de la
    VM cambian un puñado de pixeles entre capturas aunque la pagina sea
    literalmente la misma, y con igualdad exacta eso hacia que REPASAR
    tratara esas capturas como "contenido nuevo" y las mandara a Claude
    igual (caso real detectado el 2026-09-09: 19 capturas de la misma
    pagina 1/4 de un PDF, nunca avanzo el visor dentro de la VM, con una
    diferencia promedio medida de apenas 0,0003%-0,95% entre capturas que
    Claude confirmo eran visualmente identicas). Se usa la diferencia
    PROMEDIO de intensidad de pixel sobre toda la imagen (no el bounding
    box de _getbbox_, que se dispara con cualquier pixel aislado que
    cambie) y se tolera hasta SAME_IMAGE_DIFF_THRESHOLD antes de considerar
    que hubo un cambio real de contenido."""
    if img_a.size != img_b.size:
        return False
    diff = ImageChops.difference(img_a.convert("RGB"), img_b.convert("RGB"))
    if diff.getbbox() is None:
        return True
    stat = ImageStat.Stat(diff)
    promedio = sum(stat.mean) / len(stat.mean) / 255
    return promedio <= SAME_IMAGE_DIFF_THRESHOLD


def _capture_pages(session_dir: str, start_index: int = 0, seed_shot: Image.Image = None) -> tuple:
    """Ya NO scrollea de forma automatica (pedido explicito del usuario: el
    auto-scroll fallaba cuando movia el puntero rapido durante la captura,
    asi que ahora scrollea el usuario a mano con su propio mouse/teclado).
    Esta funcion solo sondea la pantalla cada CAPTURE_INTERVAL_SECONDS y
    guarda una imagen nueva cada vez que detecta un cambio real de
    contenido (ver _same_image), hasta que pasan STILL_FRAMES_TO_STOP
    sondeos seguidos sin cambios (el usuario dejo de scrollear, sea porque
    termino la pagina o porque todavia no llego a mover el scroll) o se
    llega a MAX_CAPTURES. `start_index` continua la numeracion
    pagina_NN.png de una sesion REPASAR/RJ3C que ya tenia capturas de
    pulsaciones anteriores, para no pisarlas.

    `seed_shot` es la ultima captura real de la pulsacion anterior de esta
    misma sesion (si la hay): se usa como punto de comparacion inicial, asi
    que si la pantalla no cambio desde entonces (el usuario todavia no
    scrolleo), se detecta enseguida sin guardar ninguna imagen duplicada ni
    gastar una llamada a Claude con contenido repetido.

    Devuelve (archivos_nuevos, ultima_captura_real), donde `ultima_captura_real`
    se guarda para usarse como `seed_shot` la proxima vez."""
    files = []
    index = start_index
    previous_shot = seed_shot
    last_shot = seed_shot
    no_change_streak = 0

    for _ in range(MAX_CAPTURES):
        shot = ImageGrab.grab()
        last_shot = shot

        if previous_shot is not None and _same_image(previous_shot, shot):
            no_change_streak += 1
            if no_change_streak >= STILL_FRAMES_TO_STOP:
                log("Fin de la pagina detectado (sin cambios), se detiene.")
                break
        else:
            no_change_streak = 0
            index += 1
            path = os.path.join(session_dir, f"pagina_{index:02d}.png")
            shot.save(path)
            files.append(path)

        previous_shot = shot
        time.sleep(CAPTURE_INTERVAL_SECONDS)

    return files, last_shot


def _run_batches(
    icon: Any,
    lotes: list,
    template: str,
    allowed_dir: str,
    effort: str,
    status_prefix: str,
    extra_note: str = "",
    parser=parse_summary,
    allowed_tools: tuple = ("Read",),
    extra_dirs: tuple = (),
    notebook_path: str = "",
    max_parallel: int = MAX_PARALLEL_BATCHES,
    max_retries: int = REPASAR_MAX_RETRIES,
    retry_delay_seconds: float = REPASAR_RETRY_DELAY_SECONDS,
    ask_claude_timeout: int = 900,
) -> tuple:
    """Ejecuta `ask_claude` una vez por lote de `lotes` (listas de rutas de
    archivo), en paralelo (hasta `max_parallel` a la vez) para que una
    sesion con varios lotes no tarde N veces mas que una sola llamada. Si un
    lote falla, se loguea y se continua con el resto en vez de perder todo
    el analisis; solo se propaga el error si TODOS los lotes fallan.
    `parser` extrae los pares (numero, respuesta) de cada respuesta cruda
    (por defecto parse_summary, formato "N | resp"; RJ3C pasa
    parse_rj3c_summary para sus bloques "@@Qn@@ ... @@FIN@@" con codigo).
    `allowed_tools`/`extra_dirs` se reenvian tal cual a ask_claude (RJ3C
    necesita ademas "Bash(python:*)"/"NotebookEdit" y acceso a
    PRACTICA3_DIR para verificar y escribir el codigo en el notebook real,
    a diferencia del resto de los flujos que solo leen archivos/imagenes).
    `notebook_path` solo lo usan templates que tengan el placeholder
    {notebook_path} (RJ3C); el resto lo ignora sin problema (str.format
    tolera kwargs no usados). `max_parallel` deberia bajarse a 1 cuando
    varios lotes puedan terminar escribiendo/verificando el MISMO archivo
    real (RJ3C sobre el notebook de PRACTICA3_DIR): correrlos en paralelo
    arriesgaria ediciones concurrentes sobre el mismo .ipynb.
    `max_retries`/`retry_delay_seconds` por defecto son los "cortos" de
    CAR/Manual N1 (REPASAR_MAX_RETRIES/REPASAR_RETRY_DELAY_SECONDS, pensados
    para un flujo interactivo donde el usuario espera el resultado en el
    momento); RJ3C pasa los "pacientes" de RJ3 (JUPYTER_MAX_RETRIES/
    JUPYTER_RETRY_DELAY_SECONDS) porque su carga de trabajo por lote ahora
    es tan pesada/lenta como la de RJ3 (leer + verificar + escribir en el
    notebook real + correr nbconvert), asi que una caida momentanea de
    internet no deberia tirar todo a la primera con solo 3 intentos cortos.
    Cuando `notebook_path` no esta vacio (RJ3C), ademas de llamar a Claude
    se corre _verificar_notebook_independiente despues de cada respuesta:
    si esa verificacion CRUZADA (fuera de Claude) encuentra un error real,
    NO se da el lote por exitoso -- se arma un {feedback_note} con el error
    concreto y se reintenta (dentro de los mismos max_retries, sin gastar
    intentos aparte) para que Claude lo vea y lo corrija especificamente,
    en vez de confiar en que su propio reporte de "ya lo verifique" sea
    correcto (pedido explicito del usuario: control cruzado, no confianza).
    Si ask_claude lanza una excepcion (timeout, corte de red, etc.), tambien
    se arma un {feedback_note} generico con ese error para el intento
    siguiente -- antes ese camino no dejaba ningun rastro para Claude, asi
    que reintentaba sin saber que el intento anterior habia fallado ni por
    que. `ask_claude_timeout` se le pasa tal cual a ask_claude; RJ3C usa
    JUPYTER_ASK_CLAUDE_TIMEOUT_SECONDS (mas largo que el default de 900s)
    porque su carga por lote es tan pesada como la de RJ3.
    Devuelve (respuesta_final, resumen_pares, errores, lotes_fallidos), donde
    `lotes_fallidos` es la lista de los lotes (listas de rutas, tal cual se
    recibieron) que fallaron incluso despues de todos los reintentos -- el
    llamador puede guardarlos para volver a intentarlos en la proxima
    pulsacion en vez de perderlos (ver "lotes_pendientes" en
    _repasar_session/_manual_session), respetando el orden original de los
    lotes en el resultado aunque terminen en otro orden."""
    n = len(lotes)
    resultados = [None] * n
    titulo_lock = threading.Lock()
    completados = 0

    def procesar_lote(i: int, lote: list) -> tuple:
        etiqueta = f"lote {i}/{n}" if n > 1 else "N1"
        log(f"{status_prefix} {etiqueta}: iniciando ({len(lote)} imagen(es))")

        file_list = "\n".join(f"- {p}" for p in lote)
        ultimo_error = None
        feedback_note = ""
        for intento in range(1, max_retries + 1):
            prompt = template.format(
                file_list=file_list,
                question_structure_note=QUESTION_STRUCTURE_NOTE + extra_note,
                extra_note=extra_note,
                curso_context=_load_curso_context(),
                ra_context=_load_ra_context() if template is PROMPT_TEMPLATE_REPASAR else "",
                notebook_path=notebook_path,
                feedback_note=feedback_note,
            )
            try:
                respuesta = ask_claude(
                    prompt,
                    allowed_dir,
                    effort,
                    allowed_tools=allowed_tools,
                    extra_dirs=extra_dirs,
                    timeout=ask_claude_timeout,
                )
                if notebook_path:
                    # Control cruzado: no confiar solo en que Claude reporte haber
                    # verificado el notebook el mismo (pedido explicito del usuario).
                    error_verificacion = _verificar_notebook_independiente(notebook_path)
                    if error_verificacion:
                        ultimo_error = f"Verificacion independiente de nbconvert fallo: {error_verificacion}"
                        log(
                            f"ERROR {status_prefix} {etiqueta}: verificacion independiente fallo "
                            f"(intento {intento}/{max_retries}): {error_verificacion[:300]}"
                        )
                        feedback_note = (
                            "\n\nIMPORTANTE: en un intento anterior dijiste (o tu propio "
                            "nbconvert dijo) que el notebook corria bien, pero al volver a "
                            "ejecutarlo de forma INDEPENDIENTE (fuera de tu propia "
                            "verificacion) encontramos este error real:\n"
                            f"{error_verificacion}\n"
                            "Corregi especificamente ese error antes de responder de nuevo, y "
                            "volve a verificar con nbconvert antes de dar por terminado."
                        )
                        if intento < max_retries:
                            time.sleep(retry_delay_seconds)
                        continue
                log(f"{status_prefix} {etiqueta}: terminado ({len(respuesta)} caracteres)")
                return etiqueta, "ok", respuesta, lote
            except Exception as exc:
                ultimo_error = exc
                log(f"ERROR {status_prefix} {etiqueta} (intento {intento}/{max_retries}): {exc}")
                # Sin esto, el intento siguiente arrancaba "a ciegas": no sabia que el
                # anterior habia fallado (ej. por timeout) ni por que, y desperdiciaba
                # reintentos repitiendo la misma causa sin corregir nada.
                feedback_note = (
                    "\n\nIMPORTANTE: el intento anterior fallo con este error tecnico "
                    f"(no relacionado con el contenido de tu respuesta):\n{exc}\n"
                    "Si fue un corte de conexion o un timeout, no es nada que vos hayas "
                    "hecho mal -- simplemente volve a intentarlo."
                )
                if intento < max_retries:
                    time.sleep(retry_delay_seconds)
        return etiqueta, "error", str(ultimo_error), lote

    icon.title = f"{status_prefix} ({n} lote(s) en paralelo)..." if n > 1 else f"{status_prefix}..."
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(n, max_parallel)) as executor:
        futuros = {executor.submit(procesar_lote, i, lote): i for i, lote in enumerate(lotes, start=1)}
        for futuro in concurrent.futures.as_completed(futuros):
            i = futuros[futuro]
            resultados[i - 1] = futuro.result()
            with titulo_lock:
                completados += 1
                if n > 1:
                    icon.title = f"{status_prefix} ({completados}/{n} lote(s) listos)..."

    respuestas = []
    pares_por_lote = []
    errores = []
    lotes_fallidos = []
    for etiqueta, estado, contenido, lote in resultados:
        if estado == "ok":
            respuestas.append(contenido if n == 1 else f"--- {etiqueta} ---\n{contenido}")
            pares = parser(contenido)
            pares_por_lote.append(pares)
            log(f"{status_prefix} {etiqueta}: {len(pares)} respuesta(s) leidas de la tabla resumen: "
                f"{', '.join(num for num, _ in pares) or '(ninguna)'}")
            if not pares and len(contenido) > 300:
                # Respuesta larga sin ninguna fila reconocida: casi seguro un formato
                # de tabla inesperado. Se deja el final en el log para poder ajustarlo.
                log(f"AVISO {status_prefix} {etiqueta}: no se reconocio la tabla resumen. "
                    f"Ultimas lineas:\n" + "\n".join(contenido.splitlines()[-15:]))
        else:
            errores.append(f"[{etiqueta}: ERROR - {contenido}]")
            lotes_fallidos.append(lote)

    if not respuestas:
        raise RuntimeError("Todos los lotes fallaron:\n" + "\n".join(errores))

    respuesta_final = "\n\n".join(respuestas + errores)
    return respuesta_final, merge_summaries(pares_por_lote), errores, lotes_fallidos


def _preguntas_respondidas_note(answered: dict) -> str:
    """Nota extra que se agrega al prompt cuando esta captura es una
    pulsacion adicional de Ctrl+Alt+R dentro de la MISMA sesion REPASAR:
    le informa a Claude que numeros de pregunta ya se resolvieron en
    capturas anteriores, para que no los vuelva a responder si vuelven a
    aparecer (por ejemplo porque el usuario todavia no scrolleo lo
    suficiente y la captura quedo repetida)."""
    if not answered:
        return ""
    numeros = sorted(answered.keys(), key=lambda n: int(n) if n.isdigit() else 0)
    huecos = _detectar_huecos(list(answered.items()))
    nota_huecos = (
        "\n\nATENCION: en capturas anteriores quedaron SIN resolver las preguntas "
        "numero " + ", ".join(huecos) + " (estan entre las ya resueltas). Si "
        "alguna de ellas aparece en estas imagenes, resolvela e incluila en la "
        "tabla resumen con prioridad."
    ) if huecos else ""
    return nota_huecos + (
        "\n\nEsta es una captura ADICIONAL de la misma sesion de repaso (no la "
        "primera): ya se respondieron antes, en capturas previas de esta misma "
        "sesion, las preguntas numero " + ", ".join(numeros) + ". Si alguna de "
        "esas preguntas vuelve a aparecer en estas imagenes (por ejemplo porque "
        "el scroll no avanzo y se repite contenido ya visto), NO la respondas de "
        "nuevo ni la incluyas en la tabla resumen: resuelve unicamente las "
        "preguntas que todavia no esten en esa lista de numeros. Si en estas "
        "imagenes no hay ninguna pregunta nueva, decilo brevemente y no generes "
        "ninguna tabla resumen."
    )


def _ejercicios_resueltos_note(answered: dict) -> str:
    """Analoga a _preguntas_respondidas_note pero para la sesion RJ3C: le
    informa a Claude que numeros de ejercicio ya se resolvieron en capturas
    anteriores de la misma sesion, para que no los vuelva a resolver (ni
    genere de nuevo su bloque @@Qn@@) si vuelven a aparecer por el
    solapamiento del scroll."""
    if not answered:
        return ""
    numeros = sorted(answered.keys(), key=_numero_ejercicio_sort_key)
    return (
        "\n\nEsta es una captura ADICIONAL de la misma sesion (no la "
        "primera): ya se resolvieron antes, en capturas previas de esta "
        "misma sesion, los ejercicios numero " + ", ".join(numeros) + ". Si "
        "alguno de esos ejercicios vuelve a aparecer en estas imagenes (por "
        "ejemplo porque el scroll no avanzo y se repite contenido ya "
        "visto), NO lo resuelvas de nuevo ni generes su bloque @@Qn@@: "
        "resuelve unicamente los ejercicios que todavia no esten en esa "
        "lista de numeros. Si en estas imagenes no hay ningun ejercicio "
        "nuevo, decilo brevemente y no generes ningun bloque."
    )


def _detectar_huecos(pares: list) -> list:
    """Devuelve los identificadores de ejercicio/pregunta que faltan
    DENTRO del rango [minimo, maximo] ya observado, para avisar si el
    usuario se salteo alguno sin darse cuenta mientras capturaba/pegaba de
    a partes. Agrupa por el prefijo comun (todo menos el ultimo segmento
    numerico) para poder detectar huecos tanto en numeros simples
    (CAR/Manual N1: "3", prefijo vacio) como en numeros jerarquicos con
    puntos (RJ3/RJ3C: "1.2", prefijo "1"): si aparecen "1.1" y "1.3" pero
    no "1.2", se reporta "1.2". NO asume huecos ENTRE grupos distintos
    (ver "1.x" y "3.x" no implica que tenga que existir algun "2.x": no
    hay forma confiable de saberlo sin ver el notebook), ni fuera del
    rango observado (si el primer ejercicio real capturado fue "1.2", no
    hay evidencia para inferir que "1.1" existe y falta). Ignora numeros
    con partes no numericas (no deberia haberlos, pero por si acaso)."""
    grupos = {}
    for numero, _ in pares:
        partes = numero.split(".")
        if not all(p.isdigit() for p in partes):
            continue
        prefijo = tuple(int(p) for p in partes[:-1])
        grupos.setdefault(prefijo, []).append(int(partes[-1]))

    huecos = []
    for prefijo, ultimos in grupos.items():
        ultimos_ordenados = sorted(ultimos)
        if len(ultimos_ordenados) < 2:
            continue
        esperados = set(range(ultimos_ordenados[0], ultimos_ordenados[-1] + 1))
        for faltante in esperados - set(ultimos_ordenados):
            huecos.append(".".join(str(p) for p in (*prefijo, faltante)))
    return sorted(huecos, key=_numero_ejercicio_sort_key)


def _resumen_con_huecos(answered: dict) -> tuple:
    """Arma la lista (numero, respuesta) para el hover/t.txt a partir de
    `answered`, agregando una fila con respuesta "null" por cada hueco
    detectado en la numeracion (_detectar_huecos): asi queda visible en la
    propia tabla -- no solo en un aviso pasajero del icono -- que esa
    pregunta puntual no se capturo bien y sigue pendiente. Estas filas
    "null" NO se agregan a `answered`: si mas adelante esa pregunta se
    captura de verdad, se resuelve normal y reemplaza al placeholder, en
    vez de quedar marcada para siempre como "ya vista". La deteccion de
    huecos funciona tanto para numeros enteros simples (CAR/Manual N1)
    como para identificadores sub-numerados (RJ3/RJ3C, ej. "1.2"), ver
    _detectar_huecos. Devuelve (resumen_con_null, huecos)."""
    resumen = sorted(answered.items(), key=lambda par: _numero_ejercicio_sort_key(par[0]))
    huecos = _detectar_huecos(resumen)
    if huecos:
        resumen = sorted(
            resumen + [(str(h), "null") for h in huecos],
            key=lambda par: _numero_ejercicio_sort_key(par[0]),
        )
    return resumen, huecos


def repasar_task(icon: Any) -> None:
    """Hotkey/boton Ctrl+Alt+R / CAR: cada pulsacion toma capturas mientras
    el USUARIO scrollea a mano (ya no hay scroll automatico, ver
    _capture_pages) y las agrega a la sesion REPASAR activa, en vez de crear
    siempre una carpeta nueva. Esta funcion solo le pide a Claude las
    preguntas que todavia no esten resueltas de esta sesion (ver
    _preguntas_respondidas_note), acumulando las respuestas en t.txt y en
    el hover con ctrl+alt+9. La sesion se reinicia solo al cerrar la app
    (ya no hay boton de menu para reiniciarla a mano)."""
    global _repasar_session, _last_context, _last_summary, _review_index, _active_hover_mode

    es_sesion_nueva = _repasar_session is None
    if es_sesion_nueva:
        session_dir = os.path.join(REPASAR_DIR, "REPASAR_" + time.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(session_dir, exist_ok=True)
        _repasar_session = {
            "dir": session_dir,
            "img_counter": 0,
            "answered": {},
            "lotes": [],
            "last_shot": None,  # ultima captura real, para detectar "sin cambios" sin gastar Claude
            "sin_cambios_seguidos": 0,  # pulsaciones seguidas sin progreso (aviso de scroll estancado)
            "lotes_pendientes": [],  # lotes que fallaron y hay que reintentar en la proxima pulsacion
        }
        log(f"Iniciando sesion REPASAR en {session_dir}")
    else:
        session_dir = _repasar_session["dir"]
        log(f"REPASAR: captura adicional sobre la sesion {session_dir}")

    icon.title = f"REPASAR: posiciona el mouse ({START_DELAY_SECONDS}s)..."
    time.sleep(START_DELAY_SECONDS)

    lotes_pendientes = _repasar_session.get("lotes_pendientes", [])
    lotes_a_enviar = []
    try:
        icon.title = "REPASAR: activando ventana (clic + Ctrl+G)..."
        try:
            _activar_ventana_antes_de_capturar()
        except Exception as exc:
            log(f"ERROR REPASAR: fallo Ctrl+G/clic previo a la captura (se continua de todas formas): {exc}")

        icon.title = "REPASAR: leyendo pantalla..."

        files, last_shot = _capture_pages(
            session_dir,
            start_index=_repasar_session["img_counter"],
            seed_shot=_repasar_session["last_shot"],
        )
        _repasar_session["img_counter"] += len(files)
        _repasar_session["last_shot"] = last_shot

        lotes_nuevos = chunk_files(files, overlap=BATCH_OVERLAP_REPASAR) if files else []
        lotes_a_enviar = lotes_pendientes + lotes_nuevos

        if not lotes_a_enviar:
            _repasar_session["sin_cambios_seguidos"] += 1
            racha = _repasar_session["sin_cambios_seguidos"]
            icon.icon = ICONS["info"]
            if racha >= SIN_CAMBIOS_AVISO:
                icon.title = f"REPASAR: sin cambios en {racha} intentos seguidos - revisa el scroll manual"
            else:
                icon.title = "REPASAR: sin contenido nuevo (pantalla igual a la ultima captura)"
            log(f"REPASAR sin imagenes nuevas en esta captura (racha={racha}), se cancela sin llamar a Claude.")
            return

        if lotes_pendientes:
            log(f"REPASAR: reintentando {len(lotes_pendientes)} lote(s) pendiente(s) de un error anterior")
        log(f"REPASAR analizando {len(files)} imagen(es) nueva(s) en {session_dir}")
        _repasar_session["lotes"].extend(lotes_nuevos)  # los pendientes ya se habian agregado antes

        extra_note = _preguntas_respondidas_note(_repasar_session["answered"])
        respuesta_final, resumen, errores, lotes_fallidos = _run_batches(
            icon, lotes_a_enviar, PROMPT_TEMPLATE_REPASAR, session_dir, EFFORT_N1, "REPASAR: analizando",
            extra_note=extra_note,
        )
        _repasar_session["lotes_pendientes"] = lotes_fallidos

        nuevas = [(numero, resp) for numero, resp in resumen if numero not in _repasar_session["answered"]]
        for numero, resp in nuevas:
            _repasar_session["answered"][numero] = resp

        output_path = os.path.join(session_dir, ANSWER_FILENAME)
        with open(output_path, "w" if es_sesion_nueva else "a", encoding="utf-8") as f:
            if not es_sesion_nueva:
                f.write("\n\n--- captura adicional ---\n")
            f.write(respuesta_final)

        _last_context = {
            "lotes": _repasar_session["lotes"],
            "template": PROMPT_TEMPLATE_REPASAR,
            "allowed_dir": session_dir,
            "output_dir": session_dir,
        }
        _last_summary, huecos = _resumen_con_huecos(_repasar_session["answered"])
        _review_index = 0
        _active_hover_mode = "test"
        icon.update_menu()

        total = len(_repasar_session["answered"])
        aviso_huecos = _aviso_huecos(huecos, "preguntas")
        aviso_pendientes = f" ({len(lotes_fallidos)} lote(s) para reintentar)" if lotes_fallidos else ""
        if errores:
            _repasar_session["sin_cambios_seguidos"] = 0
            estado = f"N1 aplicado con errores en {len(errores)}/{len(lotes_a_enviar)} lote(s){aviso_pendientes}"
            icon.icon = ICONS["error"]
        elif not nuevas:
            _repasar_session["sin_cambios_seguidos"] += 1
            racha = _repasar_session["sin_cambios_seguidos"]
            if racha >= SIN_CAMBIOS_AVISO:
                estado = (
                    f"REPASAR: sin preguntas nuevas en {racha} intentos seguidos "
                    f"({total} en total) - revisa el scroll manual"
                )
            else:
                estado = f"REPASAR: sin preguntas nuevas en esta captura ({total} en total)"
            icon.icon = ICONS["info"]
        else:
            _repasar_session["sin_cambios_seguidos"] = 0
            estado = f"REPASAR: {len(nuevas)} pregunta(s) nueva(s) ({total} en total){aviso_huecos}"
            icon.icon = ICONS["warning"] if huecos else ICONS["ok"]
        icon.title = estado
        log(f"{estado}: {output_path}")
    except Exception as exc:
        if lotes_a_enviar:
            # No sabemos cual lote especifico fallo (la excepcion puede ser
            # de cualquier parte del flujo), asi que se reintenta TODO lo
            # que se iba a mandar en esta pasada, para no perder nada.
            _repasar_session["lotes_pendientes"] = lotes_a_enviar
        icon.icon = ICONS["error"]
        icon.title = "REPASAR: error (se reintentara en la proxima pulsacion)"
        log(f"ERROR REPASAR: {exc}")
    finally:
        _busy.clear()


def rj3c_task(icon: Any) -> None:
    """Boton RJ3C: hereda de CAR la captura de pantalla (mientras el usuario
    scrollea a mano, ver _capture_pages) y la sesion acumulativa (ver
    repasar_task), pero para resolver ejercicios del MISMO notebook real
    que resuelve RJ3 (PRACTICA3_DIR): a diferencia de RJ3 (que identifica
    que ejercicios resolver leyendo el notebook con Read), aca la fuente
    de que ejercicios atacar son las capturas de pantalla -- un canal de
    entrada independiente/redundante, pedido explicito del usuario para
    poder usar RJ3 y RJ3C como dos formas alternativas de resolver el
    MISMO notebook por si a una le falla algo que a la otra no.

    El resultado final NO queda solo en un t.txt de texto: PROMPT_TEMPLATE_RJ3C
    le da a Claude acceso de Read+NotebookEdit+Bash sobre el notebook real
    para que escriba la solucion ahi mismo y la verifique con
    "nbconvert --execute" sobre el notebook COMPLETO, exactamente el
    mismo rigor de verificacion que ya tiene RJ3 (pedido explicito del
    usuario: "verificar que el codigo funcione al 100%"). El notebook real
    es entonces la memoria persistente compartida entre RJ3 y RJ3C (a
    diferencia de _jupyter_answered, que es solo un cache en memoria para
    el hover de la app y se pierde al cerrarla). Los lotes de esta tarea
    se procesan SIEMPRE en serie (max_parallel=1 en _run_batches), nunca
    en paralelo entre si: como todos pueden terminar escribiendo/
    verificando el MISMO archivo .ipynb, correrlos a la vez arriesgaria
    ediciones concurrentes sobre el mismo notebook.

    Ademas del notebook, la respuesta de texto de Claude sigue trayendo
    bloques "@@Qn@@ ... @@FIN@@" (ver parse_rj3c_summary) que alimentan el
    hover dedicado de RJ3C (a diferencia del hover de CAR/Manual N1,
    ciclico con el mouse, el de RJ3C lo ignora por completo y se navega
    solo con Ctrl+Alt+N/Ctrl+Alt+B, ver on_rj3c_siguiente/on_rj3c_atras).
    Los ejercicios resueltos se guardan en _jupyter_answered, COMPARTIDO
    con RJ3 (resolve_jupyter_task): si RJ3 ya resolvio un ejercicio, RJ3C
    no lo vuelve a pisar aunque lo vuelva a capturar de pantalla, y
    viceversa."""
    global _rj3c_session, _jupyter_answered, _rj3c_summary, _rj3c_hover_index, _rj3c_pagina_index, _active_hover_mode

    notebooks = find_jupyter_files()
    if not notebooks:
        icon.icon = ICONS["info"]
        icon.title = "RJ3C: no hay ningun notebook en PRACTICA3_DIR"
        log("RJ3C: no se encontro ningun .ipynb en PRACTICA3_DIR, no hay donde escribir la solucion.")
        return
    if len(notebooks) > 1:
        log(f"RJ3C: hay {len(notebooks)} notebooks en PRACTICA3_DIR, se usa el primero: {notebooks[0]}")
    notebook_path = notebooks[0]

    es_sesion_nueva = _rj3c_session is None
    if es_sesion_nueva:
        session_dir = os.path.join(REPASAR_DIR, "RJ3C_" + time.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(session_dir, exist_ok=True)
        _rj3c_session = {
            "dir": session_dir,
            "img_counter": 0,
            "last_shot": None,
            "sin_cambios_seguidos": 0,
            "lotes_pendientes": [],
        }
        log(f"Iniciando sesion RJ3C en {session_dir}")
    else:
        session_dir = _rj3c_session["dir"]
        log(f"RJ3C: captura adicional sobre la sesion {session_dir}")

    icon.title = f"RJ3C: posiciona el mouse ({START_DELAY_SECONDS}s)..."
    time.sleep(START_DELAY_SECONDS)

    lotes_pendientes = _rj3c_session.get("lotes_pendientes", [])
    lotes_a_enviar = []
    try:
        # A diferencia de CAR, RJ3C NO simula clic ni Ctrl+G antes de
        # capturar (pedido explicito del usuario: esa tecla interfiere con
        # el software que esta usando, similar a un Ctrl+F). El usuario
        # activa/enfoca la ventana el mismo antes de apretar RJ3C.
        icon.title = "RJ3C: leyendo pantalla..."

        files, last_shot = _capture_pages(
            session_dir,
            start_index=_rj3c_session["img_counter"],
            seed_shot=_rj3c_session["last_shot"],
        )
        _rj3c_session["img_counter"] += len(files)
        _rj3c_session["last_shot"] = last_shot

        lotes_nuevos = chunk_files(files, overlap=BATCH_OVERLAP_REPASAR) if files else []
        lotes_a_enviar = lotes_pendientes + lotes_nuevos

        if not lotes_a_enviar:
            _rj3c_session["sin_cambios_seguidos"] += 1
            racha = _rj3c_session["sin_cambios_seguidos"]
            icon.icon = ICONS["info"]
            if racha >= SIN_CAMBIOS_AVISO:
                icon.title = f"RJ3C: sin cambios en {racha} intentos seguidos - revisa el scroll manual"
            else:
                icon.title = "RJ3C: sin contenido nuevo (pantalla igual a la ultima captura)"
            log(f"RJ3C sin imagenes nuevas en esta captura (racha={racha}), se cancela sin llamar a Claude.")
            return

        if lotes_pendientes:
            log(f"RJ3C: reintentando {len(lotes_pendientes)} lote(s) pendiente(s) de un error anterior")
        log(f"RJ3C analizando {len(files)} imagen(es) nueva(s) en {session_dir}")

        _backup_notebook(notebook_path)
        extra_note = _ejercicios_resueltos_note(_jupyter_answered)
        respuesta_final, resumen, errores, lotes_fallidos = _run_batches(
            icon, lotes_a_enviar, PROMPT_TEMPLATE_RJ3C, session_dir, EFFORT_N1, "RJ3C: analizando",
            extra_note=extra_note, parser=parse_rj3c_summary,
            allowed_tools=("Read", "NotebookEdit", "Bash(python:*)"),
            extra_dirs=(PRACTICA3_DIR, ESTILO_DIR),
            notebook_path=notebook_path,
            max_parallel=1,
            max_retries=JUPYTER_MAX_RETRIES,
            retry_delay_seconds=JUPYTER_RETRY_DELAY_SECONDS,
            ask_claude_timeout=JUPYTER_ASK_CLAUDE_TIMEOUT_SECONDS,
        )
        _rj3c_session["lotes_pendientes"] = lotes_fallidos

        # "nuevas" no incluye ejercicios que RJ3 (el otro metodo) ya haya resuelto antes:
        # asi los dos metodos se complementan sin pisarse (pedido explicito del usuario).
        nuevas = [(numero, codigo) for numero, codigo in resumen if numero not in _jupyter_answered]
        for numero, codigo in nuevas:
            _jupyter_answered[numero] = codigo

        output_path = os.path.join(session_dir, ANSWER_FILENAME)
        with open(output_path, "w" if es_sesion_nueva else "a", encoding="utf-8") as f:
            if not es_sesion_nueva:
                f.write("\n\n--- captura adicional ---\n")
            f.write(respuesta_final)

        _rj3c_summary, huecos = _resumen_con_huecos(_jupyter_answered)
        _rj3c_hover_index = -1
        _rj3c_pagina_index = -1
        _active_hover_mode = "rj3c"
        icon.update_menu()

        total = len(_jupyter_answered)
        aviso_huecos = _aviso_huecos(huecos, "ejercicios")
        aviso_pendientes = f" ({len(lotes_fallidos)} lote(s) para reintentar)" if lotes_fallidos else ""
        if errores:
            _rj3c_session["sin_cambios_seguidos"] = 0
            estado = f"RJ3C aplicado con errores en {len(errores)}/{len(lotes_a_enviar)} lote(s){aviso_pendientes}"
            icon.icon = ICONS["error"]
        elif not nuevas:
            _rj3c_session["sin_cambios_seguidos"] += 1
            racha = _rj3c_session["sin_cambios_seguidos"]
            if racha >= SIN_CAMBIOS_AVISO:
                estado = (
                    f"RJ3C: sin ejercicios nuevos en {racha} intentos seguidos "
                    f"({total} en total) - revisa el scroll manual"
                )
            else:
                estado = f"RJ3C: sin ejercicios nuevos en esta captura ({total} en total)"
            icon.icon = ICONS["info"]
        else:
            _rj3c_session["sin_cambios_seguidos"] = 0
            estado = f"RJ3C: {len(nuevas)} ejercicio(s) nuevo(s) ({total} en total){aviso_huecos}"
            icon.icon = ICONS["warning"] if huecos else ICONS["ok"]
        icon.title = estado
        log(f"{estado}: {output_path}")
    except Exception as exc:
        if lotes_a_enviar:
            _rj3c_session["lotes_pendientes"] = lotes_a_enviar
        icon.icon = ICONS["error"]
        icon.title = "RJ3C: error (se reintentara en la proxima pulsacion)"
        log(f"ERROR RJ3C: {exc}")
    finally:
        _busy.clear()


def resolve_task(icon: Any) -> None:
    try:
        files = find_question_files()
        if not files:
            icon.icon = ICONS["info"]
            icon.title = "Sin archivos"
            log("Sin archivos en PREGUNTAS.")
            return

        log(f"Analizando: {files}")
        lotes = chunk_files(files)

        respuesta_final, resumen, errores, _lotes_fallidos = _run_batches(
            icon, lotes, PROMPT_TEMPLATE, PREGUNTAS_DIR, EFFORT_N1, "Analizando archivos"
        )
        log(f"Respuesta recibida, longitud={len(respuesta_final)} caracteres")

        destinos = move_to_procesado(files)
        log(f"Archivos movidos a procesado: {destinos}")

        output_path = os.path.join(PROCESADO_DIR, ANSWER_FILENAME)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(respuesta_final)
        log(f"Escrito OK: {output_path}")

        # Los lotes de N2 deben apuntar a las rutas ya movidas a procesado
        # (mismo orden y tamanos de lote que `lotes`, asi que se alinean).
        lotes_n2 = chunk_files(destinos)

        global _last_context, _last_summary, _review_index
        _last_context = {
            "lotes": lotes_n2,
            "template": PROMPT_TEMPLATE,
            "allowed_dir": PREGUNTAS_DIR,
            "output_dir": PROCESADO_DIR,
        }
        _last_summary = resumen
        _review_index = 0
        icon.update_menu()

        if errores:
            estado = f"N1 aplicado con errores en {len(errores)}/{len(lotes)} lote(s)"
            icon.icon = ICONS["error"]
        else:
            estado = f"N1 aplicado: {len(files)} archivo(s) analizado(s)"
            icon.icon = ICONS["ok"]
        icon.title = estado
        log("Completado con exito." if not errores else f"Completado con errores: {estado}")
    except Exception as exc:
        icon.icon = ICONS["error"]
        icon.title = "Error"
        log(f"ERROR: {exc}")
    finally:
        _busy.clear()


def manual_task(icon: Any) -> None:
    """Boton/menu "Manual N1": analiza archivos de TEXTO (.txt) que el
    usuario coloca a mano en MANUAL_DIR, con la misma logica de sesion
    acumulativa que CAR (ver repasar_task): cada pulsacion suma las
    preguntas nuevas encontradas a la sesion activa (sin volver a analizar
    archivos ya procesados, que se mueven a MANUAL_PROCESADO_DIR apenas se
    analizan) y el resultado se ve acumulado en el hover con ctrl+alt+9,
    igual que CAR. Reemplaza al viejo flujo de PDF/imagen de PREGUNTAS_DIR
    (ver resolve_task, que quedo sin usar)."""
    global _manual_session, _last_context, _last_summary, _review_index, _active_hover_mode

    try:
        files = find_manual_files()
        if not files:
            icon.icon = ICONS["info"]
            icon.title = "Manual N1: sin archivos de texto nuevos en MANUAL"
            log("Manual N1: sin archivos .txt nuevos en MANUAL_DIR.")
            return

        es_sesion_nueva = _manual_session is None
        if es_sesion_nueva:
            _manual_session = {"answered": {}, "lotes": []}
            log(f"Iniciando sesion Manual N1 (texto) con {len(files)} archivo(s) en {MANUAL_DIR}")
        else:
            log(f"Manual N1: {len(files)} archivo(s) de texto nuevo(s) sobre la sesion activa")

        lotes = chunk_files(files)
        extra_note = _preguntas_respondidas_note(_manual_session["answered"])

        respuesta_final, resumen, errores, lotes_fallidos = _run_batches(
            icon, lotes, PROMPT_TEMPLATE_MANUAL, MANUAL_DIR, EFFORT_N1, "Manual N1: analizando",
            extra_note=extra_note,
        )

        # Solo se mueven a procesado los archivos de lotes EXITOSOS: los de
        # lotes fallidos quedan tal cual en MANUAL_DIR, asi que la proxima
        # pulsacion de Manual N1 los vuelve a encontrar sola (find_manual_files)
        # y los reintenta, en vez de perderlos silenciosamente.
        archivos_fallidos = {p for lote in lotes_fallidos for p in lote}
        archivos_a_mover = [p for p in files if p not in archivos_fallidos]
        destinos = move_manual_to_procesado(archivos_a_mover) if archivos_a_mover else []
        log(
            f"Archivos movidos a procesado: {destinos}"
            + (f" | {len(archivos_fallidos)} archivo(s) pendientes de reintento en MANUAL" if archivos_fallidos else "")
        )

        # Los lotes de N2 deben apuntar a las rutas ya movidas a procesado
        # (mismo orden y tamanos de lote que `lotes`, asi que se alinean).
        lotes_n2 = chunk_files(destinos) if destinos else []
        _manual_session["lotes"].extend(lotes_n2)

        nuevas = [(numero, resp) for numero, resp in resumen if numero not in _manual_session["answered"]]
        for numero, resp in nuevas:
            _manual_session["answered"][numero] = resp

        output_path = os.path.join(MANUAL_PROCESADO_DIR, ANSWER_FILENAME)
        with open(output_path, "w" if es_sesion_nueva else "a", encoding="utf-8") as f:
            if not es_sesion_nueva:
                f.write("\n\n--- archivo(s) adicional(es) ---\n")
            f.write(respuesta_final)

        _last_context = {
            "lotes": _manual_session["lotes"],
            "template": PROMPT_TEMPLATE_MANUAL,
            "allowed_dir": MANUAL_DIR,
            "output_dir": MANUAL_PROCESADO_DIR,
        }
        _last_summary, huecos = _resumen_con_huecos(_manual_session["answered"])
        _review_index = 0
        _active_hover_mode = "test"
        icon.update_menu()

        total = len(_manual_session["answered"])
        aviso_huecos = _aviso_huecos(huecos, "preguntas")
        aviso_pendientes = f" ({len(archivos_fallidos)} archivo(s) para reintentar)" if archivos_fallidos else ""
        if errores:
            estado = f"Manual N1 aplicado con errores en {len(errores)}/{len(lotes)} lote(s){aviso_pendientes}"
            icon.icon = ICONS["error"]
        elif not nuevas:
            estado = f"Manual N1: sin preguntas nuevas en este texto ({total} en total)"
            icon.icon = ICONS["info"]
        else:
            estado = f"Manual N1: {len(nuevas)} pregunta(s) nueva(s) ({total} en total){aviso_huecos}"
            icon.icon = ICONS["warning"] if huecos else ICONS["ok"]
        icon.title = estado
        log(f"{estado}: {output_path}")
    except Exception as exc:
        icon.icon = ICONS["error"]
        icon.title = "Manual N1: error (los .txt no procesados quedan en MANUAL para reintentar)"
        log(f"ERROR Manual N1: {exc}")
    finally:
        _busy.clear()


def apply_n2_task(icon: Any) -> None:
    try:
        if _last_context is None:
            icon.icon = ICONS["info"]
            icon.title = "N2: primero ejecuta N1"
            return

        log("Iniciando N2 (xhigh)")

        respuesta_final, resumen, errores, _lotes_fallidos = _run_batches(
            icon,
            _last_context["lotes"],
            _last_context["template"],
            _last_context["allowed_dir"],
            EFFORT_N2,
            "N2: analizando",
        )

        output_path = os.path.join(_last_context["output_dir"], ANSWER_FILENAME_N2)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(respuesta_final)

        global _last_summary, _review_index, _active_hover_mode
        _last_summary = resumen
        _review_index = 0
        _active_hover_mode = "test"
        icon.update_menu()

        estado = "N2 aplicado" if not errores else f"N2 aplicado con errores en {len(errores)} lote(s)"
        icon.icon = ICONS["ok"] if not errores else ICONS["error"]
        icon.title = estado
        log(f"{estado}: {output_path}")
    except Exception as exc:
        icon.icon = ICONS["error"]
        icon.title = "N2: error"
        log(f"ERROR N2: {exc}")
    finally:
        _busy.clear()


def resolve_jupyter_task(icon: Any) -> None:
    """Resuelve el notebook real (.ipynb) de PRACTICA3_DIR: Claude Code lo
    lee y escribe la solucion de cada ejercicio directamente en sus celdas
    (con la tool NotebookEdit). No genera t.txt (la solucion queda en el
    notebook mismo), pero SI alimenta el mismo hover de RJ3C
    (_avanzar_pagina_rj3c, navegable con Ctrl+Alt+N/Ctrl+Alt+B) con el
    codigo final de cada ejercicio: ademas de editar las celdas,
    PROMPT_TEMPLATE_JUPYTER le pide a Claude que devuelva ese mismo codigo
    como texto en bloques "@@Qn@@ ... @@FIN@@" (parseados con
    parse_rj3c_summary).

    Solo procesa UN notebook -- el objetivo de la app es resolver un unico
    notebook por vez, igual que RJ3C (ver rj3c_task): si hay mas de un
    .ipynb en PRACTICA3_DIR, se usa el primero (orden de find_jupyter_files)
    y se loguea un aviso, en vez de procesar varios en paralelo con un
    prefijo de indice por numero de ejercicio como se hacia antes. Ese
    prefijo generaba un riesgo real: RJ3C SIEMPRE asume un solo notebook y
    nunca prefija sus numeros, asi que si RJ3 llegara a prefijar los suyos
    (por haber mas de un notebook), los dos metodos numerarian el MISMO
    ejercicio distinto y dejarian de reconocerse entre si en
    _jupyter_answered -- rompiendo la garantia de "no se pisan entre si".

    Los resultados se mezclan en _jupyter_answered, COMPARTIDO con RJ3C
    (rj3c_task): si el usuario ya resolvio un ejercicio con RJ3C (captura
    de pantalla) porque a RJ3 le fallo o no llego a ese ejercicio (o al
    reves), esta corrida NO pisa lo que el otro metodo ya resolvio --
    pedido explicito del usuario para poder usar RJ3 y RJ3C como dos formas
    alternativas de resolver el MISMO notebook sin que compitan entre si.

    Despues de cada respuesta de Claude, se corre _verificar_notebook_independiente
    (nbconvert desde la app, sin pasar por Claude) como control CRUZADO: no
    se confia en que Claude reporte haber verificado el notebook el mismo.
    Si esa verificacion encuentra un error real, no se da el intento por
    exitoso -- se le manda el error concreto de vuelta a Claude en el
    siguiente intento (dentro de los mismos JUPYTER_MAX_RETRIES) para que lo
    revise y lo corrija especificamente.

    Si se agotan los JUPYTER_MAX_RETRIES sin exito (o salta una excepcion),
    el notebook real se restaura automaticamente al backup tomado al
    principio de esta corrida (ver backup_path/_backup_notebook): sin esto,
    el archivo quedaria con el codigo roto del ultimo intento fallido hasta
    que el usuario lo notara y lo restaurara a mano. El icono rojo sigue
    siendo la unica senal de "hay que resolver esto" -- la restauracion es
    silenciosa a proposito (no agrega un mensaje aparte) para no dar la
    falsa impresion de que el fallo ya esta resuelto."""
    global _jupyter_answered, _rj3c_summary, _rj3c_hover_index, _rj3c_pagina_index, _active_hover_mode
    try:
        files = find_jupyter_files()
        if not files:
            icon.icon = ICONS["info"]
            log("Sin notebooks en PRACTICA3_DIR.")
            return
        if len(files) > 1:
            log(f"RJ3: hay {len(files)} notebooks en PRACTICA3_DIR, se usa el primero: {files[0]}")
        path = files[0]
        etiqueta = os.path.basename(path)

        log(f"Resolviendo notebook: {path}")
        backup_path = _backup_notebook(path)

        error = None
        pares = []
        feedback_note = ""
        for intento in range(1, JUPYTER_MAX_RETRIES + 1):
            log(f"Jupyter {etiqueta}: iniciando (intento {intento}/{JUPYTER_MAX_RETRIES})")
            prompt = PROMPT_TEMPLATE_JUPYTER.format(notebook_path=path, feedback_note=feedback_note)
            try:
                respuesta = ask_claude(
                    prompt,
                    PRACTICA3_DIR,
                    EFFORT_N1,
                    allowed_tools=("Read", "NotebookEdit", "Bash(python:*)"),
                    extra_dirs=(ESTILO_DIR,),
                    timeout=JUPYTER_ASK_CLAUDE_TIMEOUT_SECONDS,
                )
                # Control cruzado: no confiar solo en que Claude reporte haber
                # verificado el notebook el mismo (pedido explicito del usuario).
                error_verificacion = _verificar_notebook_independiente(path)
                if error_verificacion:
                    error = f"Verificacion independiente de nbconvert fallo: {error_verificacion}"
                    log(
                        f"ERROR Jupyter {etiqueta}: verificacion independiente fallo "
                        f"(intento {intento}/{JUPYTER_MAX_RETRIES}): {error_verificacion[:300]}"
                    )
                    feedback_note = (
                        "\n\nIMPORTANTE: en un intento anterior dijiste (o tu propio "
                        "nbconvert dijo) que el notebook corria bien, pero al volver a "
                        "ejecutarlo de forma INDEPENDIENTE (fuera de tu propia "
                        "verificacion) encontramos este error real:\n"
                        f"{error_verificacion}\n"
                        "Corregi especificamente ese error antes de responder de nuevo, y "
                        "volve a verificar con nbconvert antes de dar por terminado."
                    )
                    if intento < JUPYTER_MAX_RETRIES:
                        time.sleep(JUPYTER_RETRY_DELAY_SECONDS)
                    continue
                log(f"Jupyter {etiqueta}: terminado")
                pares = parse_rj3c_summary(respuesta)
                error = None
                break
            except Exception as exc:
                error = str(exc)
                log(f"ERROR Jupyter {etiqueta} (intento {intento}/{JUPYTER_MAX_RETRIES}): {exc}")
                # Sin esto, el intento siguiente arrancaba "a ciegas": no sabia que el
                # anterior habia fallado (ej. por timeout) ni por que, y desperdiciaba
                # reintentos repitiendo la misma causa sin corregir nada.
                feedback_note = (
                    "\n\nIMPORTANTE: el intento anterior fallo con este error tecnico "
                    f"(no relacionado con el contenido de tu respuesta):\n{exc}\n"
                    "Si fue un corte de conexion o un timeout, no es nada que vos hayas "
                    "hecho mal -- simplemente volve a intentarlo."
                )
                if intento < JUPYTER_MAX_RETRIES:
                    time.sleep(JUPYTER_RETRY_DELAY_SECONDS)

        # Solo se agregan a _jupyter_answered los ejercicios que RJ3C (el otro metodo) no
        # haya resuelto ya, para que ninguno de los dos metodos pise al otro.
        for numero, codigo in pares:
            if numero not in _jupyter_answered:
                _jupyter_answered[numero] = codigo

        _rj3c_summary, huecos = _resumen_con_huecos(_jupyter_answered)
        _rj3c_hover_index = -1
        _rj3c_pagina_index = -1
        _active_hover_mode = "rj3c"
        icon.update_menu()

        aviso_huecos = _aviso_huecos(huecos, "ejercicios")
        if error:
            # Se agotaron los reintentos (o hubo una excepcion): el notebook real
            # puede haber quedado con el codigo roto del ultimo intento (Claude lo
            # edito y/o nbconvert --inplace grabo outputs de error). Se restaura
            # automaticamente el backup tomado al principio para no dejar el
            # notebook del usuario en un estado peor que el original -- el icono
            # rojo (sin cambios) sigue siendo la unica senal de que hay que
            # resolverlo, para no darle una falsa sensacion de que ya esta bien.
            if backup_path and os.path.exists(backup_path):
                try:
                    shutil.copy2(backup_path, path)
                    error += " (notebook restaurado al backup previo)"
                except OSError as exc:
                    error += f" (ADEMAS fallo la restauracion del backup: {exc})"
            icon.icon = ICONS["error"]
            log(f"Jupyter con errores: {etiqueta}: {error}")
        else:
            icon.icon = ICONS["warning"] if huecos else ICONS["ok"]
            log(
                f"Jupyter completado con exito ({len(_rj3c_summary)} ejercicio(s) para ver "
                f"con Ctrl+Alt+N/B){aviso_huecos}."
            )
    except Exception as exc:
        icon.icon = ICONS["error"]
        log(f"ERROR Jupyter: {exc}")
    finally:
        _busy.clear()


def verificar_task(icon: Any) -> None:
    """Boton "V" (Verificar): corre SOLO _verificar_notebook_independiente
    (el mismo nbconvert --execute --inplace que ya usan RJ3/RJ3C como
    control cruzado) sobre el notebook real de PRACTICA3_DIR, SIN llamar a
    Claude ni auditar/reescribir nada. Pensado para cuando el usuario edito
    una celda a mano despues de que RJ3/RJ3C ya resolvieron el notebook, y
    solo quiere confirmar rapido si sigue corriendo limpio de punta a
    punta, sin pagar el costo (varios minutos, una llamada a Claude) de una
    corrida completa de RJ3.

    Toma backup antes de verificar igual que RJ3/RJ3C (nbconvert --inplace
    SI modifica el archivo aunque sea solo para grabar los outputs de la
    ejecucion), pero a diferencia de RJ3, si la verificacion encuentra un
    error NO restaura el backup ni corrige nada -- esto es una accion
    puramente de diagnostico: si el usuario edito el notebook a mano y la
    verificacion da error, ese error es justamente lo que vino a ver, no
    algo para deshacer solo. La unica senal de resultado es el color del
    icono (verde/rojo), sin mensajes aparte."""
    try:
        files = find_jupyter_files()
        if not files:
            icon.icon = ICONS["info"]
            log("Verificar: sin notebooks en PRACTICA3_DIR.")
            return
        if len(files) > 1:
            log(f"Verificar: hay {len(files)} notebooks en PRACTICA3_DIR, se usa el primero: {files[0]}")
        path = files[0]
        etiqueta = os.path.basename(path)

        _backup_notebook(path)
        log(f"Verificar: corriendo nbconvert sobre {etiqueta}...")
        error_verificacion = _verificar_notebook_independiente(path)
        if error_verificacion:
            icon.icon = ICONS["error"]
            log(f"Verificar: {etiqueta} tiene errores: {error_verificacion[:300]}")
        else:
            icon.icon = ICONS["ok"]
            log(f"Verificar: {etiqueta} corre limpio de punta a punta.")
    except Exception as exc:
        icon.icon = ICONS["error"]
        log(f"ERROR Verificar: {exc}")
    finally:
        _busy.clear()


def on_resolver(icon: Any, item) -> None:
    _start_task(icon, manual_task)


def on_resolver_jupyter(icon: Any, item) -> None:
    _start_task(icon, resolve_jupyter_task)


def on_repasar(icon: Any, item) -> None:
    _start_task(icon, repasar_task)


def on_rj3c(icon: Any, item) -> None:
    _start_task(icon, rj3c_task)


def on_apply_n2(icon: Any, item) -> None:
    _start_task(icon, apply_n2_task)


def n2_disponible(item) -> bool:
    return _last_context is not None


def on_verificar(icon: Any, item) -> None:
    _start_task(icon, verificar_task)


def on_quit(icon: Any, item) -> None:
    icon.stop()


# Limite general del tooltip de la bandeja (szTip = 128 WCHAR incluyendo el
# terminador nulo): pystray lanza "string too long" si se supera, lo que hacia
# fallar REPASAR despues de terminar el analisis (ej. lista larga de huecos).
TOOLTIP_MAX_CHARS = 127


def _recortar_tooltip(texto: str) -> str:
    texto = texto or ""
    if len(texto) <= TOOLTIP_MAX_CHARS:
        return texto
    return texto[: TOOLTIP_MAX_CHARS - 3] + "..."


def _aviso_huecos(huecos: list, etiqueta: str) -> str:
    """Aviso compacto de huecos para el tooltip: muestra como mucho 8 numeros."""
    if not huecos:
        return ""
    lista = ", ".join(map(str, huecos[:8])) + (", ..." if len(huecos) > 8 else "")
    return f" -- OJO, faltan {len(huecos)} {etiqueta}: {lista}"


class _SafeTitleIcon(pystray.Icon):  # type: ignore[misc, valid-type]
    """pystray.Icon cuyo title se recorta solo al limite de Windows."""

    @property
    def title(self):  # type: ignore[override]
        return self._title

    @title.setter
    def title(self, value):  # type: ignore[override]
        value = _recortar_tooltip(value)
        if value != self._title:
            self._title = value
            if self.visible:
                self._update_title()


def main() -> None:
    if not _acquire_single_instance_lock():
        log("Ya hay una instancia corriendo, se cierra esta en silencio.")
        return

    os.makedirs(PREGUNTAS_DIR, exist_ok=True)
    os.makedirs(REPASAR_DIR, exist_ok=True)
    os.makedirs(MANUAL_DIR, exist_ok=True)
    image = Image.open(LOGO_PATH)
    load_status_icons(image)
    ####cambio de nombre
    menu = pystray.Menu(
        pystray.MenuItem("Manual N1", on_resolver, default=True),
        pystray.MenuItem("CAR", on_repasar),
        pystray.MenuItem("Aplicar N2 (opcional)", on_apply_n2, enabled=n2_disponible),  # type: ignore[reportArgumentType]
        pystray.MenuItem("RJ3", on_resolver_jupyter),
        pystray.MenuItem("RJ3C", on_rj3c),
        pystray.MenuItem("V", on_verificar),
        pystray.MenuItem("Salir", on_quit),
    )

    icon = _SafeTitleIcon("repasar_matematica", ICONS["idle"], "Analizando archivos...", menu)

    threading.Thread(target=_hotkey_watcher, args=(icon,), daemon=True).start()
    log(
        f"Vigilancia de atajos por sondeo iniciada: {HOTKEY} / {REVIEW_HOTKEY} / "
        f"{RJ3C_NEXT_HOTKEY} / {RJ3C_PREV_HOTKEY} (+ doble clic en botones laterales del mouse)"
    )

    # Al arrancar, procesa automaticamente lo que haya en MANUAL.
    _start_task(icon, manual_task)

    icon.run()


if __name__ == "__main__":
    main()

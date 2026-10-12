"""
App de bandeja del sistema (sin ventana de consola) que analiza archivos
con Claude Code.

- Solo lee archivos (PDF o imagen: png/jpg/jpeg/webp/bmp) que esten dentro
  de la carpeta PREGUNTAS (al lado de este script / del .exe).
- Mientras procesa, el icono de la bandeja cambia de color (sin lanzar
  notificaciones de Windows) para indicar el estado.
- Al terminar, guarda el resultado en t.txt junto con los archivos que lo
  originaron (en PREGUNTAS/procesado o en la carpeta REPASAR de la sesion).
- No abre ninguna ventana de CMD (compilar con --windowed).
"""

import os
import re
import sys
import glob
import shutil
import subprocess
import threading
import time
import ctypes
import concurrent.futures
from typing import Any

from PIL import Image, ImageGrab, ImageChops, ImageDraw
import pystray  # type: ignore[import-untyped]

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PREGUNTAS_DIR = os.path.join(BASE_DIR, "PREGUNTAS")
PROCESADO_DIR = os.path.join(PREGUNTAS_DIR, "procesado")
REPASAR_DIR = os.path.join(BASE_DIR, "REPASAR")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
LOG_FILE = os.path.join(BASE_DIR, "app.log")

ANSWER_FILENAME = "t.txt"
ANSWER_FILENAME_N2 = "t_n2.txt"

VALID_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".webp", ".bmp")

HOTKEY = "ctrl+alt+r"
REVIEW_HOTKEY = "ctrl+alt+9"  # avanza una pregunta/respuesta por pulsacion en el tooltip
HOTKEY_POLL_SECONDS = 0.05  # frecuencia de sondeo del estado fisico de las teclas
VK_CONTROL = 0x11
VK_MENU = 0x12  # Alt
VK_R = 0x52
VK_9 = 0x39
# Botones laterales del mouse como disparador alternativo: cuando el foco
# esta sobre una maquina virtual (VirtualBox, etc.) el teclado se captura
# a nivel de driver para el invitado y ningun atajo de teclado del host
# (ni por hook ni por sondeo de estado) llega a verse, pero los clics de
# mouse si pasan con normalidad.
VK_XBUTTON1 = 0x05  # boton lateral "atras" -> igual que Ctrl+Alt+R
VK_XBUTTON2 = 0x06  # boton lateral "adelante" -> igual que Ctrl+Alt+9
CAPTURE_INTERVAL_SECONDS = 1.0
SCROLL_WHEEL_DELTA = -360  # negativo = hacia abajo
MOUSEEVENTF_WHEEL = 0x0800
MAX_CAPTURES = 60  # limite de seguridad si la pagina nunca deja de cambiar
STILL_FRAMES_TO_STOP = 2  # capturas seguidas sin cambios para asumir que llego al final
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
# bien, rojo si hubo error, gris para "nada que hacer".
COLOR_BUSY = (243, 156, 18, 255)
COLOR_OK = (39, 174, 96, 255)
COLOR_ERROR = (192, 57, 43, 255)
COLOR_INFO = (127, 140, 141, 255)

ICONS = {}

PROMPT_TEMPLATE = """Eres un experto en matematicas para IA. Lee con la herramienta Read
cada uno de estos archivos (son las preguntas de un examen, en PDF y/o
imagen, posiblemente repartidas en varios archivos/paginas):

{file_list}

{question_structure_note}

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

PROMPT_TEMPLATE_REPASAR = """Eres un experto en matematicas para IA. Lee con la herramienta Read
cada una de estas imagenes, en el orden dado (son partes consecutivas
de una misma pagina de preguntas; puede haber contenido repetido entre
imagenes consecutivas por el solapamiento):

{file_list}

{question_structure_note}

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


def log(message: str) -> None:
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except OSError:
        pass


def find_question_files() -> list:
    if not os.path.isdir(PREGUNTAS_DIR):
        os.makedirs(PREGUNTAS_DIR, exist_ok=True)
        return []
    files = []
    for path in sorted(glob.glob(os.path.join(PREGUNTAS_DIR, "*"))):
        if os.path.isfile(path) and path.lower().endswith(VALID_EXTENSIONS):
            files.append(path)
    return files


SUMMARY_LINE_RE = re.compile(r"^\s*(\d{1,3})\s*\|\s*(.{1,40}?)\s*$")


def parse_summary(respuesta: str) -> list:
    """Extrae pares (numero, respuesta) de la tabla resumen final ('N |
    respuesta') que se le pide a Claude en el prompt, para mostrarlos en
    el submenu "Ver" sin tener que abrir t.txt."""
    pares = []
    for linea in respuesta.splitlines():
        m = SUMMARY_LINE_RE.match(linea)
        if m:
            pares.append((m.group(1), m.group(2)))
    return pares


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
    ordenada por numero de pregunta, sin duplicar numeros repetidos (pueden
    repetirse por el solapamiento entre lotes; se conserva la primera
    aparicion)."""
    vistos = {}
    for pares in pares_por_lote:
        for numero, resp in pares:
            vistos.setdefault(numero, resp)
    try:
        return sorted(vistos.items(), key=lambda par: int(par[0]))
    except ValueError:
        return list(vistos.items())


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
        return
    if _review_index >= len(_last_summary):
        icon.title = "Repaso completo"
        _review_index = 0
        return
    numero, resp = _last_summary[_review_index]
    icon.title = f"tuhxqwdq{numero}: {resp}"
    _review_index += 1


def _key_down(vk: int) -> bool:
    return bool(ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000)


def _hotkey_watcher(icon: Any) -> None:
    """Sondea el estado fisico de las teclas en vez de usar un hook global
    de teclado: dentro de una maquina virtual, el software de VM instala
    su propio hook para reenviar las teclas al huesped y puede "tragarse"
    el evento antes de que un hook de otra app (como el que usaba la
    libreria keyboard) llegue a verlo, aunque la tecla si se presiono en
    el host. GetAsyncKeyState lee el estado real de la tecla y no depende
    de esa cadena de hooks, asi que el atajo sigue funcionando aunque el
    foco este sobre la ventana de la VM."""
    r_was_down = False
    nine_was_down = False
    mouse_back_was_down = False
    mouse_fwd_was_down = False
    while True:
        mods_down = _key_down(VK_CONTROL) and _key_down(VK_MENU)
        r_down = mods_down and _key_down(VK_R)
        nine_down = mods_down and _key_down(VK_9)
        mouse_back_down = _key_down(VK_XBUTTON1)
        mouse_fwd_down = _key_down(VK_XBUTTON2)

        if (r_down and not r_was_down) or (mouse_back_down and not mouse_back_was_down):
            _start_task(icon, repasar_task)
        if (nine_down and not nine_was_down) or (mouse_fwd_down and not mouse_fwd_was_down):
            on_review_next(icon)

        r_was_down = r_down
        nine_was_down = nine_down
        mouse_back_was_down = mouse_back_down
        mouse_fwd_was_down = mouse_fwd_down
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
    for name in ("claude.cmd", "claude.exe", "claude"):
        path = shutil.which(name)
        if path:
            return path
    raise FileNotFoundError("No se encontro el CLI de Claude Code en el PATH.")


def ask_claude(prompt: str, allowed_dir: str, effort: str) -> str:
    claude_path = find_claude_executable()
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    result = subprocess.run(
        [claude_path, "--print", "--allowedTools", "Read", "--add-dir", allowed_dir, "--effort", effort],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=900,
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
_last_summary = []  # lista (numero, respuesta) del ultimo analisis, para el submenu "Ver"
_review_index = 0  # cuantas preguntas ya se mostraron con ctrl+alt+9 del ultimo analisis
_instance_mutex = None  # handle del mutex de instancia unica (debe seguir vivo todo el proceso)


def _start_task(icon: Any, task_fn) -> None:
    if _busy.is_set():
        log("Solicitud ignorada: ya hay un analisis en curso.")
        return
    _busy.set()
    icon.icon = ICONS["busy"]
    threading.Thread(target=task_fn, args=(icon,), daemon=True).start()


def _scroll_down() -> None:
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, SCROLL_WHEEL_DELTA, 0)


def _same_image(img_a: Image.Image, img_b: Image.Image) -> bool:
    if img_a.size != img_b.size:
        return False
    diff = ImageChops.difference(img_a.convert("RGB"), img_b.convert("RGB"))
    return diff.getbbox() is None


def _capture_pages(session_dir: str) -> list:
    """Se desplaza hacia abajo tomando una imagen por cada parte nueva de la
    pagina, hasta que ya no detecta cambios (fin de la pagina)."""
    files = []
    index = 0
    previous_shot = None
    no_change_streak = 0

    for _ in range(MAX_CAPTURES):
        shot = ImageGrab.grab()

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
        time.sleep(CAPTURE_INTERVAL_SECONDS * 0.4)
        _scroll_down()
        time.sleep(CAPTURE_INTERVAL_SECONDS * 0.6)

    return files


def _run_batches(icon: Any, lotes: list, template: str, allowed_dir: str, effort: str, status_prefix: str) -> tuple:
    """Ejecuta `ask_claude` una vez por lote de `lotes` (listas de rutas de
    archivo), en paralelo (hasta MAX_PARALLEL_BATCHES a la vez) para que una
    sesion con varios lotes no tarde N veces mas que una sola llamada. Si un
    lote falla, se loguea y se continua con el resto en vez de perder todo
    el analisis; solo se propaga el error si TODOS los lotes fallan.
    Devuelve (respuesta_final, resumen_pares, errores), respetando el orden
    original de los lotes en el resultado aunque terminen en otro orden."""
    n = len(lotes)
    resultados = [None] * n
    titulo_lock = threading.Lock()
    completados = 0

    def procesar_lote(i: int, lote: list) -> tuple:
        etiqueta = f"lote {i}/{n}" if n > 1 else "N1"
        log(f"{status_prefix} {etiqueta}: iniciando ({len(lote)} imagen(es))")

        file_list = "\n".join(f"- {p}" for p in lote)
        prompt = template.format(file_list=file_list, question_structure_note=QUESTION_STRUCTURE_NOTE)
        try:
            respuesta = ask_claude(prompt, allowed_dir, effort)
        except Exception as exc:
            log(f"ERROR {status_prefix} {etiqueta}: {exc}")
            return etiqueta, "error", str(exc)

        log(f"{status_prefix} {etiqueta}: terminado ({len(respuesta)} caracteres)")
        return etiqueta, "ok", respuesta

    icon.title = f"{status_prefix} ({n} lote(s) en paralelo)..." if n > 1 else f"{status_prefix}..."
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(n, MAX_PARALLEL_BATCHES)) as executor:
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
    for etiqueta, estado, contenido in resultados:
        if estado == "ok":
            respuestas.append(contenido if n == 1 else f"--- {etiqueta} ---\n{contenido}")
            pares_por_lote.append(parse_summary(contenido))
        else:
            errores.append(f"[{etiqueta}: ERROR - {contenido}]")

    if not respuestas:
        raise RuntimeError("Todos los lotes fallaron:\n" + "\n".join(errores))

    respuesta_final = "\n\n".join(respuestas + errores)
    return respuesta_final, merge_summaries(pares_por_lote), errores


def repasar_task(icon: Any) -> None:
    session_dir = os.path.join(REPASAR_DIR, "REPASAR_" + time.strftime("%Y%m%d_%H%M%S"))
    os.makedirs(session_dir, exist_ok=True)

    icon.title = f"REPASAR: posiciona el mouse ({START_DELAY_SECONDS}s)..."
    log(f"Iniciando REPASAR en {session_dir}")
    time.sleep(START_DELAY_SECONDS)

    icon.title = "REPASAR: leyendo pantalla..."

    try:
        files = _capture_pages(session_dir)
        if not files:
            icon.icon = ICONS["info"]
            icon.title = "REPASAR: sin contenido"
            log("REPASAR sin imagenes, se cancela.")
            return

        log(f"REPASAR analizando {len(files)} imagen(es) en {session_dir}")
        lotes = chunk_files(files, overlap=BATCH_OVERLAP_REPASAR)

        respuesta_final, resumen, errores = _run_batches(
            icon, lotes, PROMPT_TEMPLATE_REPASAR, session_dir, EFFORT_N1, "REPASAR: analizando"
        )

        output_path = os.path.join(session_dir, ANSWER_FILENAME)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(respuesta_final)

        global _last_context, _last_summary, _review_index
        _last_context = {
            "lotes": lotes,
            "template": PROMPT_TEMPLATE_REPASAR,
            "allowed_dir": session_dir,
            "output_dir": session_dir,
        }
        _last_summary = resumen
        _review_index = 0
        icon.update_menu()

        if errores:
            estado = f"N1 aplicado con errores en {len(errores)}/{len(lotes)} lote(s)"
            icon.icon = ICONS["error"]
        else:
            estado = "N1 aplicado (REPASAR)"
            icon.icon = ICONS["ok"]
        icon.title = estado
        log(f"{estado}: {output_path}")
    except Exception as exc:
        icon.icon = ICONS["error"]
        icon.title = "REPASAR: error"
        log(f"ERROR REPASAR: {exc}")
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

        respuesta_final, resumen, errores = _run_batches(
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


def apply_n2_task(icon: Any) -> None:
    try:
        if _last_context is None:
            icon.icon = ICONS["info"]
            icon.title = "N2: primero ejecuta N1"
            return

        log("Iniciando N2 (xhigh)")

        respuesta_final, resumen, errores = _run_batches(
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

        global _last_summary, _review_index
        _last_summary = resumen
        _review_index = 0
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


def on_resolver(icon: Any, item) -> None:
    _start_task(icon, resolve_task)


def on_repasar(icon: Any, item) -> None:
    _start_task(icon, repasar_task)


def on_apply_n2(icon: Any, item) -> None:
    _start_task(icon, apply_n2_task)


def n2_disponible(item) -> bool:
    return _last_context is not None


def _ver_items():
    if not _last_summary:
        yield pystray.MenuItem("(sin resultados aun)", None, enabled=False)
        return
    for numero, resp in _last_summary:
        yield pystray.MenuItem(f"{numero}: {resp}", None, enabled=False)


def on_quit(icon: Any, item) -> None:
    icon.stop()


def main() -> None:
    if not _acquire_single_instance_lock():
        log("Ya hay una instancia corriendo, se cierra esta en silencio.")
        return

    os.makedirs(PREGUNTAS_DIR, exist_ok=True)
    os.makedirs(REPASAR_DIR, exist_ok=True)
    image = Image.open(LOGO_PATH)
    load_status_icons(image)

    menu = pystray.Menu(
        pystray.MenuItem("Manual N1", on_resolver, default=True),
        pystray.MenuItem("Iniciar REPASAR (Ctrl+Alt+R)", on_repasar),
        pystray.MenuItem("Aplicar N2 (opcional)", on_apply_n2, enabled=n2_disponible),  # type: ignore[reportArgumentType]
        pystray.MenuItem("Ver", pystray.Menu(_ver_items)),
        pystray.MenuItem("Salir", on_quit),
    )

    icon = pystray.Icon("repasar_matematica", ICONS["idle"], "Analizando archivos...", menu)

    threading.Thread(target=_hotkey_watcher, args=(icon,), daemon=True).start()
    log(f"Vigilancia de atajos por sondeo iniciada: {HOTKEY} / {REVIEW_HOTKEY} (+ botones laterales del mouse)")

    # Al arrancar, procesa automaticamente lo que haya en PREGUNTAS.
    _start_task(icon, resolve_task)

    icon.run()


if __name__ == "__main__":
    main()

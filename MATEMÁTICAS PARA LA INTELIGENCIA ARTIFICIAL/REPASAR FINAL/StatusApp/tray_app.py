"""
Indicador de estado en la bandeja del sistema (system tray).

- AMARILLO  -> tarea en curso ("working")
- VERDE     -> tarea completada al 100% ("done")
- GRIS      -> sin tarea iniciada / archivo de estado ausente ("idle")

El icono se actualiza leyendo periodicamente un archivo de texto plano
(status.txt) que otro proceso (worker.py, o cualquier script tuyo)
va escribiendo con una de estas palabras: working / done / idle.

Pensado para compilarse a .exe con PyInstaller y ejecutarse en segundo
plano (sin ventana de consola).
"""

import os
import sys
import time
import threading

from PIL import Image, ImageDraw
import pystray

# Carpeta donde vive este script (o el .exe generado por PyInstaller)
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATUS_FILE = os.path.join(BASE_DIR, "status.txt")
POLL_SECONDS = 1.5

COLORS = {
    "working": (255, 200, 0),    # amarillo
    "done": (40, 170, 60),       # verde
    "idle": (150, 150, 150),     # gris
    "error": (200, 40, 40),      # rojo (por si el worker falla)
}

LABELS = {
    "working": "Resolviendo examen... (en curso)",
    "done": "Examen resuelto al 100%",
    "idle": "Sin tarea en curso",
    "error": "Error al procesar la tarea",
}


def read_status() -> str:
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            value = f.read().strip().lower()
        if value not in COLORS:
            return "idle"
        return value
    except FileNotFoundError:
        return "idle"
    except OSError:
        return "idle"


def make_icon_image(color: tuple) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = 6
    draw.ellipse(
        (margin, margin, size - margin, size - margin),
        fill=color,
        outline=(30, 30, 30, 255),
        width=3,
    )
    return img


def run_tray():
    current_status = {"value": None}

    icon = pystray.Icon(
        "status_indicator",
        make_icon_image(COLORS["idle"]),
        LABELS["idle"],
    )

    def poll_loop():
        while True:
            status = read_status()
            if status != current_status["value"]:
                current_status["value"] = status
                icon.icon = make_icon_image(COLORS[status])
                icon.title = LABELS[status]
            time.sleep(POLL_SECONDS)

    def on_quit(icon_obj, item):
        icon_obj.stop()

    icon.menu = pystray.Menu(
        pystray.MenuItem(lambda item: LABELS[current_status["value"] or "idle"], None, enabled=False),
        pystray.MenuItem("Salir", on_quit),
    )

    threading.Thread(target=poll_loop, daemon=True).start()
    icon.run()


if __name__ == "__main__":
    run_tray()

"""
Worker: extrae el texto del PDF del examen, se lo envia a Claude Code
(en modo no interactivo, `claude --print`) para que lo resuelva, y
guarda la respuesta en un archivo .txt.

Mientras se ejecuta escribe "working" en status.txt (el indicador de
bandeja tray_app.py lo pinta en AMARILLO). Al terminar con exito
escribe "done" (VERDE). Si algo falla, escribe "error" (ROJO).

Uso:
    python worker.py "ruta\\al\\examen.pdf"

Si no se indica ruta, usa por defecto el PDF del examen que esta un
nivel por encima de esta carpeta (../Sep15-Examen-1a-Convocatoria.pdf).
"""

import os
import shutil
import subprocess
import sys

import fitz  # PyMuPDF

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATUS_FILE = os.path.join(BASE_DIR, "status.txt")

DEFAULT_PDF = os.path.join(BASE_DIR, "..", "Sep15-Examen-1a-Convocatoria.pdf")
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "..", "Respuestas_Claude.txt")

PROMPT_TEMPLATE = """Eres un experto en matematicas para IA. A continuacion tienes el
texto completo de un examen (extraido de un PDF). Resuelve TODAS las
preguntas, una por una, mostrando el razonamiento breve y terminando
cada una con "Respuesta: <resultado>". Al final incluye una tabla
resumen "numero de pregunta -> respuesta final". Usa coma decimal
donde el enunciado lo pida. Responde en texto plano (sin markdown de
tablas complejas), listo para guardarse en un .txt.

--- TEXTO DEL EXAMEN ---
{exam_text}
--- FIN DEL TEXTO ---
"""


def set_status(value: str) -> None:
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(value)


def extract_pdf_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    try:
        return "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()


def find_claude_executable() -> str:
    """Localiza el ejecutable de Claude Code de forma robusta en Windows."""
    for name in ("claude.cmd", "claude.exe", "claude"):
        path = shutil.which(name)
        if path:
            return path
    raise FileNotFoundError(
        "No se encontro el CLI de Claude Code en el PATH. "
        "Instalalo con: npm install -g @anthropic-ai/claude-code"
    )


def ask_claude(prompt: str) -> str:
    claude_path = find_claude_executable()
    # El prompt se envia por stdin (no como argumento) porque el examen
    # completo puede superar el limite de longitud de linea de comandos
    # de Windows (~8191 caracteres) y truncarse silenciosamente.
    result = subprocess.run(
        [claude_path, "--print"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=600,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude --print devolvio codigo {result.returncode}:\n{result.stderr}"
        )
    return result.stdout.strip()


def do_task(pdf_path: str, output_path: str) -> None:
    print(f"Leyendo PDF: {pdf_path}")
    exam_text = extract_pdf_text(pdf_path)

    print("Enviando el examen a Claude Code para resolverlo...")
    prompt = PROMPT_TEMPLATE.format(exam_text=exam_text)
    respuesta = ask_claude(prompt)

    print(f"Guardando respuestas en: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(respuesta)


def main() -> None:
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

    set_status("working")
    try:
        do_task(pdf_path, output_path)
    except Exception as exc:
        set_status("error")
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
    else:
        set_status("done")
        print("Listo. Examen resuelto al 100%.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Integración con Claude Code CLI (headless) para el botón "🤖 Explícamelo"
del Reto de código: le pide a Claude una explicación corta del último error
del alumno, usando la sesión de la suscripción de la CLI (no una API key
medida por token). Consumido por la ruta `/explain_error`."""
import sys
import os as _os
import shutil as _shutil
import tempfile as _tempfile
import subprocess as _subprocess
import json as _json


# ── Reto de código: explicación de errores con Claude Code (headless) ──
# Usa la suscripción de Claude Code (claude -p, misma sesión OAuth de la CLI)
# en vez de una API key medida por token — así el alumno no paga aparte.
# CLAUDE_CODE_EXECPATH lo exporta la propia CLI cuando está instalada; si no
# está, caemos a "claude" y confiamos en el PATH.
CLAUDE_BIN = _os.environ.get('CLAUDE_CODE_EXECPATH') or _shutil.which('claude') or 'claude'
CLAUDE_EXPLAIN_TIMEOUT_SECS = 30
CLAUDE_EXPLAIN_MODEL = 'claude-haiku-4-5-20251001'  # rápido y barato, de sobra para una pista corta
# Carpeta de trabajo aislada y vacía para el subproceso: sin esto, la CLI
# auto-descubriría el CLAUDE.md/memoria de ESTE proyecto y los inyectaría en
# cada llamada, disparando el consumo de tokens para una simple pista.
_CLAUDE_EXPLAIN_CWD = _tempfile.mkdtemp(prefix='pyviz_ai_')

CLAUDE_TUTOR_SYSTEM_PROMPT = (
    "Eres un profesor de Python que corrige el intento de un alumno en un "
    "ejercicio guiado. Te paso el error de Python y unas pocas líneas de "
    "código alrededor de la línea que falló (no el archivo completo). "
    "Responde SIEMPRE en español, sin markdown, en como máximo 4 líneas, "
    "con este formato exacto:\n"
    "CAUSA: <por qué falla, una frase corta>\n"
    "LINEA: <qué está mal específicamente en esa línea>\n"
    "SOLUCION: <cómo arreglarlo, con el cambio de código concreto>\n"
    "No repitas el traceback ni saludes ni agregues nada fuera de esas 3 líneas."
)


def _error_window(code, error_line, radius=3):
    """Recorta el código a unas pocas líneas alrededor del error (con número
    de línea) en vez de mandar el archivo completo al modelo — el motivo
    principal por el que esta llamada gasta pocos tokens."""
    lines = code.split('\n')
    if not error_line or error_line < 1 or error_line > len(lines) or len(lines) <= 2 * radius + 2:
        return '\n'.join(f'{i+1}: {ln}' for i, ln in enumerate(lines))
    start, end = max(1, error_line - radius), min(len(lines), error_line + radius)
    out = []
    for i in range(start, end + 1):
        mark = '  <-- esta línea falla' if i == error_line else ''
        out.append(f'{i}: {lines[i-1]}{mark}')
    return '\n'.join(out)


CLAUDE_PATTERN_SYSTEM_PROMPT = (
    "Eres un tutor que analiza el HISTORIAL de respuestas de un alumno en un "
    "bloque de temas relacionados de un curso. Te paso una lista de intentos "
    "recientes, cada uno con: tema, si acertó o falló, qué otra opción dudó "
    "(si alguna) y el motivo que el alumno marcó (por botones: sabía la "
    "teoría / descartó por eliminación / dudó entre dos / adivinó / confundió "
    "conceptos). Tu trabajo es detectar UN patrón de confusión recurrente y "
    "concreto (no resumas los datos, no los repitas). "
    "Responde SIEMPRE en español, sin markdown, en máximo 3 líneas, "
    "directo y específico (por ejemplo: nombra los dos conceptos que confunde "
    "si eso es lo que ves). Si los datos son demasiado dispersos para ver un "
    "patrón claro, dilo en una sola línea en vez de inventar uno."
)


def _claude_analyze_patterns(familia, mode, signal_rows):
    """Le pide a Claude Code (headless, mismo mecanismo que _claude_explain_error)
    que diagnostique un patrón de confusión recurrente a partir del historial
    de motivos/opciones dudadas de un bloque de temas débiles -- se llama solo
    cuando ya hay señal acumulada suficiente (ver /analyze_patterns en la
    ruta Flask), no por cada pregunta."""
    lines = []
    for r in signal_rows:
        doubt = f", dudó con: {r['doubted']}" if r.get('doubted') else ''
        lines.append(f"- {r['topic']} | resultado: {r['result']} | motivo: {r['reason_tag']}{doubt}")
    user_prompt = f"Bloque de temas: {familia} (curso: {mode})\n\nHistorial reciente:\n" + '\n'.join(lines) + '\n'
    cmd = [CLAUDE_BIN, '-p', '--output-format', 'json',
           '--model', CLAUDE_EXPLAIN_MODEL,
           '--tools', '',
           '--no-session-persistence',
           '--strict-mcp-config',
           '--system-prompt', CLAUDE_PATTERN_SYSTEM_PROMPT]
    run_kwargs = {}
    if sys.platform == 'win32':
        run_kwargs['creationflags'] = _subprocess.CREATE_NO_WINDOW
    try:
        proc = _subprocess.run(cmd, input=user_prompt, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', cwd=_CLAUDE_EXPLAIN_CWD,
                                timeout=CLAUDE_EXPLAIN_TIMEOUT_SECS, **run_kwargs)
    except _subprocess.TimeoutExpired:
        return {'ok': False, 'diagnosis': f'Claude tardó más de {CLAUDE_EXPLAIN_TIMEOUT_SECS}s en responder — probá de nuevo.'}
    except FileNotFoundError:
        return {'ok': False, 'diagnosis': 'No se encontró el CLI de Claude Code (claude) en este equipo.'}
    raw = (proc.stdout or '').strip()
    text = raw
    try:
        parsed = _json.loads(raw)
        text = (parsed.get('result') or text).strip()
    except (ValueError, AttributeError, TypeError):
        pass
    if proc.returncode != 0 and not text:
        return {'ok': False, 'diagnosis': f'Claude Code devolvió un error: {(proc.stderr or "").strip()[:300]}'}
    return {'ok': True, 'diagnosis': text}


def _claude_explain_error(code, error_text, error_line):
    """Le pide a Claude Code (headless, -p) una explicación corta del error.
    Usa la sesión de la suscripción de la CLI (no una API key por token):
    --tools "" quita las definiciones de herramientas del prompt, --system-prompt
    reemplaza el system prompt por defecto (evita CLAUDE.md/memoria/instrucciones
    de agente) y cwd apunta a una carpeta vacía para que no auto-descubra el
    CLAUDE.md de este proyecto — todo para minimizar tokens de entrada."""
    snippet = _error_window(code, error_line)
    user_prompt = f"Error de Python:\n{error_text}\n\nCódigo (con número de línea):\n{snippet}\n"
    cmd = [CLAUDE_BIN, '-p', '--output-format', 'json',
           '--model', CLAUDE_EXPLAIN_MODEL,
           '--tools', '',
           '--no-session-persistence',
           '--strict-mcp-config',
           '--system-prompt', CLAUDE_TUTOR_SYSTEM_PROMPT]
    run_kwargs = {}
    if sys.platform == 'win32':
        run_kwargs['creationflags'] = _subprocess.CREATE_NO_WINDOW
    try:
        proc = _subprocess.run(cmd, input=user_prompt, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', cwd=_CLAUDE_EXPLAIN_CWD,
                                timeout=CLAUDE_EXPLAIN_TIMEOUT_SECS, **run_kwargs)
    except _subprocess.TimeoutExpired:
        return {'ok': False, 'explanation': f'Claude tardó más de {CLAUDE_EXPLAIN_TIMEOUT_SECS}s en responder — probá de nuevo.'}
    except FileNotFoundError:
        return {'ok': False, 'explanation': 'No se encontró el CLI de Claude Code (claude) en este equipo.'}
    raw = (proc.stdout or '').strip()
    text, usage = raw, None
    try:
        parsed = _json.loads(raw)
        text = (parsed.get('result') or text).strip()
        usage = parsed.get('usage')
    except (ValueError, AttributeError, TypeError):
        pass
    if proc.returncode != 0 and not text:
        return {'ok': False, 'explanation': f'Claude Code devolvió un error: {(proc.stderr or "").strip()[:300]}'}
    return {'ok': True, 'explanation': text, 'error_line': error_line, 'usage': usage}

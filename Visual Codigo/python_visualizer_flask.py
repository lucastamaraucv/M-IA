#!/usr/bin/env python3
"""Python Debugger Visual — VS Code style, Flask backend.

Punto de entrada delgado: solo configuración de Flask y las 4 rutas. La
lógica pesada vive en módulos aparte (narrator.py, sandbox.py, challenge.py,
ai_tutor.py) y el frontend en templates/index.html + static/ — separados así
para que una mejora a un solo Modo Maestro no requiera tener presente todo
el archivo (antes >6700 líneas en uno solo)."""

from flask import Flask, render_template, request, jsonify, url_for
import multiprocessing as _mp
import queue as _queue_mod
import time as _time
import os as _os
import logging as _logging
from logging.handlers import RotatingFileHandler as _RotatingFileHandler

# Force a non-interactive backend BEFORE any user code can import matplotlib.
# Without this, a user's plt.show() opens (or tries to open) a GUI window and
# blocks the request thread forever — the browser just sits on "Analizando…"
# with no way to recover. Agg makes show()/FuncAnimation no-ops: the plotting
# calls still run (so class/data logic still traces normally) but nothing
# tries to actually render a window this web debugger can't display anyway.
try:
    import matplotlib as _mpl
    _mpl.use('Agg', force=True)
except ImportError:
    pass

from narrator import _find_relations, _explain_lines
from sandbox import _run_user_code, _json_safe
from challenge import _build_challenge
from ai_tutor import _claude_explain_error, _claude_analyze_patterns
from notes_store import save_note, list_notes
from error_journal_store import save_error, list_errors, update_personal_rule
from stats_store import (record_attempt, record_confidence, record_reasoning,
                          get_reasoning_signal, get_report, get_trend, get_streak)

app = Flask(__name__)
app.json.sort_keys = False  # preserve dict insertion order in JSON responses
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # don't let Flask tell the browser to cache statics long-term

# Log centralizado de errores del backend (app.log, ya en .gitignore vía
# "*.log"): además de los pageerror/console.error que ya captura Playwright
# (ver verify/e2e_browser_test.js) en el lado navegador, esto guarda en disco
# las excepciones del lado servidor -- tanto las que YA se atrapan dentro de
# cada ruta (return jsonify({'ok': False, ...}), antes se perdían en la
# terminal) como las verdaderamente no manejadas (500). Rota a los 2 MB para
# no crecer sin límite. logging.captureWarnings además manda aquí los
# warnings de Python (DeprecationWarning, etc.), no solo excepciones.
_log_handler = _RotatingFileHandler(
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'app.log'),
    maxBytes=2 * 1024 * 1024, backupCount=3, encoding='utf-8')
_log_handler.setFormatter(_logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s'))
_logging.getLogger().addHandler(_log_handler)
_logging.getLogger().setLevel(_logging.WARNING)
app.logger.setLevel(_logging.WARNING)
_logging.captureWarnings(True)

EXEC_TIMEOUT_SECS = 12  # wall-clock safety net for blocking calls MAX_STEPS can't catch
                        # (time.sleep(), a stuck join(), network I/O, a GUI call that
                        # still blocks despite Agg, etc.)


def _static_v(filename):
    """Cache-busting real: añade ?v=<mtime del archivo> a la URL de un
    estático. Este proyecto edita static/js/*.js constantemente durante el
    desarrollo (cada Modo Maestro nuevo, cada fix) — sin esto, el navegador
    puede seguir sirviendo una versión vieja desde caché incluso tras un
    F5 normal, y un cambio ya aplicado y verificado en el código parece
    "no funcionar" cuando en realidad el navegador nunca llegó a cargarlo.
    Al cambiar el mtime del archivo, la URL cambia, y un navegador SIEMPRE
    pide una URL que no tiene en caché."""
    path = _os.path.join(app.static_folder, filename)
    try:
        v = int(_os.path.getmtime(path))
    except OSError:
        v = 0
    return url_for('static', filename=filename) + f'?v={v}'


app.jinja_env.globals['static_v'] = _static_v


# ── Routes ──────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prepare', methods=['POST'])
def prepare():
    try:
        data = request.json
        code = data.get('code', '')
        if not code.strip():
            return jsonify({'steps': [], 'error': 'Empty code'})

        q = _mp.Queue()
        p = _mp.Process(target=_run_user_code, args=(code, q), daemon=True)
        p.start()

        steps, run_error, final_vars, final_output, done, err_line, truncated = [], None, None, '', False, None, False
        deadline = _time.monotonic() + EXEC_TIMEOUT_SECS
        # Drain the queue as steps stream in, instead of waiting for one big
        # result at the end — this is what lets us keep partial progress
        # even if we have to kill the process below.
        while True:
            remaining = deadline - _time.monotonic()
            if remaining <= 0:
                break
            try:
                msg = q.get(timeout=remaining)
            except _queue_mod.Empty:
                break
            if msg[0] == 'step':
                steps.append(msg[1])
            else:  # 'done'
                _, run_error, final_vars, final_output, err_line, truncated = msg
                done = True
                break

        # Run on a child PROCESS (not a thread) with a hard timeout so a call
        # that blocks the interpreter (time.sleep(), a stuck socket, a GUI
        # call that still blocks despite Agg) can't hang this request forever
        # — and, unlike a thread, a process that doesn't finish in time can
        # actually be killed instead of leaking forever.
        if p.is_alive():
            p.terminate()
            p.join(2)
            if p.is_alive():
                p.kill()
                p.join()
        q.close()

        if not done:
            # También un corte de seguridad, no un bug del alumno -- el
            # proceso seguía vivo, simplemente se agotó el tiempo de pared.
            truncated = True
            run_error = (f'⏱ Tiempo límite de {EXEC_TIMEOUT_SECS}s superado — el código parece '
                         f'bloqueado (p. ej. time.sleep() largo, espera de E/S o red, un hilo '
                         f'atascado). Se muestran los pasos ya registrados.')
            final_output = steps[-1]['output'] if steps else ''

        steps.append({'line': -1, 'frames': [{'name': '<module>', 'line': -1,
                     'variables': final_vars or {}}], 'output': final_output})
        return jsonify(_json_safe({'steps': steps, 'error': run_error, 'error_line': err_line,
                        'truncated': truncated,
                        'relations': _find_relations(code),
                        'explains': _explain_lines(code)}))

    except SyntaxError as e:
        return jsonify({'steps': [], 'error': f'Syntax error line {e.lineno}: {e.msg}', 'error_line': e.lineno})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'steps': [], 'error': f'{type(e).__name__}: {e}'})




@app.route('/explain_error', methods=['POST'])
def explain_error():
    try:
        data = request.json
        code = data.get('code', '')
        error_text = (data.get('error') or '').strip()
        error_line = data.get('error_line')
        if not error_text:
            return jsonify({'ok': False, 'explanation': 'No hay ningún error para explicar.'})
        return jsonify(_json_safe(_claude_explain_error(code, error_text, error_line)))
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'explanation': f'{type(e).__name__}: {e}'})


@app.route('/save_note', methods=['POST'])
def save_note_route():
    try:
        data = request.json
        mode = (data.get('mode') or '').strip()
        topic_idx = data.get('topic_idx')
        topic_name = data.get('topic_name') or ''
        text = data.get('text') or ''
        feedback = data.get('feedback')
        kind = data.get('kind') or 'note'
        note_id = save_note(mode, topic_idx, topic_name, text, feedback, kind)
        if note_id is None:
            return jsonify({'ok': False, 'error': 'Nota vacía, no se guardó nada.'})
        return jsonify({'ok': True, 'id': note_id})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/notes', methods=['GET'])
def notes_route():
    try:
        mode = request.args.get('mode')
        return jsonify(_json_safe(list_notes(mode)))
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/save_error', methods=['POST'])
def save_error_route():
    try:
        data = request.json
        mode = (data.get('mode') or '').strip()
        topic_idx = data.get('topic_idx')
        topic_name = data.get('topic_name') or ''
        question = data.get('question') or ''
        chosen_text = data.get('chosen_text')
        correct_text = data.get('correct_text')
        why_wrong = data.get('why_wrong')
        error_id = save_error(mode, topic_idx, topic_name, question, chosen_text, correct_text, why_wrong)
        if error_id is None:
            return jsonify({'ok': False, 'error': 'Pregunta vacía, no se guardó nada.'})
        return jsonify({'ok': True, 'id': error_id})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/list_errors', methods=['GET'])
def list_errors_route():
    try:
        mode = request.args.get('mode')
        return jsonify(_json_safe(list_errors(mode)))
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/update_error_rule', methods=['POST'])
def update_error_rule_route():
    try:
        data = request.json
        error_id = data.get('id')
        personal_rule = data.get('personal_rule') or ''
        ok = update_personal_rule(error_id, personal_rule)
        return jsonify({'ok': ok})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/record_attempt', methods=['POST'])
def record_attempt_route():
    try:
        data = request.json
        mode = (data.get('mode') or '').strip()
        topic_idx = data.get('topic_idx')
        topic_name = data.get('topic_name') or ''
        result = data.get('result') or ''
        box = data.get('box')
        due_at = data.get('due_at')
        attempt_id = record_attempt(mode, topic_idx, topic_name, result, box, due_at)
        return jsonify({'ok': attempt_id is not None})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/record_confidence', methods=['POST'])
def record_confidence_route():
    try:
        data = request.json
        mode = (data.get('mode') or '').strip()
        topic_idx = data.get('topic_idx')
        level = data.get('level') or ''
        box = data.get('box')
        due_at = data.get('due_at')
        ok = record_confidence(mode, topic_idx, level, box, due_at)
        return jsonify({'ok': ok})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/record_reasoning', methods=['POST'])
def record_reasoning_route():
    try:
        data = request.json
        mode = (data.get('mode') or '').strip()
        topic_idx = data.get('topic_idx')
        doubted_option = data.get('doubted_option')
        reason_tag = data.get('reason_tag') or ''
        ok = record_reasoning(mode, topic_idx, doubted_option, reason_tag)
        return jsonify({'ok': ok})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


# Menos de esta cantidad de intentos con motivo registrado en un bloque no
# es señal suficiente para pedirle un diagnóstico a Claude -- evita una
# llamada al CLI (con su latencia) cuando todavía no hay patrón que ver.
_MIN_REASONING_ROWS_FOR_ANALYSIS = 3


@app.route('/analyze_patterns', methods=['POST'])
def analyze_patterns_route():
    try:
        data = request.json
        mode = (data.get('mode') or '').strip()
        topic_idxs = data.get('topic_idxs') or []
        familia = data.get('familia') or ''
        signal_rows = get_reasoning_signal(mode, topic_idxs)
        if len(signal_rows) < _MIN_REASONING_ROWS_FOR_ANALYSIS:
            return jsonify({'ok': False, 'reason': 'not_enough_data'})
        return jsonify(_json_safe(_claude_analyze_patterns(familia, mode, signal_rows)))
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/stats_report', methods=['GET'])
def stats_report_route():
    try:
        mode = request.args.get('mode')
        return jsonify(_json_safe(get_report(mode)))
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/stats_trend', methods=['GET'])
def stats_trend_route():
    try:
        mode = request.args.get('mode')
        days = request.args.get('days', 14, type=int)
        return jsonify(_json_safe(get_trend(mode, days)))
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/stats_streak', methods=['GET'])
def stats_streak_route():
    try:
        return jsonify({'streak': get_streak()})
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'})


@app.route('/challenge', methods=['POST'])
def challenge():
    try:
        data = request.json
        code = data.get('code', '')
        if not code.strip():
            return jsonify({'challengeable': False})
        return jsonify(_json_safe(_build_challenge(code)))
    except Exception as e:
        app.logger.exception('Error en %s %s', request.method, request.path)
        return jsonify({'challengeable': False, 'error': f'{type(e).__name__}: {e}'})


@app.errorhandler(Exception)
def _handle_unexpected_error(e):
    """Red de seguridad para cualquier excepción que se escape sin pasar por
    el try/except propio de una ruta (las 13 rutas ya tienen el suyo, ver
    arriba) -- sin esto, un error genuinamente inesperado solo se vería como
    una página 500 en el navegador, sin quedar registrado en app.log."""
    app.logger.exception('Excepción no manejada en %s %s', request.method, request.path)
    return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'}), 500


if __name__ == '__main__':
    print('\n  Python Debugger Visual\n  http://localhost:5000\n  Ctrl+C to stop\n')
    app.run(debug=True, port=5000, use_reloader=False, threaded=True)

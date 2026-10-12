#!/usr/bin/env python3
"""Sandbox de ejecución: corre el código del alumno en un proceso aparte
(`_run_user_code`, llamado vía `multiprocessing.Process` desde la ruta
`/prepare`), con `sys.settrace` para capturar un paso por línea, y sanea
NaN/Infinity antes de mandar la respuesta JSON al navegador (`_json_safe`)."""
import sys
import ast as _ast
import math as _math
import builtins as _builtins
from narrator import _build_eval_map, _active_subscripts, _decompose, _var_code_order

_BUILTIN_NAMES = set(dir(_builtins))
MAX_STEPS = 2000  # hard cap on traced steps so an infinite loop can't hang the server if MAX_STEPS never fires


class _StepLimitReached(RuntimeError):
    """Marca específicamente el corte por MAX_STEPS, distinto de un
    RuntimeError genuino del código del alumno -- así el frontend puede
    mostrar 'Truncado' en vez de 'Error' (el código no tiene ningún bug,
    simplemente generó más pasos de los que se trazan por seguridad)."""
    pass


def _json_safe(o):
    """Recursively replace JSON-invalid values (NaN, Infinity) with readable
    string sentinels so the browser's strict JSON.parse never chokes."""
    if isinstance(o, float):
        if _math.isnan(o): return 'NaN'
        if _math.isinf(o): return 'Infinity' if o > 0 else '-Infinity'
        return o
    if isinstance(o, dict):
        return {k: _json_safe(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_json_safe(v) for v in o]
    if isinstance(o, tuple):
        return [_json_safe(v) for v in o]
    return o


def _run_user_code(code, q):
    """Runs in a child process (spawned by /prepare) so a genuine timeout can
    kill it outright — unlike a thread, which Python can never force-stop,
    leaving blocked calls (time.sleep(), a stuck socket, …) running forever
    in the server if MAX_STEPS never fires. Streams each traced step onto
    `q` as it happens (not just once at the end) so the parent still gets
    whatever progress was made even if it later has to kill this process."""
    out_buf = []
    steps_count = 0

    def custom_print(*args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        out_buf.append(sep.join(str(a) for a in args) + end)

    def custom_input(prompt=''):
        # input() would block the server forever in this non-interactive viewer
        raise RuntimeError('input() no está disponible en el visualizador. '
                           'Usa un valor fijo, p. ej. x = 5')

    def serial(v, d=0):
        if d > 6: return repr(v)
        if isinstance(v, bool): return v
        if isinstance(v, (int, float, str, type(None))): return v
        if isinstance(v, (list, tuple)): return [serial(i, d+1) for i in v]
        if isinstance(v, dict): return {str(k): serial(val, d+1) for k, val in v.items()}
        if isinstance(v, set): return {'__set__': True, 'values': sorted([serial(i, d+1) for i in v], key=str)}
        # numpy scalar types
        try:
            import numpy as _np
            if isinstance(v, _np.integer): return int(v)
            if isinstance(v, _np.floating): return float(v)
            if isinstance(v, _np.bool_): return bool(v)
            if isinstance(v, _np.ndarray):
                if v.ndim == 0: return serial(v.item(), d+1)
                if v.ndim == 1: return [serial(x, d+1) for x in v.tolist()]
                return {'__matrix__': True, 'data': v.tolist()[:20],
                        'shape': list(v.shape), 'dtype': str(v.dtype)}
        except Exception: pass
        # pandas
        try:
            import pandas as _pd
            if isinstance(v, _pd.Series):
                idxs = [str(i) for i in v.index.tolist()][:30]
                vals = [serial(x, d+1) for x in v.values.tolist()[:30]]
                return {'__series__': True, 'index': idxs, 'values': vals,
                        'name': str(v.name) if v.name is not None else None, 'len': len(v)}
            if isinstance(v, _pd.DataFrame):
                MAX_R = 15
                cols = [str(c) for c in v.columns]
                rows = [{str(c): serial(v.iloc[i][c], d+1) for c in v.columns}
                        for i in range(min(MAX_R, len(v)))]
                return {'__df__': True, 'columns': cols, 'data': rows,
                        'shape': list(v.shape), 'truncated': len(v) > MAX_R}
        except Exception: pass
        # class instances with __dict__
        if hasattr(v, '__dict__') and not isinstance(v, type):
            attrs = {}
            for ak, av in list(v.__dict__.items())[:12]:
                if not ak.startswith('_'):
                    try: attrs[ak] = serial(av, d+1)
                    except: attrs[ak] = repr(av)
            return {'__obj__': True, 'type': type(v).__name__, 'attrs': attrs}
        return repr(v)

    def getvars(loc):
        r = {}
        for k, v in loc.items():
            if k.startswith('_') or k in _BUILTIN_NAMES or callable(v): continue
            # skip imported modules and class definitions
            if type(v).__name__ == 'module': continue
            if isinstance(v, type): continue
            try: r[k] = serial(v)
            except: r[k] = repr(v)
        return r

    # Unique filename so library-generated code compiled as '<string>'
    # (numpy/pandas regex, eval, etc.) doesn't collide with the user's code.
    USER_FILE = '<vis_user_code>'

    def stack(frame):
        s, f = [], frame
        while f:
            if f.f_code.co_filename == USER_FILE:
                s.insert(0, {'name': f.f_code.co_name, 'line': f.f_lineno, 'variables': getvars(dict(f.f_locals))})
            f = f.f_back
        return s

    eval_map = _build_eval_map(code)
    active_subs = _active_subscripts(code)

    def tracer(frame, event, arg):
        nonlocal steps_count
        if frame.f_code.co_filename != USER_FILE: return tracer
        if event == 'line':
            if steps_count >= MAX_STEPS:
                raise _StepLimitReached(f'Límite de {MAX_STEPS} pasos alcanzado — el código sigue '
                                   f'ejecutándose (bucle muy largo o quizás infinito). '
                                   f'Se muestran los pasos ya registrados.')
            st = {'line': frame.f_lineno, 'frames': stack(frame), 'output': ''.join(out_buf)}
            node = eval_map.get(frame.f_lineno)
            if node is not None:
                bd = _decompose(node, frame.f_globals, frame.f_locals)
                if bd:
                    st['eval'] = bd
            # Which indices of which list(s) this line is comparing/touching
            # right now — drives the bar-chart "claw" highlight in the UI.
            subs = active_subs.get(frame.f_lineno)
            if subs:
                idxmap = {}
                for varname, idxnode in subs:
                    try:
                        iexpr = _ast.fix_missing_locations(_ast.Expression(body=idxnode))
                        iv = eval(compile(iexpr, '<vis_idx>', 'eval'), frame.f_globals, frame.f_locals)
                    except Exception:
                        continue
                    if isinstance(iv, bool) or not isinstance(iv, int):
                        continue
                    idxmap.setdefault(varname, [])
                    if iv not in idxmap[varname]:
                        idxmap[varname].append(iv)
                if idxmap:
                    st['idx'] = idxmap
            steps_count += 1
            q.put(('step', st))
        return tracer

    g = {'__builtins__': _builtins, 'print': custom_print, 'input': custom_input,
         '__name__': '__main__'}
    run_error = None
    truncated = False  # True = corte de seguridad (MAX_STEPS), no un bug real del alumno

    # sys.settrace is per-thread; this process's main thread is the only
    # thread here, so it can be armed directly (no inner worker thread needed
    # — that layer only existed for the old thread-based design).
    sys.settrace(tracer)
    err_line = None
    try:
        exec(compile(code, USER_FILE, 'exec'), g)
    except Exception as e:
        # Keep whatever steps were already streamed instead of discarding
        # them — a runtime error (or hitting MAX_STEPS) shouldn't blank
        # out everything the visualizer already traced.
        if isinstance(e, _StepLimitReached):
            truncated = True
            run_error = str(e)  # sin prefijo "_StepLimitReached: ", el mensaje ya se explica solo
        else:
            run_error = f'{type(e).__name__}: {e}'
        # Walk the traceback to the deepest frame that's actually the user's
        # code (not numpy/pandas internals) so the Reto modal can point at
        # the exact offending line instead of just showing the message.
        tb = e.__traceback__
        while tb:
            if tb.tb_frame.f_code.co_filename == USER_FILE:
                err_line = tb.tb_lineno
            tb = tb.tb_next
        if err_line is None and isinstance(e, SyntaxError) and e.lineno is not None:
            err_line = e.lineno  # compile() falla antes de crear un frame trazable
    finally:
        sys.settrace(None)

    fv = getvars({k: v for k, v in g.items() if k not in ('__builtins__', 'print', '__name__')})
    # Sort final variables by first assignment line in source code
    code_order = _var_code_order(code)
    fv = dict(sorted(fv.items(), key=lambda kv: (code_order.get(kv[0], 99999), kv[0])))
    q.put(('done', run_error, fv, ''.join(out_buf), err_line, truncated))



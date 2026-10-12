#!/usr/bin/env python3
"""Construcción del "Reto de código" del Modo Maestro Py: análisis AST puro
(no ejecuta nada) que convierte el código de un tema en un stub para que el
alumno lo rellene, más el prompt derivado del comentario inicial del
ejercicio. Consumido por la ruta `/challenge`."""
import ast as _ast
import copy as _copy


def _leading_comment_prompt(code):
    """Primeras líneas de comentario al inicio del código, unidas en una frase —
    convención que siguen todos los ejercicios (S00–S16, Práctica 1/2)."""
    lines = []
    for raw in code.split('\n'):
        s = raw.strip()
        if not s:
            if lines:
                break
            continue
        if s.startswith('#'):
            lines.append(s.lstrip('#').strip())
        else:
            break
    return ' '.join(lines) if lines else \
        'Reescribe este ejemplo con tu propio código, reproduciendo el mismo resultado.'


def _build_challenge(code):
    """Divide un ejemplo en {prompt, mode, stub, hasAssert} para el "Reto de
    código" del Modo Maestro. mode='fill': hay función(es)/clase(s) top-level;
    se vacían a `pass` y se dejan sobre el harness original — preservado tal
    cual con get_source_segment (no ast.unparse) para no destrozar strings
    multilínea/formato del setup y los prints/asserts de prueba. mode='blank':
    no hay nada que vaciar (script de sintaxis suelto), editor en blanco."""
    try:
        tree = _ast.parse(code)
    except SyntaxError:
        return {'challengeable': False}

    top_defs = [n for n in tree.body if isinstance(n, (_ast.FunctionDef, _ast.ClassDef))]
    has_assert = any(isinstance(n, _ast.Assert) for n in _ast.walk(tree))
    prompt = _leading_comment_prompt(code)

    if not top_defs:
        return {'challengeable': True, 'mode': 'blank', 'prompt': prompt,
                'stub': '', 'hasAssert': has_assert}

    try:
        # Recorre tree.body en su ORDEN ORIGINAL (no "todas las defs primero,
        # luego el resto"): una clase puede referenciar en su propia cabecera
        # algo que un import trae (p. ej. `class Figura(ABC):`), así que el
        # import tiene que seguir apareciendo ANTES de esa clase en el stub.
        parts = []
        for n in tree.body:
            if isinstance(n, (_ast.FunctionDef, _ast.ClassDef)):
                blanked = _copy.deepcopy(n)
                blanked.body = [_ast.Pass()]
                _ast.fix_missing_locations(blanked)
                txt = _ast.unparse(blanked)
                txt = txt.replace('    pass', '    # TODO: escribe tu código aquí\n    pass', 1)
                parts.append(txt)
            else:
                seg = _ast.get_source_segment(code, n)
                if seg:
                    parts.append(seg)
        stub = '\n\n'.join(parts)
    except Exception:
        return {'challengeable': False}

    return {'challengeable': True, 'mode': 'fill', 'prompt': prompt,
            'stub': stub, 'hasAssert': has_assert}



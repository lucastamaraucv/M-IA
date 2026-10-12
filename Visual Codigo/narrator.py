#!/usr/bin/env python3
"""Narrador AST: análisis estático del código del alumno (sin ejecutarlo) para
generar las explicaciones en español línea por línea, las relaciones
for-loop → contenedor, los accesos a subíndices seguros de re-evaluar, y el
desglose paso a paso de sub-expresiones compuestas — todo lo que consume
`sandbox._run_user_code` y la ruta `/prepare`."""
import ast as _ast

def _var_code_order(code):
    """Return dict of varname → first line of assignment in source code."""
    order = {}
    try:
        tree = _ast.parse(code)
        for node in _ast.walk(tree):
            ln = getattr(node, 'lineno', None)
            if ln is None: continue
            targets = []
            if isinstance(node, _ast.Assign):
                for t in node.targets:
                    targets += [n for n in _ast.walk(t) if isinstance(n, _ast.Name)]
            elif isinstance(node, (_ast.AugAssign, _ast.AnnAssign)):
                if isinstance(node.target, _ast.Name):
                    targets = [node.target]
            elif isinstance(node, _ast.For):
                targets = [n for n in _ast.walk(node.target) if isinstance(n, _ast.Name)]
            elif isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
                targets = [type('_N', (), {'id': node.name})]
                for arg in getattr(getattr(node, 'args', None), 'args', []):
                    if arg.arg not in order:
                        order[arg.arg] = ln
            elif isinstance(node, _ast.With):
                for item in node.items:
                    if isinstance(getattr(item, 'optional_vars', None), _ast.Name):
                        targets.append(item.optional_vars)
            for t in targets:
                nm = getattr(t, 'id', None)
                if nm and nm not in order:
                    order[nm] = ln
    except Exception:
        pass
    return order


def _find_relations(code):
    """Parse AST to find for-loop variable → source relationships."""
    rels = {}
    try:
        tree = _ast.parse(code)
        for node in _ast.walk(tree):
            if not isinstance(node, _ast.For): continue
            src = None
            iter_n = node.iter
            if isinstance(iter_n, _ast.Name):
                src = iter_n.id
            elif isinstance(iter_n, _ast.Call):
                fn = iter_n
                if isinstance(fn.func, _ast.Name):
                    fname = fn.func.id
                    if fname == 'enumerate' and fn.args and isinstance(fn.args[0], _ast.Name):
                        src = fn.args[0].id
                    elif fname == 'reversed' and fn.args and isinstance(fn.args[0], _ast.Name):
                        src = fn.args[0].id
                elif isinstance(fn.func, _ast.Attribute) and isinstance(fn.func.value, _ast.Name):
                    if fn.func.attr in ('items', 'keys', 'values'):
                        src = fn.func.value.id
                    elif fn.func.attr in ('enumerate',):
                        src = fn.func.value.id
            if src:
                if isinstance(node.target, _ast.Name):
                    rels[node.target.id] = src
                elif isinstance(node.target, _ast.Tuple):
                    for e in node.target.elts:
                        if isinstance(e, _ast.Name):
                            rels[e.id] = src
    except Exception:
        pass
    return rels


def _active_subscripts(code):
    """{lineno: [(varname, index_ast_node), ...]} for every single-line
    `var[idx_expr]` access whose idx_expr is safe to re-evaluate later.
    This is what lets the frontend highlight exactly which indices a
    comparison/swap line is touching (e.g. the i and i+1 in
    `if a[i] > a[i+1]:`) for ANY sorting algorithm's index style — unlike
    _find_relations, it doesn't depend on a `for x in a` loop shape."""
    out = {}
    try:
        tree = _ast.parse(code)
        for node in _ast.walk(tree):
            if not isinstance(node, _ast.Subscript): continue
            if not isinstance(node.value, _ast.Name): continue
            idx = node.slice
            if isinstance(idx, _ast.Slice): continue  # a[i:j] — not a single index
            if _has_unsafe_node(idx): continue
            ln = getattr(node, 'lineno', None)
            if ln is None: continue
            out.setdefault(ln, []).append((node.value.id, idx))
    except Exception:
        pass
    return out


def _explain_lines(code):
    """AST-based natural-language (Spanish) explanation per source line.
    Returns {lineno: {'text': str, 'kind': str}} for the executable statements."""
    out = {}

    def short(node, maxlen=46):
        try:
            s = _ast.unparse(node)
        except Exception:
            return '...'
        s = ' '.join(s.split())
        return s if len(s) <= maxlen else s[:maxlen - 1] + '…'

    def name_of(node):
        if isinstance(node, _ast.Name): return node.id
        if isinstance(node, _ast.Tuple):
            return ', '.join(name_of(e) for e in node.elts)
        if isinstance(node, _ast.Attribute): return short(node)
        if isinstance(node, _ast.Subscript): return short(node)
        if isinstance(node, _ast.Starred): return '*' + name_of(node.value)
        return short(node)

    def bitmask_call_hint(node):
        """Recognize a couple of common bitmask idioms so Return/Assign (which
        don't go through call_desc) can surface them too, instead of just
        printing the raw call source. Returns None when nothing matches."""
        fn = node.func
        if isinstance(fn, _ast.Name) and fn.id == 'int' and len(node.args) == 2 \
                and isinstance(node.args[1], _ast.Constant) and node.args[1].value == 2:
            return f'Convierte un texto binario en un entero (crea un bitmask): {short(node)}'
        if isinstance(fn, _ast.Attribute) and fn.attr == 'count' \
                and isinstance(fn.value, _ast.Call) and isinstance(fn.value.func, _ast.Name) \
                and fn.value.func.id == 'bin':
            inner = short(fn.value.args[0]) if fn.value.args else '…'
            return f'Cuenta los bits en 1 (popcount) de «{inner}» → nº de actores distintos'
        return None

    def call_desc(node):
        """Describe a Call node, with friendly handling of common builtins/methods."""
        fn = node.func
        if isinstance(fn, _ast.Name):
            fname = fn.id
            if fname == 'print':
                inner = ', '.join(short(a) for a in node.args) or '(vacío)'
                return ('print', f'Imprime en la consola: {inner}')
            if fname == 'range':
                return ('range', f'Genera la secuencia de números {short(node)}')
            if fname in ('len',):
                return ('call', f'Calcula la longitud con {short(node)}')
            if fname in ('input',):
                return ('call', f'Pide un dato al usuario con {short(node)}')
            if fname in ('open',):
                return ('call', f'Abre un archivo con {short(node)}')
            bh = bitmask_call_hint(node)
            if bh:
                return ('call', bh)
            if fname == 'bin':
                return ('call', f'Convierte {short(node.args[0]) if node.args else "…"} a su representación binaria (texto "0b…")')
            return ('call', f'Llama a la función {fname}(…)')
        if isinstance(fn, _ast.Attribute):
            obj = name_of(fn.value)
            meth = fn.attr
            bh = bitmask_call_hint(node)
            if bh:
                return ('method', bh)
            return ('method', f'Aplica el método .{meth}() sobre {obj}')
        return ('call', f'Evalúa {short(node)}')

    def explain(node):
        # ── Assignment ──
        if isinstance(node, _ast.Assign):
            tgt = node.targets[0]
            val = node.value
            tname = name_of(tgt)
            # a = b = c = 0  → several targets at once
            if len(node.targets) > 1:
                allt = ', '.join('«' + name_of(t) + '»' for t in node.targets)
                return ('assign', f'Asigna {short(val)} a {allt}')
            if isinstance(val, _ast.Lambda):
                params = ', '.join(a.arg for a in val.args.args)
                return ('def', f'Define la función lambda «{tname}({params})»')
            if isinstance(tgt, _ast.Tuple):
                # swap detection: a, b = b, a
                if (isinstance(val, _ast.Tuple) and len(tgt.elts) == len(val.elts) == 2
                        and {name_of(e) for e in tgt.elts} == {name_of(e) for e in val.elts}):
                    return ('assign', f'Intercambia los valores de {name_of(tgt)}')
                return ('assign', f'Asignación múltiple: {tname} = {short(val)}')
            if isinstance(val, _ast.JoinedStr):
                return ('assign', f'Construye un texto (f-string) y lo guarda en «{tname}»')
            if isinstance(val, _ast.Call):
                bh = bitmask_call_hint(val)
                if bh:
                    return ('assign', f'Guarda en «{tname}»: {bh}')
                return ('assign', f'Guarda en «{tname}» el resultado de {short(val)}')
            if isinstance(val, _ast.BinOp):
                bit_ops = {_ast.BitOr: 'OR bit a bit', _ast.BitAnd: 'AND bit a bit',
                           _ast.BitXor: 'XOR bit a bit', _ast.LShift: 'desplaza bits ←',
                           _ast.RShift: 'desplaza bits →'}
                note = bit_ops.get(type(val.op))
                if note:
                    return ('assign', f'Calcula {short(val)} ({note}) y lo guarda en «{tname}»')
                return ('assign', f'Calcula {short(val)} y lo guarda en «{tname}»')
            if isinstance(val, _ast.IfExp):
                return ('cond', f'Asigna a «{tname}» según la condición {short(val.test)}')
            if isinstance(val, (_ast.List, _ast.ListComp)):
                return ('assign', f'Crea una lista y la asigna a «{tname}»')
            if isinstance(val, (_ast.Dict, _ast.DictComp)):
                return ('assign', f'Crea un diccionario y lo asigna a «{tname}»')
            if isinstance(val, (_ast.Set, _ast.SetComp)):
                return ('assign', f'Crea un conjunto y lo asigna a «{tname}»')
            if isinstance(val, _ast.GeneratorExp):
                return ('yield', f'Crea un generador (perezoso) y lo asigna a «{tname}»')
            if isinstance(val, _ast.Tuple):
                return ('assign', f'Crea una tupla y la asigna a «{tname}»')
            return ('assign', f'Asigna {short(val)} a la variable «{tname}»')
        if isinstance(node, _ast.AnnAssign):
            tname = name_of(node.target)
            if node.value is not None:
                return ('assign', f'Asigna {short(node.value)} a «{tname}» (con anotación de tipo)')
            return ('assign', f'Declara «{tname}» con anotación de tipo')
        if isinstance(node, _ast.AugAssign):
            op = type(node.op).__name__
            verb = {'Add': 'Suma', 'Sub': 'Resta', 'Mult': 'Multiplica',
                    'Div': 'Divide', 'Mod': 'Aplica módulo', 'Pow': 'Eleva',
                    'FloorDiv': 'Divide (entera)',
                    'BitOr': 'Combina con OR bit a bit (une los bits en 1)',
                    'BitAnd': 'Combina con AND bit a bit (mantiene los bits comunes)',
                    'BitXor': 'Combina con XOR bit a bit',
                    'LShift': 'Desplaza los bits a la izquierda de',
                    'RShift': 'Desplaza los bits a la derecha de'}.get(op, 'Actualiza')
            return ('augassign', f'{verb} {short(node.value)} sobre «{name_of(node.target)}»')
        # ── Control flow ──
        if isinstance(node, _ast.For):
            return ('loop', f'Bucle for: recorre «{name_of(node.iter)}», asignando cada elemento a «{name_of(node.target)}»')
        if isinstance(node, _ast.While):
            return ('loop', f'Bucle while: repite mientras {short(node.test)}')
        if isinstance(node, _ast.If):
            return ('cond', f'Condición: evalúa si {short(node.test)}')
        if isinstance(node, (_ast.With, _ast.AsyncWith)):
            item = node.items[0] if node.items else None
            ctx = short(item.context_expr) if item else ''
            if item and isinstance(getattr(item, 'optional_vars', None), _ast.Name):
                return ('with', f'Abre un contexto with {ctx} como «{item.optional_vars.id}» (se cierra solo al salir)')
            return ('with', f'Abre un contexto with: {ctx} (se cierra solo al salir)')
        if isinstance(node, _ast.Try):
            return ('try', 'Bloque try: intenta ejecutar código vigilando errores')
        if isinstance(node, _ast.ExceptHandler):
            t = short(node.type) if node.type else 'cualquier error'
            return ('except', f'except: captura {t} si ocurre')
        # ── Definitions ──
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            args = ', '.join(a.arg for a in node.args.args)
            pre = 'Define la función asíncrona' if isinstance(node, _ast.AsyncFunctionDef) else 'Define la función'
            return ('def', f'{pre} «{node.name}({args})»')
        if isinstance(node, _ast.ClassDef):
            if node.bases:
                bases = ', '.join(name_of(b) for b in node.bases)
                return ('class', f'Define la clase «{node.name}» (hereda de {bases})')
            return ('class', f'Define la clase «{node.name}»')
        if isinstance(node, _ast.Return):
            if node.value is None:
                return ('return', 'Devuelve el control (return sin valor)')
            if isinstance(node.value, _ast.Call):
                bh = bitmask_call_hint(node.value)
                if bh:
                    return ('return', f'Devuelve: {bh}')
            return ('return', f'Devuelve {short(node.value)}')
        if isinstance(node, _ast.Yield) or (isinstance(node, _ast.Expr) and isinstance(node.value, _ast.Yield)):
            return ('yield', 'Produce un valor con yield (generador)')
        # ── Imports ──
        if isinstance(node, _ast.Import):
            mods = ', '.join(a.name for a in node.names)
            return ('import', f'Importa el módulo {mods}')
        if isinstance(node, _ast.ImportFrom):
            names = ', '.join(a.name for a in node.names)
            return ('import', f'Importa {names} desde {node.module}')
        # ── Simple statements ──
        if isinstance(node, _ast.Expr):
            v = node.value
            if isinstance(v, _ast.Call):
                k, d = call_desc(v)
                return (k, d)
            if isinstance(v, _ast.Yield):
                return ('yield', 'Produce un valor con yield (generador)')
            return ('expr', f'Evalúa {short(v)}')
        if isinstance(node, _ast.Assert):
            return ('assert', f'Verifica (assert) que {short(node.test)}')
        if isinstance(node, _ast.Raise):
            return ('raise', f'Lanza una excepción {short(node.exc) if node.exc else ""}')
        if isinstance(node, _ast.Pass):
            return ('pass', 'No hace nada (pass)')
        if isinstance(node, _ast.Break):
            return ('break', 'Rompe el bucle (break)')
        if isinstance(node, _ast.Continue):
            return ('continue', 'Salta a la siguiente vuelta del bucle (continue)')
        if isinstance(node, _ast.Delete):
            return ('del', f'Elimina {", ".join(name_of(t) for t in node.targets)}')
        if isinstance(node, _ast.Global):
            return ('global', f'Usa la variable global: {", ".join(node.names)}')
        if isinstance(node, _ast.Nonlocal):
            return ('global', f'Usa la variable del ámbito exterior: {", ".join(node.names)}')
        return None

    try:
        tree = _ast.parse(code)
        for node in _ast.walk(tree):
            # Decorator lines (@property, @staticmethod, …) sit above the def
            for dec in getattr(node, 'decorator_list', []) or []:
                dln = getattr(dec, 'lineno', None)
                if dln and dln not in out:
                    out[dln] = {'text': f'Decorador @{short(dec)}: modifica la función/clase siguiente',
                                'kind': 'def'}
            # match/case (Python 3.10+)
            if node.__class__.__name__ == 'Match':
                mln = getattr(node, 'lineno', None)
                if mln and mln not in out:
                    out[mln] = {'text': f'Evalúa {short(node.subject)} y compara con los patrones case',
                                'kind': 'cond'}
                for case in getattr(node, 'cases', []):
                    pat = getattr(case, 'pattern', None)
                    cln = getattr(pat, 'lineno', None) or getattr(case, 'lineno', None)
                    if cln and cln not in out:
                        out[cln] = {'text': 'Patrón case: comprueba si el valor coincide con este caso',
                                    'kind': 'cond'}
            if not isinstance(node, _ast.stmt) and not isinstance(node, _ast.ExceptHandler):
                continue
            ln = getattr(node, 'lineno', None)
            if ln is None:
                continue
            res = explain(node)
            if res:
                kind, text = res
                if ln not in out:
                    out[ln] = {'text': text, 'kind': kind}
                else:
                    # Same physical line already explained: this happens with
                    # compound statements joined by ';' (e.g. `a.pop(); b.append(x)`)
                    # — append instead of silently dropping the 2nd+ statement.
                    out[ln]['text'] += '  ·  ' + text

        # Second pass: multi-line *simple* statements (dicts/lists/calls spanning
        # several lines) emit trace events on their continuation lines too —
        # propagate the same explanation so the narrator never goes blank.
        _SIMPLE = (_ast.Assign, _ast.AnnAssign, _ast.AugAssign, _ast.Return,
                   _ast.Expr, _ast.Assert, _ast.Raise, _ast.Delete)
        for node in _ast.walk(tree):
            if not isinstance(node, _SIMPLE):
                continue
            ln = getattr(node, 'lineno', None)
            end = getattr(node, 'end_lineno', None)
            if not ln or not end or end <= ln or ln not in out:
                continue
            base = out[ln]
            for cont in range(ln + 1, end + 1):
                if cont not in out:
                    out[cont] = {'text': '↳ continúa: ' + base['text'], 'kind': base['kind']}
    except Exception:
        pass
    return out


# ── Expression breakdown (paso a paso del cálculo) ──────────────────────────
# Subscript/Attribute reads (bitmasks[t], obj.attr) are treated as safe to
# re-evaluate: for ordinary containers/objects they have no side effects, and
# allowing them lets the breakdown reach expressions like `mejor[1] is None`
# that are central to understanding conditions/pruning in algorithms.
_UNSAFE_EVAL = (_ast.Lambda, _ast.ListComp, _ast.DictComp, _ast.SetComp,
                _ast.GeneratorExp, _ast.Await, _ast.Starred, _ast.NamedExpr)
# len()/abs() have no side effects and are extremely common inside
# conditions (`len(dias[j]) < max_dia`) — allow just these as an exception
# to the "no calls" rule so those conditions can still be broken down.
_SAFE_CALL_NAMES = {'len', 'abs'}


def _has_unsafe_node(expr):
    for n in _ast.walk(expr):
        if isinstance(n, _UNSAFE_EVAL):
            return True
        if isinstance(n, _ast.Call):
            fn = n.func
            if not (isinstance(fn, _ast.Name) and fn.id in _SAFE_CALL_NAMES):
                return True
    return False


def _build_eval_map(code):
    """{lineno: expr_node} para sentencias de una sola línea cuyo valor/condición
    se puede desglosar (asignaciones, condiciones de if/while, return)."""
    m = {}
    try:
        tree = _ast.parse(code)
        for node in _ast.walk(tree):
            expr = None
            if isinstance(node, (_ast.Assign, _ast.AugAssign, _ast.AnnAssign)):
                expr = node.value
            elif isinstance(node, (_ast.If, _ast.While)):
                expr = node.test
            elif isinstance(node, _ast.Return):
                expr = node.value
            if expr is None:
                continue
            ln = getattr(expr, 'lineno', None)
            end = getattr(expr, 'end_lineno', ln)
            if ln is None or end != ln:   # solo expresiones de una línea
                continue
            m.setdefault(ln, expr)
    except Exception:
        pass
    return m


def _short_val(v):
    try:
        if isinstance(v, bool):
            r = 'True' if v else 'False'
        elif isinstance(v, float):
            if v != v: return 'nan'
            r = repr(round(v, 4)) if abs(v) < 1e16 else repr(v)
        else:
            r = repr(v)
    except Exception:
        return '?'
    return r if len(r) <= 32 else r[:31] + '…'


def _decompose(expr, fglobals, flocals):
    """Lista [{'expr','val'}] de subexpresiones compuestas evaluadas con los
    valores reales del frame, en orden de evaluación (de dentro hacia fuera).
    Solo expresiones sin llamadas arbitrarias/comprehensions (salvo len/abs),
    para no producir efectos secundarios al re-evaluarlas."""
    if expr is None or _has_unsafe_node(expr):
        return []
    out, seen = [], set()

    def visit(n):
        for child in _ast.iter_child_nodes(n):
            visit(child)
        if isinstance(n, (_ast.BinOp, _ast.UnaryOp, _ast.BoolOp, _ast.Compare)):
            try:
                src = _ast.unparse(n)
            except Exception:
                return
            if src in seen:
                return
            try:
                node = _ast.fix_missing_locations(_ast.Expression(body=n))
                val = eval(compile(node, '<vis_eval>', 'eval'), fglobals, flocals)
            except Exception:
                return
            seen.add(src)
            out.append({'expr': src if len(src) <= 40 else src[:39] + '…',
                        'val': _short_val(val)})

    try:
        visit(expr)
    except Exception:
        return []
    return out[:5]

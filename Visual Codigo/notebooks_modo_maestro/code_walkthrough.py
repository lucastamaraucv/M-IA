"""Explicador automatico de codigo, en base al AST, para los notebooks del
Modo Maestro.

En vez de una celda vacia "Pruebalo tu", cada notebook trae una seccion
"Explicacion paso a paso" generada aqui: recorre el arbol de sintaxis del
codigo de ejemplo y arma, bloque por bloque, una descripcion en espanol de
que hace cada linea (asignaciones, bucles, condicionales, funciones,
clases, try/except, etc.), enriquecida con las explicaciones de
method_docs.METHOD_DOCS cuando el fragmento usa un metodo/funcion conocido.

Tambien expone top_level_names() para el cierre "como reutilizar esto":
que funciones/clases/variables quedan disponibles tras ejecutar la celda.
"""
from __future__ import annotations

import ast

from method_docs import METHOD_DOCS

MAX_SNIPPET = 90
MAX_DEPTH = 4  # mas alla de esto, se resume como "..." para no saturar el notebook

_AUGOPS = {
    ast.Add: "+=", ast.Sub: "-=", ast.Mult: "*=", ast.Div: "/=",
    ast.FloorDiv: "//=", ast.Mod: "%=", ast.Pow: "**=",
    ast.LShift: "<<=", ast.RShift: ">>=", ast.BitOr: "|=",
    ast.BitAnd: "&=", ast.BitXor: "^=",
}


def _src(node: ast.AST) -> str:
    try:
        text = ast.unparse(node)
    except Exception:
        return "<expresion>"
    text = " ".join(text.split())  # colapsa saltos de linea internos
    if len(text) > MAX_SNIPPET:
        text = text[: MAX_SNIPPET - 1] + "…"
    return text


_METHOD_DOCS_BY_SPECIFICITY = sorted(METHOD_DOCS.items(), key=lambda kv: -len(kv[0]))


def _annotate(snippet: str) -> str:
    """Si snippet contiene una llamada/metodo conocido de METHOD_DOCS,
    agrega su explicacion. Prueba las claves mas largas (mas especificas)
    primero, para que "np.arange(" gane sobre el generico "range(" en un
    snippet como "np.arange(12)". Solo la primera coincidencia, para no
    saturar la explicacion."""
    for key, doc in _METHOD_DOCS_BY_SPECIFICITY:
        if key in snippet:
            return f" — *{doc}*"
    return ""


def _names(targets) -> str:
    return ", ".join(f"`{_src(t)}`" for t in targets)


def _bullets(body: list[ast.AST], depth: int, out: list[tuple[int, str]]) -> None:
    if depth > MAX_DEPTH:
        if body:
            out.append((depth, "…"))
        return
    for node in body:
        _describe(node, depth, out)


def _describe(node: ast.AST, depth: int, out: list[tuple[int, str]]) -> None:
    add = out.append

    if isinstance(node, ast.Import):
        mods = ", ".join(f"`{a.name}`" + (f" como `{a.asname}`" if a.asname else "") for a in node.names)
        add((depth, f"Importa {mods}."))

    elif isinstance(node, ast.ImportFrom):
        mods = ", ".join(f"`{a.name}`" + (f" como `{a.asname}`" if a.asname else "") for a in node.names)
        add((depth, f"Desde `{node.module}` importa {mods}."))

    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = _src(node.args) if node.args.args or node.args.vararg or node.args.kwarg else ""
        deco = "".join(f"`@{_src(d)}` " for d in node.decorator_list)
        add((depth, f"{deco}Define la funcion `{node.name}({args})`:"))
        _bullets([n for n in node.body if not _is_docstring(n)], depth + 1, out)

    elif isinstance(node, ast.ClassDef):
        bases = ", ".join(_src(b) for b in node.bases)
        deco = "".join(f"`@{_src(d)}` " for d in node.decorator_list)
        head = f"{deco}Define la clase `{node.name}`" + (f"(hereda de {bases})" if bases else "") + ":"
        add((depth, head))
        _bullets([n for n in node.body if not _is_docstring(n)], depth + 1, out)

    elif isinstance(node, ast.Assign):
        snippet = _src(node.value)
        add((depth, f"Asigna a {_names(node.targets)}: `{snippet}`{_annotate(snippet)}"))

    elif isinstance(node, ast.AnnAssign):
        snippet = _src(node.value) if node.value else "(sin valor)"
        add((depth, f"Declara `{_src(node.target)}: {_src(node.annotation)}` = `{snippet}`{_annotate(snippet)}"))

    elif isinstance(node, ast.AugAssign):
        op = _AUGOPS.get(type(node.op), type(node.op).__name__)
        snippet = _src(node.value)
        add((depth, f"Actualiza `{_src(node.target)}` (`{_src(node.target)} {op} {snippet}`){_annotate(snippet)}"))

    elif isinstance(node, ast.For):
        it = _src(node.iter)
        add((depth, f"Bucle **for**: recorre `{it}` guardando cada valor en `{_src(node.target)}`:{_annotate(it)}"))
        _bullets(node.body, depth + 1, out)
        if node.orelse:
            add((depth, "Si el bucle termina sin `break` (else):"))
            _bullets(node.orelse, depth + 1, out)

    elif isinstance(node, ast.While):
        test = _src(node.test)
        add((depth, f"Bucle **while**: mientras `{test}` sea verdadero:"))
        _bullets(node.body, depth + 1, out)

    elif isinstance(node, ast.If):
        test = _src(node.test)
        add((depth, f"**Si** `{test}` entonces:"))
        _bullets(node.body, depth + 1, out)
        if node.orelse:
            # elif se representa como un If anidado dentro de orelse
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                _describe(node.orelse[0], depth, out)
            else:
                add((depth, "**En caso contrario:**"))
                _bullets(node.orelse, depth + 1, out)

    elif isinstance(node, ast.Try):
        add((depth, "Intenta ejecutar (**try**):"))
        _bullets(node.body, depth + 1, out)
        for h in node.handlers:
            etype = _src(h.type) if h.type else "cualquier excepcion"
            asname = f" como `{h.name}`" if h.name else ""
            add((depth, f"Si ocurre `{etype}`{asname} (**except**):"))
            _bullets(h.body, depth + 1, out)
        if node.orelse:
            add((depth, "Si no hubo ninguna excepcion (**else**):"))
            _bullets(node.orelse, depth + 1, out)
        if node.finalbody:
            add((depth, "Siempre al final, haya habido error o no (**finally**):"))
            _bullets(node.finalbody, depth + 1, out)

    elif isinstance(node, ast.With):
        ctx = ", ".join(_src(i.context_expr) for i in node.items)
        add((depth, f"Bloque **with** usando `{ctx}` (se cierra/libera automaticamente al salir):"))
        _bullets(node.body, depth + 1, out)

    elif isinstance(node, ast.Return):
        val = _src(node.value) if node.value is not None else "None"
        add((depth, f"**Devuelve** `{val}`{_annotate(val)}."))

    elif isinstance(node, ast.Assert):
        test = _src(node.test)
        add((depth, f"**Verifica** (assert) que `{test}` sea verdadero — si no, el programa se detiene aqui."))

    elif isinstance(node, ast.Raise):
        exc = _src(node.exc) if node.exc else ""
        add((depth, f"**Lanza una excepcion**: `{exc}`."))

    elif isinstance(node, (ast.Global, ast.Nonlocal)):
        kind = "global" if isinstance(node, ast.Global) else "nonlocal"
        add((depth, f"Declara `{', '.join(node.names)}` como variable `{kind}`."))

    elif isinstance(node, ast.Delete):
        add((depth, f"Elimina {_names(node.targets)}."))

    elif isinstance(node, ast.Break):
        add((depth, "**Sale** del bucle (`break`)."))

    elif isinstance(node, ast.Continue):
        add((depth, "**Salta** a la siguiente vuelta del bucle (`continue`)."))

    elif isinstance(node, ast.Pass):
        pass  # no aporta nada al lector, se omite

    elif isinstance(node, ast.Expr):
        if _is_docstring(node):
            return
        val = node.value
        if isinstance(val, ast.Call):
            fname = _src(val.func)
            argtxt = ", ".join(_src(a) for a in val.args) + (
                (", " if val.args and val.keywords else "")
                + ", ".join(f"{k.arg}={_src(k.value)}" for k in val.keywords)
            )
            if fname == "print":
                add((depth, f"**Imprime** en pantalla: `{argtxt}`."))
            else:
                snippet = f"{fname}({argtxt})"
                add((depth, f"Llama a `{snippet}`{_annotate(snippet)}."))
        elif isinstance(val, ast.Yield) or isinstance(val, ast.YieldFrom):
            add((depth, f"**yield** `{_src(val.value) if getattr(val, 'value', None) else ''}` — produce un valor y pausa la funcion hasta el proximo `next()`."))
        else:
            add((depth, f"Evalua `{_src(val)}`."))

    else:
        add((depth, f"`{_src(node)}`"))


def _is_docstring(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def walkthrough_markdown(code: str) -> str:
    """Devuelve una lista con vinetas anidadas en Markdown que explica,
    bloque por bloque, que hace `code`."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "*(no se pudo analizar el codigo automaticamente)*"

    out: list[tuple[int, str]] = []
    _bullets([n for n in tree.body if not _is_docstring(n)], 0, out)

    lines = []
    for depth, text in out:
        indent = "    " * depth
        lines.append(f"{indent}- {text}")
    return "\n".join(lines) if lines else "*(sin contenido ejecutable)*"


def top_level_names(code: str) -> dict[str, list[str]]:
    """Funciones, clases y variables que quedan definidas en el modulo tras
    ejecutar el codigo, en el orden en que aparecen."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"functions": [], "classes": [], "variables": []}

    functions, classes, variables = [], [], []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    variables.append(t.id)
                elif isinstance(t, (ast.Tuple, ast.List)):
                    variables.extend(e.id for e in t.elts if isinstance(e, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            variables.append(node.target.id)

    # unicos, preservando orden
    def _uniq(seq):
        seen, out = set(), []
        for x in seq:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return {"functions": _uniq(functions), "classes": _uniq(classes), "variables": _uniq(variables)}

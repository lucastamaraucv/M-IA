#!/usr/bin/env python3
"""
DEBUGGER VISUAL AVANZADO CON VISUALIZACIÓN DE OBJETOS
======================================================
Ejecuta:  python debugger_visual.py
Abre:     http://localhost:5050

Muestra variables, objetos en memoria y ejecución paso a paso.
"""
import sys, io, textwrap, traceback, threading, webbrowser
from flask import Flask, request, jsonify, make_response

app  = Flask(__name__)
MAX_STEPS = 600
EXEC_FILE = "<debugger>"

# ══════════════════════════════════════════════════════════════
# SERIALIZACIÓN: Python → JSON para visualización
# ══════════════════════════════════════════════════════════════
_SKIP = {
    "__builtins__","__name__","__doc__","__package__",
    "__loader__","__spec__","__annotations__","__cached__","__file__",
}

def _val(v, depth=0, seen=None):
    """Convierte un valor Python en dict JSON para el frontend."""
    if seen is None:
        seen = set()
    oid = id(v)

    if isinstance(v, bool):   return {"t": "bool",  "v": str(v)}
    if isinstance(v, int):    return {"t": "int",   "v": v}
    if isinstance(v, float):  return {"t": "float", "v": round(v, 8)}
    if isinstance(v, str):    return {"t": "str",   "v": v}
    if v is None:             return {"t": "None",  "v": "None"}

    if depth > 3 or oid in seen:
        return {"t": type(v).__name__, "v": repr(v)[:60], "id": oid, "ref": True}
    seen = seen | {oid}

    if isinstance(v, (list, tuple)):
        name  = "list" if isinstance(v, list) else "tuple"
        items = [_val(x, depth + 1, seen) for x in v[:50]]
        return {"t": name, "id": oid, "items": items, "len": len(v)}

    if isinstance(v, dict):
        pairs = [{"k": _val(k, depth+1, seen), "v": _val(vv, depth+1, seen)}
                 for k, vv in list(v.items())[:30]]
        return {"t": "dict", "id": oid, "pairs": pairs, "len": len(v)}

    if isinstance(v, set):
        items = [_val(x, depth+1, seen) for x in list(v)[:30]]
        return {"t": "set", "id": oid, "items": items, "len": len(v)}

    return {"t": type(v).__name__, "v": repr(v)[:80], "id": oid}


def _frame_vars(d, base=None):
    out  = {}
    skip = _SKIP | (base or set())
    for k, v in d.items():
        if k.startswith("__") or k in skip:
            continue
        try:
            out[k] = _val(v)
        except Exception:
            out[k] = {"t": "error", "v": "<error>"}
    return out


# ══════════════════════════════════════════════════════════════
# EJECUCIÓN TRAZADA PASO A PASO
# ══════════════════════════════════════════════════════════════
def run_traced(code):
    code  = textwrap.dedent(code)
    lines = code.splitlines()
    steps = []
    out   = []
    n     = [0]

    g         = {"__name__": "__main__", "__builtins__": __builtins__}
    base_keys = set(g.keys())

    class _Cap(io.StringIO):
        def write(self, s):
            out.append(s)
            return len(s)

    cap = _Cap()

    def trace(frame, event, arg):
        if frame.f_code.co_filename != EXEC_FILE:
            return trace
        if n[0] >= MAX_STEPS:
            return None

        name = frame.f_code.co_name

        # No rastrear el interior de comprehensions línea a línea
        if name in ("<listcomp>", "<dictcomp>", "<setcomp>", "<genexpr>"):
            return trace

        if event == "line":
            n[0] += 1
            if name == "<module>":
                vars_snap = _frame_vars(frame.f_locals, base_keys)
            else:
                vars_snap = _frame_vars(frame.f_locals)

            steps.append({
                "ev":   "line",
                "ln":   frame.f_lineno,
                "fn":   name,
                "vars": vars_snap,
                "out":  "".join(out),
            })

        elif event == "return":
            if name == "<module>":
                return trace
            n[0] += 1
            s = {
                "ev":   "return",
                "ln":   frame.f_lineno,
                "fn":   name,
                "vars": _frame_vars(g, base_keys),
                "out":  "".join(out),
            }
            if arg is not None:
                s["ret"] = _val(arg)
            steps.append(s)

        return trace

    old_stdout = sys.stdout
    sys.stdout = cap
    error = None

    try:
        compiled = compile(code, EXEC_FILE, "exec")
        sys.settrace(trace)
        exec(compiled, g)
        sys.settrace(None)
    except Exception:
        sys.settrace(None)
        error = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        sys.settrace(None)

    steps.append({
        "ev":   "error" if error else "end",
        "ln":   len(lines),
        "fn":   "<module>",
        "vars": _frame_vars(g, base_keys),
        "out":  "".join(out),
        "err":  error,
    })

    return steps, lines


# ══════════════════════════════════════════════════════════════
# FLASK
# ══════════════════════════════════════════════════════════════
@app.route("/")
def index():
    r = make_response(HTML)
    r.headers["Content-Type"] = "text/html; charset=utf-8"
    return r


@app.route("/run", methods=["POST"])
def run_route():
    code = request.json.get("code", "")
    steps, lines = run_traced(code)
    return jsonify({"steps": steps, "lines": lines})


# ══════════════════════════════════════════════════════════════
# FRONTEND HTML / CSS / JS  (todo embebido)
# ══════════════════════════════════════════════════════════════
HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Debugger Visual Python</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#1e1e2e;--surface:#252538;--surface2:#2e2e45;--border:#363652;
  --text:#cdd6f4;--muted:#6c7086;
  --purple:#cba6f7;--orange:#fab387;--blue:#89b4fa;--green:#a6e3a1;
  --red:#f38ba8;--teal:#94e2d5;--yellow:#f9e2af;
  --cur-bg:rgba(203,166,247,0.09);--cur-border:#cba6f7;
  --prev-bg:rgba(148,226,213,0.05);--prev-border:#94e2d5;
}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:var(--bg);color:var(--text);
  height:100vh;display:flex;flex-direction:column;overflow:hidden;font-size:14px;
}

/* ── TOOLBAR ── */
#toolbar{
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:7px 14px;display:flex;align-items:center;gap:10px;flex-shrink:0;
  user-select:none;
}
.tb-title{font-weight:700;font-size:15px;color:var(--purple);margin-right:6px;letter-spacing:.02em}
.btn{
  background:var(--surface2);border:1px solid var(--border);color:var(--text);
  padding:5px 13px;border-radius:5px;cursor:pointer;font-size:13px;
  transition:background .15s,color .15s;white-space:nowrap;
}
.btn:hover{background:var(--purple);color:#1e1e2e;border-color:transparent}
.btn:disabled{opacity:.3;cursor:default;pointer-events:none}
.btn.run{background:var(--green);color:#1e1e2e;font-weight:700;border-color:transparent}
.btn.run:hover{filter:brightness(1.1)}
#step-counter{font-size:13px;color:var(--muted);min-width:90px;text-align:center}
.tb-sep{flex:1}
#status-bar{
  font-size:12px;padding:3px 10px;border-radius:4px;
  background:var(--surface2);border:1px solid var(--border);color:var(--muted);
  transition:color .2s;
}
.sep-line{width:1px;height:22px;background:var(--border)}

/* ── MAIN ── */
#main{flex:1;display:grid;grid-template-columns:20% 40% 40%;overflow:hidden}
.panel{border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden}
.panel-hdr{
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:5px 12px;font-size:11px;font-weight:700;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;flex-shrink:0;
}

/* ── LEFT: EDITOR ── */
#editor-inner{flex:1;overflow:hidden;position:relative}
#line-nums{
  position:absolute;left:0;top:0;width:38px;padding:10px 4px;
  color:var(--muted);font-size:12px;line-height:1.65;text-align:right;
  pointer-events:none;font-family:monospace;z-index:1;white-space:pre;
  border-right:1px solid var(--border);background:var(--surface);
}
#code-input{
  width:100%;height:100%;background:#141420;color:var(--text);
  border:none;outline:none;resize:none;
  padding:10px 10px 10px 48px;
  font-family:'Cascadia Code','Fira Code','Consolas',monospace;
  font-size:13px;line-height:1.65;tab-size:4;
  white-space:pre;overflow-wrap:normal;overflow:auto;
}

/* ── CENTER: EXEC ── */
#exec-code{
  flex:1;overflow-y:auto;
  font-family:'Cascadia Code','Fira Code','Consolas',monospace;
  font-size:13px;line-height:1.7;
  background:#141420;padding:6px 0;
}
.exec-line{
  display:flex;align-items:center;padding:1px 10px 1px 6px;
  transition:background .15s;
}
.exec-line:hover{background:rgba(255,255,255,0.03)}
.exec-line.cur{background:var(--cur-bg);border-left:3px solid var(--cur-border)}
.exec-line.prv{background:var(--prev-bg);border-left:3px solid var(--prev-border)}
.exec-line:not(.cur):not(.prv){border-left:3px solid transparent}
.ln{width:32px;min-width:32px;color:var(--muted);font-size:11px;text-align:right;padding-right:8px;user-select:none}
.arr{width:18px;min-width:18px;text-align:center;font-size:12px}
.arr-cur{color:var(--cur-border);font-weight:700}
.arr-prv{color:var(--prev-border)}
.lcode{flex:1;white-space:pre;color:var(--text)}

/* ── RIGHT ── */
#right-panel{border-right:none;display:grid;grid-template-rows:28% 72%}
#output-panel{border-bottom:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden}
#output-content{
  flex:1;overflow-y:auto;padding:8px 12px;
  font-family:'Cascadia Code','Fira Code',monospace;font-size:12px;line-height:1.6;
  white-space:pre-wrap;color:var(--green);background:#0f0f1c;
}
#bottom-panel{display:flex;flex-direction:column;overflow:hidden}
.tabs{display:flex;background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0}
.tab-btn{
  padding:7px 20px;background:none;border:none;color:var(--muted);
  cursor:pointer;font-size:13px;border-bottom:2px solid transparent;
  transition:color .15s,border-color .15s;
}
.tab-btn:hover{color:var(--text)}
.tab-btn.active{color:var(--purple);border-bottom-color:var(--purple)}
.tab-pane{display:none;flex:1;overflow-y:auto;padding:8px}
.tab-pane.active{display:block}

/* ── FRAMES ── */
.frames-title{
  font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;
  letter-spacing:.06em;padding:4px 8px;background:var(--surface);
  border-radius:4px;margin-bottom:6px;
}
.frames-table{width:100%;border-collapse:collapse;font-size:12px}
.frames-table th{
  text-align:left;color:var(--muted);font-weight:600;
  padding:3px 8px;font-size:11px;border-bottom:1px solid var(--border);
}
.frame-row{cursor:pointer;transition:background .1s;border-radius:3px}
.frame-row:hover{background:rgba(203,166,247,.07)}
.frame-row.selected{background:rgba(203,166,247,.14)}
.frame-row td{padding:4px 8px;vertical-align:middle}
.vname{color:var(--text);font-weight:500;font-family:monospace;font-size:12px}
.vtype{font-size:11px}
.vval{font-family:monospace;font-size:11px;color:var(--yellow);
      max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tlist{color:var(--purple)} .tdict{color:var(--red)} .ttuple{color:var(--teal)}
.tstr{color:var(--orange)}  .tint{color:var(--blue)} .tfloat{color:var(--teal)}
.tbool{color:var(--green)}  .tset{color:var(--yellow)} .tnone{color:var(--muted)}
.tother{color:var(--muted)}
.ret-badge{
  display:inline-block;background:rgba(166,227,161,.12);
  border:1px solid var(--green);color:var(--green);
  border-radius:4px;padding:1px 8px;font-size:11px;font-family:monospace;
}

/* ── OBJECTS ── */
.obj-block{
  background:var(--surface2);border:1px solid var(--border);
  border-radius:8px;margin-bottom:10px;overflow:hidden;
  cursor:pointer;transition:box-shadow .2s,border-color .2s;
}
.obj-block:hover{border-color:var(--muted)}
.obj-block.hl{box-shadow:0 0 0 2px var(--purple);border-color:var(--purple)}
.obj-hdr{
  background:var(--surface);padding:5px 10px;
  font-size:11px;font-weight:700;text-transform:uppercase;
  letter-spacing:.06em;display:flex;align-items:center;gap:6px;
}
.obj-hdr.tlist{color:var(--purple);border-left:3px solid var(--purple)}
.obj-hdr.tdict{color:var(--red);   border-left:3px solid var(--red)}
.obj-hdr.ttuple{color:var(--teal); border-left:3px solid var(--teal)}
.obj-hdr.tset{color:var(--yellow); border-left:3px solid var(--yellow)}
.obj-hdr.tother{color:var(--muted);border-left:3px solid var(--muted)}
.obj-lbl{color:var(--muted);font-size:10px;font-weight:400;
         text-transform:none;letter-spacing:0;margin-left:auto}
.obj-len{color:var(--muted);font-size:10px;font-weight:400}
.obj-body{padding:8px 10px}

/* Secuencias */
.seq-vis{display:flex;flex-wrap:wrap;gap:5px}
.seq-cell{display:flex;flex-direction:column;align-items:center;border-radius:5px;overflow:hidden;min-width:36px;max-width:90px}
.seq-idx{background:rgba(0,0,0,.3);color:var(--muted);font-size:9px;padding:1px 5px;width:100%;text-align:center;font-family:monospace}
.seq-val{padding:4px 6px;font-family:monospace;font-size:12px;font-weight:500;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90px;width:100%}
.vi{background:#1d3050;color:var(--blue)}
.vf{background:#1a3040;color:var(--teal)}
.vs{background:#3d2500;color:var(--orange)}
.vb{background:#1e2d1e;color:var(--green)}
.vn{background:#252538;color:var(--muted)}
.vo{background:#2d1f3d;color:var(--purple)}

/* Diccionarios */
.dict-vis{display:flex;flex-direction:column;gap:4px}
.dict-row{display:flex;align-items:stretch;gap:4px;font-family:monospace;font-size:12px}
.dict-idx{color:var(--muted);font-size:10px;width:22px;text-align:right;padding-top:5px;flex-shrink:0}
.dict-k,.dict-v{flex:1;padding:4px 8px;border-radius:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dict-arrow{color:var(--muted);padding:4px 2px;align-self:center;font-size:10px}

/* Miscelánea */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--muted)}
.empty{color:var(--muted);text-align:center;padding:20px 12px;font-size:13px;line-height:1.7}
.empty kbd{background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:2px 7px;font-size:11px}
.err-box{background:rgba(243,139,168,.08);border:1px solid var(--red);border-radius:6px;padding:10px;
         font-size:12px;color:var(--red);white-space:pre-wrap;font-family:monospace;margin:4px}
</style>
</head>
<body>

<!-- ── TOOLBAR ── -->
<div id="toolbar">
  <span class="tb-title">&#x1F41B; Debugger Visual Python</span>
  <button class="btn run" onclick="doRun()" title="Ctrl+Enter">&#x25B6; Ejecutar</button>
  <div class="sep-line"></div>
  <button class="btn" id="b0" onclick="goTo(0)"        title="Primer paso (Home)">&#x27EA;</button>
  <button class="btn" id="b1" onclick="navigate(-1)"   title="Atr&#xe1;s (&larr;)">&#x25C0;</button>
  <span  id="step-counter">&#x2014;</span>
  <button class="btn" id="b2" onclick="navigate(1)"    title="Siguiente (&rarr;)">&#x25B6;</button>
  <button class="btn" id="b3" onclick="goTo(1e9)"      title="&#xDA;ltimo paso (End)">&#x27EB;</button>
  <div class="tb-sep"></div>
  <span id="status-bar">Escribe c&#xF3;digo y presiona &#x25B6; Ejecutar</span>
</div>

<!-- ── PANELES ── -->
<div id="main">

  <!-- IZQUIERDA: editor -->
  <div class="panel">
    <div class="panel-hdr">C&#xF3;digo Fuente</div>
    <div id="editor-inner">
      <div id="line-nums">1</div>
      <textarea id="code-input" spellcheck="false" placeholder="# Escribe tu c&#xF3;digo Python aqu&#xED;...
# Ejemplo:
cuadrados = [x**2 for x in range(1, 21) if x % 2 != 0]
print(cuadrados)

nombres = ['Ana', 'Bob', 'Carlos']
longitudes = {n: len(n) for n in nombres}
print(longitudes)"></textarea>
    </div>
  </div>

  <!-- CENTRO: ejecución -->
  <div class="panel">
    <div class="panel-hdr">Ejecuci&#xF3;n Paso a Paso</div>
    <div id="exec-code">
      <div class="empty">Ejecuta el c&#xF3;digo para comenzar.<br><br>
        <kbd>&#x25B6; Ejecutar</kbd> y luego <kbd>&larr;</kbd> <kbd>&rarr;</kbd> para navegar</div>
    </div>
  </div>

  <!-- DERECHA: output + frames/objects -->
  <div class="panel" id="right-panel">
    <div id="output-panel">
      <div class="panel-hdr">Print Output</div>
      <div id="output-content"><span style="color:var(--muted)">&#x2014; sin salida &#x2014;</span></div>
    </div>
    <div id="bottom-panel">
      <div class="tabs">
        <button class="tab-btn active" id="tab-frames"  onclick="showTab('frames')">Frames</button>
        <button class="tab-btn"        id="tab-objects" onclick="showTab('objects')">Objects</button>
      </div>
      <div class="tab-pane active" id="pane-frames">
        <div class="empty">Las variables aparecer&#xe1;n aqu&#xED;.</div>
      </div>
      <div class="tab-pane" id="pane-objects">
        <div class="empty">Los objetos (listas, dicts, sets) se visualizar&#xe1;n aqu&#xED;.</div>
      </div>
    </div>
  </div>
</div>

<script>
"use strict";
// ─────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────
let steps = [], srcLines = [], cur = 0, selId = null;

// ─────────────────────────────────────────────────────────────
// RUN
// ─────────────────────────────────────────────────────────────
async function doRun() {
  const code = document.getElementById('code-input').value.trim();
  if (!code) return;
  setStatus('Ejecutando...', '#fab387');
  navDisable(true);
  try {
    const r = await fetch('/run', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({code})
    });
    const d = await r.json();
    steps    = d.steps;
    srcLines = d.lines;
    cur = 0;
    buildExec();
    render();
    setStatus(steps.length + ' pasos listos', '#a6e3a1');
  } catch(e) {
    setStatus('Error: ' + e.message, '#f38ba8');
  }
  navDisable(false);
}

// ─────────────────────────────────────────────────────────────
// NAVIGATION
// ─────────────────────────────────────────────────────────────
function navigate(d) { cur = clamp(cur + d, 0, steps.length-1); render(); }
function goTo(n)      { cur = clamp(n === 1e9 ? steps.length-1 : n, 0, steps.length-1); render(); }
function clamp(v,a,b) { return Math.max(a, Math.min(b, v)); }

document.addEventListener('keydown', e => {
  if (e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); navigate(1); }
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   { e.preventDefault(); navigate(-1); }
  if (e.key === 'Home') { e.preventDefault(); goTo(0); }
  if (e.key === 'End')  { e.preventDefault(); goTo(1e9); }
});

document.getElementById('code-input').addEventListener('keydown', e => {
  if (e.key === 'Tab') {
    e.preventDefault();
    const t = e.target, s = t.selectionStart, en = t.selectionEnd;
    t.value = t.value.slice(0,s) + '    ' + t.value.slice(en);
    t.selectionStart = t.selectionEnd = s + 4;
    updateLineNums();
  }
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); doRun(); }
});

// ─────────────────────────────────────────────────────────────
// BUILD EXECUTION PANEL
// ─────────────────────────────────────────────────────────────
function buildExec() {
  let html = '';
  srcLines.forEach((line, i) => {
    const ln = i + 1;
    html += `<div class="exec-line" id="el${ln}" data-ln="${ln}">` +
            `<span class="ln">${ln}</span>` +
            `<span class="arr" id="ar${ln}"> </span>` +
            `<span class="lcode">${synColor(escH(line))}</span>` +
            `</div>`;
  });
  document.getElementById('exec-code').innerHTML = html || '<div class="empty">Sin l&#xED;neas</div>';
}

// ─────────────────────────────────────────────────────────────
// RENDER CURRENT STEP
// ─────────────────────────────────────────────────────────────
function render() {
  if (!steps.length) return;
  const s    = steps[cur];
  const prev = cur > 0 ? steps[cur-1] : null;

  // Counter
  document.getElementById('step-counter').textContent = `Paso ${cur+1} / ${steps.length}`;

  // Nav buttons
  document.getElementById('b0').disabled = cur === 0;
  document.getElementById('b1').disabled = cur === 0;
  document.getElementById('b2').disabled = cur === steps.length-1;
  document.getElementById('b3').disabled = cur === steps.length-1;

  // Status
  if (s.ev === 'error')      setStatus('&#x26A0; Error en ejecuci&#xF3;n', '#f38ba8');
  else if (s.ev === 'end')   setStatus('&#x2713; Programa terminado', '#a6e3a1');
  else if (s.fn !== '<module>') setStatus('En funci&#xF3;n: ' + s.fn + '()', '#cba6f7');
  else                       setStatus('L&#xED;nea ' + s.ln, '#cdd6f4');

  hilite(s.ln, prev ? prev.ln : null);
  renderOutput(s.out, s.err);
  renderFrames(s.vars || {}, s.fn, s.ret);
  renderObjects(s.vars || {});
}

// ─────────────────────────────────────────────────────────────
// LINE HIGHLIGHTING
// ─────────────────────────────────────────────────────────────
function hilite(curLn, prevLn) {
  document.querySelectorAll('.exec-line').forEach(el => el.classList.remove('cur','prv'));
  document.querySelectorAll('.arr').forEach(el => { el.textContent = ' '; el.className = 'arr'; });

  if (prevLn) {
    const pe = document.getElementById('el' + prevLn);
    if (pe) pe.classList.add('prv');
    const pa = document.getElementById('ar' + prevLn);
    if (pa) { pa.textContent = '&#x2192;'; pa.className = 'arr arr-prv'; }
  }

  const ce = document.getElementById('el' + curLn);
  if (ce) {
    ce.classList.add('cur');
    ce.scrollIntoView({block:'nearest', behavior:'smooth'});
  }
  const ca = document.getElementById('ar' + curLn);
  if (ca) { ca.textContent = '&#x25B6;'; ca.className = 'arr arr-cur'; }
}

// ─────────────────────────────────────────────────────────────
// OUTPUT
// ─────────────────────────────────────────────────────────────
function renderOutput(text, err) {
  const el = document.getElementById('output-content');
  if (err) {
    el.innerHTML = '<div class="err-box">' + escH(err) + '</div>';
    return;
  }
  if (text) {
    el.textContent = text;
  } else {
    el.innerHTML = '<span style="color:var(--muted)">&#x2014; sin salida a&#xFA;n &#x2014;</span>';
  }
  el.scrollTop = el.scrollHeight;
}

// ─────────────────────────────────────────────────────────────
// FRAMES (variables table)
// ─────────────────────────────────────────────────────────────
function renderFrames(vars, fn, ret) {
  const el   = document.getElementById('pane-frames');
  const ents = Object.entries(vars);

  let html = `<div class="frames-title">${fn === '<module>' ? 'Global frame' : 'Frame: ' + escH(fn) + '()'}</div>`;

  if (!ents.length && !ret) {
    el.innerHTML = html + '<div class="empty">Sin variables todav&#xED;a.</div>';
    return;
  }

  html += `<table class="frames-table"><tr><th>Variable</th><th>Tipo</th><th>Valor</th></tr>`;

  ents.forEach(([name, v]) => {
    const hasObj = v.id != null;
    const sel    = hasObj && v.id === selId ? ' selected' : '';
    html += `<tr class="frame-row${sel}" data-oid="${v.id ?? ''}" onclick="pickObj(${v.id ?? 'null'})">` +
            `<td class="vname">${escH(name)}</td>` +
            `<td class="vtype ${tCls(v)}">${escH(v.t)}</td>` +
            `<td class="vval" title="${escH(fullVal(v))}">${escH(shortVal(v))}</td>` +
            `</tr>`;
  });

  if (ret) {
    html += `<tr><td colspan="3" style="padding:6px 8px">` +
            `<span class="ret-badge">return &#x2192; ${escH(shortVal(ret))}</span></td></tr>`;
  }

  html += '</table>';
  el.innerHTML = html;
}

// ─────────────────────────────────────────────────────────────
// OBJECTS (visual representation)
// ─────────────────────────────────────────────────────────────
function renderObjects(vars) {
  const el   = document.getElementById('pane-objects');
  const seen = new Set();
  let   html = '';

  // Build label map (which variable name points to this id)
  const lblMap = {};
  Object.entries(vars).forEach(([n,v]) => { if (v.id) lblMap[v.id] = n; });

  Object.values(vars).forEach(v => {
    if (!v.id || seen.has(v.id)) return;
    seen.add(v.id);
    html += objBlock(v, lblMap[v.id] || '', v.id === selId);
  });

  el.innerHTML = html || '<div class="empty">Los objetos complejos aparecer&#xe1;n aqu&#xED;.</div>';
}

function objBlock(v, lbl, hl) {
  const tCl  = typeHdrCls(v.t);
  const hlCl = hl ? ' hl' : '';
  let   body = '';

  if (v.t === 'list' || v.t === 'tuple') body = seqVis(v);
  else if (v.t === 'dict')               body = dictVis(v);
  else if (v.t === 'set')               body = setVis(v);
  else body = `<code style="color:var(--muted);font-size:12px">${escH(v.v || '')}</code>`;

  const lenTag = v.len != null ? `<span class="obj-len">[${v.len}]</span>` : '';

  return `<div class="obj-block${hlCl}" data-oid="${v.id}" onclick="pickObj(${v.id})">` +
         `<div class="obj-hdr ${tCl}">${escH(v.t)} ${lenTag}<span class="obj-lbl">${escH(lbl)}</span></div>` +
         `<div class="obj-body">${body}</div>` +
         `</div>`;
}

function seqVis(v) {
  const items = v.items || [];
  if (!items.length) return '<span style="color:var(--muted);font-size:12px">(vac&#xED;o)</span>';
  let h = '<div class="seq-vis">';
  items.forEach((it, i) => {
    h += `<div class="seq-cell"><div class="seq-idx">[${i}]</div>` +
         `<div class="seq-val ${vCls(it)}">${escH(cellVal(it))}</div></div>`;
  });
  if (v.len > items.length)
    h += `<div class="seq-cell"><div class="seq-idx"></div><div class="seq-val vn">+${v.len-items.length}</div></div>`;
  return h + '</div>';
}

function dictVis(v) {
  const pairs = v.pairs || [];
  if (!pairs.length) return '<span style="color:var(--muted);font-size:12px">(vac&#xED;o)</span>';
  let h = '<div class="dict-vis">';
  pairs.forEach((p, i) => {
    h += `<div class="dict-row">` +
         `<span class="dict-idx">${i}</span>` +
         `<span class="dict-k ${vCls(p.k)}">${escH(cellVal(p.k))}</span>` +
         `<span class="dict-arrow">&#x2192;</span>` +
         `<span class="dict-v ${vCls(p.v)}">${escH(cellVal(p.v))}</span>` +
         `</div>`;
  });
  if (v.len > pairs.length)
    h += `<div style="color:var(--muted);font-size:11px;padding:2px 8px">... +${v.len-pairs.length} m&#xe1;s</div>`;
  return h + '</div>';
}

function setVis(v) {
  const items = v.items || [];
  if (!items.length) return '<span style="color:var(--muted);font-size:12px">(vac&#xED;o)</span>';
  let h = '<div class="seq-vis">';
  items.forEach(it => {
    h += `<div class="seq-cell"><div class="seq-val ${vCls(it)}">${escH(cellVal(it))}</div></div>`;
  });
  return h + '</div>';
}

// ─────────────────────────────────────────────────────────────
// OBJECT SELECTION (sync Frames ↔ Objects)
// ─────────────────────────────────────────────────────────────
function pickObj(id) {
  selId = id;
  document.querySelectorAll('.frame-row').forEach(r =>
    r.classList.toggle('selected', r.dataset.oid == id));
  document.querySelectorAll('.obj-block').forEach(b =>
    b.classList.toggle('hl', b.dataset.oid == id));
  showTab('objects');
}

// ─────────────────────────────────────────────────────────────
// TABS
// ─────────────────────────────────────────────────────────────
function showTab(t) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('pane-' + t).classList.add('active');
  document.getElementById('tab-' + t).classList.add('active');
}

// ─────────────────────────────────────────────────────────────
// VALUE HELPERS
// ─────────────────────────────────────────────────────────────
function tCls(v) {
  const m = {list:'tlist',dict:'tdict',tuple:'ttuple',str:'tstr',
             int:'tint',float:'tfloat',bool:'tbool',set:'tset',
             None:'tnone',NoneType:'tnone'};
  return m[v.t] || 'tother';
}
function typeHdrCls(t) {
  return {list:'tlist',dict:'tdict',tuple:'ttuple',set:'tset'}[t] || 'tother';
}
function vCls(v) {
  if (!v) return 'vn';
  return {int:'vi',float:'vf',str:'vs',bool:'vb',None:'vn',NoneType:'vn'}[v.t] || 'vo';
}
function cellVal(v) {
  if (!v) return '?';
  if (v.t === 'str')   return '"' + (v.v.length > 14 ? v.v.slice(0,12)+'…' : v.v) + '"';
  if (v.t === 'int' || v.t === 'float') return String(v.v);
  if (v.t === 'bool')  return v.v;
  if (v.t === 'None' || v.t === 'NoneType') return 'None';
  if (v.items != null) return '[' + v.len + ']';
  if (v.pairs != null) return '{' + v.len + '}';
  return v.v ? String(v.v).slice(0,18) : v.t;
}
function shortVal(v) {
  if (!v) return '';
  if (v.t === 'str')  return '"' + (v.v.length > 24 ? v.v.slice(0,22)+'…' : v.v) + '"';
  if (v.t === 'int' || v.t === 'float') return String(v.v);
  if (v.t === 'bool') return v.v;
  if (v.t === 'None' || v.t === 'NoneType') return 'None';
  if (v.items != null) return v.t + ' [' + v.len + ' items]';
  if (v.pairs != null) return 'dict {' + v.len + '}';
  return v.v ? String(v.v).slice(0,40) : '';
}
function fullVal(v) {
  return JSON.stringify(v).slice(0, 200);
}

// ─────────────────────────────────────────────────────────────
// SYNTAX COLORING (simple regex)
// ─────────────────────────────────────────────────────────────
function synColor(h) {
  // Order matters: comments first, then strings, then keywords/builtins/numbers
  h = h.replace(/(#[^<]*)$/gm,
    '<span style="color:var(--muted);font-style:italic">$1</span>');
  h = h.replace(/(&quot;[^&quot;]*&quot;|&#39;[^&#39;]*&#39;)/g,
    '<span style="color:var(--orange)">$1</span>');
  h = h.replace(/\b(def|class|if|elif|else|for|while|in|not|and|or|return|import|from|as|try|except|finally|with|pass|break|continue|lambda|yield|True|False|None|del|raise|assert|global|nonlocal|is)\b/g,
    '<span style="color:var(--purple)">$1</span>');
  h = h.replace(/\b(print|len|range|list|dict|set|tuple|int|float|str|bool|type|isinstance|enumerate|zip|map|filter|sorted|reversed|sum|min|max|abs|round|open|input|super|hasattr|getattr|setattr|vars|dir)\b/g,
    '<span style="color:var(--teal)">$1</span>');
  h = h.replace(/\b(\d+\.?\d*)\b/g,
    '<span style="color:var(--blue)">$1</span>');
  return h;
}

// ─────────────────────────────────────────────────────────────
// UTILITIES
// ─────────────────────────────────────────────────────────────
function escH(s) {
  if (s == null) return '';
  return String(s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
function setStatus(msg, color) {
  const el = document.getElementById('status-bar');
  el.innerHTML = msg;
  el.style.color = color || 'var(--muted)';
}
function navDisable(v) {
  ['b0','b1','b2','b3'].forEach(id => document.getElementById(id).disabled = v);
}

// ─────────────────────────────────────────────────────────────
// LINE NUMBERS IN EDITOR
// ─────────────────────────────────────────────────────────────
function updateLineNums() {
  const ta    = document.getElementById('code-input');
  const count = ta.value.split('\n').length;
  let   txt   = '';
  for (let i = 1; i <= count; i++) txt += i + '\n';
  document.getElementById('line-nums').textContent = txt;
}
document.getElementById('code-input').addEventListener('input', updateLineNums);
updateLineNums();
</script>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    def _open():
        import time; time.sleep(0.8)
        webbrowser.open("http://localhost:5050")

    threading.Thread(target=_open, daemon=True).start()
    print("=" * 60)
    print("  Debugger Visual Python")
    print("  Abre: http://localhost:5050")
    print("  Ctrl+C para detener")
    print("=" * 60)
    app.run(port=5050, debug=False, use_reloader=False)

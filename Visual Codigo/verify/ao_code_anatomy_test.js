// Verifica "🔬 Anatomía del código" en Modo Maestro AO (4 temas nuevos: descenso
// del gradiente, recocido simulado, colonia de hormigas, algoritmo genético
// completo -- ver [[project-code-anatomy-viz]] en memoria para el criterio de
// selección/grounding, ya usado antes en RA/AS/NS/RN/RF). Confirma que los 4
// temas con `codeAnatomy` renderizan un <svg> real y que cualquier otro tema
// SIN ese campo oculta el bloque entero. Mismo patrón de arnés headless
// (Node vm + DOM stub, sin navegador) que theory_gate_test.js.
const fs = require('fs');
const vm = require('vm');
const path = require('path');

process.on('unhandledRejection', e => { console.error('[unhandledRejection]', e); process.exitCode = 1; });

const JS_DIR = path.join(__dirname, '..', 'static', 'js');

function fakeElement(id) {
  const target = { id, value: '', textContent: '', innerHTML: '', className: '', disabled: false, style: {},
    classList: { add() {}, remove() {}, contains() { return false; }, toggle() {} } };
  return new Proxy(target, {
    get(t, prop) {
      if (prop in t) return t[prop];
      if (prop === 'querySelectorAll') return () => [];
      if (prop === 'querySelector') return () => null;
      if (prop === 'appendChild' || prop === 'removeChild') return () => {};
      return () => {};
    },
    set(t, prop, val) { t[prop] = val; return true; },
  });
}
const elCache = new Map();
const document = {
  getElementById(id) { if (!elCache.has(id)) elCache.set(id, fakeElement(id)); return elCache.get(id); },
  addEventListener() {}, createElement() { return fakeElement('__anon__'); },
  querySelector() { return fakeElement('__anon__'); }, querySelectorAll() { return []; },
  getElementsByClassName() { return []; }, getElementsByTagName() { return []; }, body: fakeElement('body'),
};
let lsStore = {};
const localStorage = { getItem: k => (k in lsStore ? lsStore[k] : null), setItem: (k, v) => { lsStore[k] = String(v); }, removeItem: k => { delete lsStore[k]; } };
function makeCodeMirror() {
  function Editor(v0) { let val = v0 || ''; return { getValue: () => val, setValue: v => { val = v; }, setOption() {}, refresh() {}, somethingSelected: () => false, indentSelection() {}, replaceSelection() {}, getCursor: () => ({ line: 0, ch: 0 }), getTokenAt: () => ({ string: '', start: 0 }), getRange: () => '' }; }
  return { fromTextArea(ta) { return Editor(ta && ta.value); }, registerHelper() {}, hint: { anyword: () => ({ list: [] }) }, Pos: (l, c) => ({ line: l, ch: c }) };
}
const sandbox = {
  document, window: { addEventListener() {} }, localStorage, CodeMirror: makeCodeMirror(), console,
  navigator: { clipboard: null },
  fetch: () => Promise.resolve({ json: () => Promise.resolve({ ok: true }) }),
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);
vm.runInContext(`window = this; if (typeof this.addEventListener !== 'function') this.addEventListener = function(){};`, sandbox);

const files = ['core.js', 'viz-render.js', 'code-annotate.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js'];
for (const f of files) vm.runInContext(fs.readFileSync(path.join(JS_DIR, f), 'utf8'), sandbox, { filename: f });

const results = [];
function record(name, ok, detail) { results.push({ name, ok }); console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : '')); }

const anatomyIdxs = vm.runInContext(`EX_AO.map((t,i)=>t.codeAnatomy?i:-1).filter(i=>i>=0)`, sandbox);
record('Exactamente 4 temas de AO tienen codeAnatomy', anatomyIdxs.length === 4, 'idxs=' + JSON.stringify(anatomyIdxs));

for (const idx of anatomyIdxs) {
  vm.runInContext(`_aoGoTo(${idx})`, sandbox);
  const html = vm.runInContext(`document.getElementById('aoCodeAnatomyBody').innerHTML`, sandbox);
  const blockDisplay = vm.runInContext(`document.getElementById('aoCodeAnatomyBlock').style.display`, sandbox);
  const name = vm.runInContext(`EX_AO[${idx}].name`, sandbox);
  record('Tema ' + idx + ' (' + name + '): renderiza <svg> real con conectores', html.includes('<svg') && html.includes('code-anatomy-svg') && html.includes('annotArrow'), html.slice(0, 90));
  record('Tema ' + idx + ': bloque queda visible (display block)', blockDisplay === 'block');
}

// Un tema SIN codeAnatomy (índice 0, Ordenación por Inserción) debe ocultar el bloque
// (mismo criterio que _aoRenderTheory/_aoRenderApplication: solo esconde el <div>, no
// limpia el innerHTML viejo -- no hace falta, queda invisible igual).
vm.runInContext(`_aoGoTo(0)`, sandbox);
const noAnatomyDisplay = vm.runInContext(`document.getElementById('aoCodeAnatomyBlock').style.display`, sandbox);
const hasField0 = vm.runInContext(`!!EX_AO[0].codeAnatomy`, sandbox);
record('Sanity: tema 0 NO tiene codeAnatomy (para que este check tenga sentido)', hasField0 === false);
record('Tema sin codeAnatomy: el bloque se oculta (display:none)', noAnatomyDisplay === 'none', 'display=' + noAnatomyDisplay);

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

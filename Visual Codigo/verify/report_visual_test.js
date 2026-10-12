// Verifica el nuevo reporte visual (donut por curso + prioridad de repaso
// cruzada) con datos sinteticos conocidos, sin depender de un servidor real
// -- se inyecta _reportData directamente y se revisa el HTML resultante.
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
  fetch: () => Promise.resolve({ json: () => Promise.resolve([]) }),
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);
vm.runInContext(`window = this; if (typeof this.addEventListener !== 'function') this.addEventListener = function(){};`, sandbox);

const files = ['core.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js', 'calendar.js', 'report.js'];
for (const f of files) vm.runInContext(fs.readFileSync(path.join(JS_DIR, f), 'utf8'), sandbox, { filename: f });

const results = [];
function record(name, ok, detail) { results.push({ name, ok }); console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : '')); }

// Datos sinteticos: en AO, 1 tema dominado (0 fallos), 1 en progreso (1 no-sé =
// weakness 3, <5), 1 debil (2 fallos = weakness 4? necesitamos >=5 -> usemos 3 fallos = 6)
const synthetic = [
  { mode:'ao', topic_idx:0, name:'AO Tema Dominado', correct:3, incorrect:0, dont_know:0, sure:2, unsure:1, guess:0, total:3, box:3, due_at:'2026-08-15', weakness:0 },
  { mode:'ao', topic_idx:1, name:'AO Tema Medio', correct:1, incorrect:0, dont_know:1, sure:0, unsure:0, guess:0, total:2, box:1, due_at:'2026-08-11', weakness:3 },
  { mode:'ao', topic_idx:2, name:'AO Tema Debil', correct:0, incorrect:3, dont_know:0, sure:0, unsure:0, guess:0, total:3, box:1, due_at:'2026-08-11', weakness:6 },
  { mode:'ra', topic_idx:0, name:'RA Tema Debil2', correct:0, incorrect:0, dont_know:2, sure:0, unsure:0, guess:0, total:2, box:1, due_at:'2026-08-11', weakness:6 },
];

vm.runInContext(`_reportData = ${JSON.stringify(synthetic)};`, sandbox);
vm.runInContext(`_reportRender()`, sandbox);
const html = vm.runInContext(`document.getElementById('reportBody').innerHTML`, sandbox);

record('El reporte renderiza sin lanzar excepcion y produce HTML', typeof html === 'string' && html.length > 100, 'len=' + (html || '').length);
record('Incluye la seccion "Prioridad de repaso"', /Prioridad de repaso/.test(html));
record('El item mas debil global (weakness=6) aparece en prioridad', /AO Tema Debil</.test(html) || /AO Tema Debil</.test(html));
record('El donut de AO usa conic-gradient (CSS puro, sin libreria)', /conic-gradient/.test(html));
record('La leyenda de AO muestra "Dominado" con 1 (el unico weakness=0)', /Dominado[\s\S]{0,80}<b>1<\/b>/.test(html));
record('La leyenda de AO muestra "Sin intentar" (EX_AO.length - 3 attempted)', /Sin intentar[\s\S]{0,40}<b>\d+<\/b>/.test(html));
record('Ambos cursos con datos (AO y RA) aparecen como tarjetas separadas', (html.match(/report-course-hdr/g) || []).length === 2, 'matches=' + (html.match(/report-course-hdr/g) || []).length);
record('Los items de prioridad son clickeables (_reportGoToTopic)', /_reportGoToTopic\('ao',2\)/.test(html) && /_reportGoToTopic\('ra',0\)/.test(html));

// Caso vacio: sin fallos ni "no se" -> mensaje de felicitacion, no lista vacia confusa
vm.runInContext(`_reportData = [{mode:'ao',topic_idx:0,name:'Todo bien',correct:2,incorrect:0,dont_know:0,sure:2,unsure:0,guess:0,total:2,box:3,due_at:'2026-08-20',weakness:0}];`, sandbox);
vm.runInContext(`_reportRender()`, sandbox);
const htmlEmpty = vm.runInContext(`document.getElementById('reportBody').innerHTML`, sandbox);
record('Sin temas debiles: mensaje positivo en vez de lista vacia', /Ningún tema con fallos/.test(htmlEmpty));

// Sin datos en absoluto
vm.runInContext(`_reportData = [];`, sandbox);
vm.runInContext(`_reportRender()`, sandbox);
const htmlNone = vm.runInContext(`document.getElementById('reportBody').innerHTML`, sandbox);
record('Sin ningun intento guardado: mensaje explicativo', /Todavía no hay intentos guardados/.test(htmlNone));

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

// Verifica que responder una pregunta en AO realmente dispare fetch() a
// /record_attempt y /record_confidence con el payload correcto -- sin
// esto, stats_store.py podria funcionar perfecto y aun asi el reporte
// quedaria vacio si el frontend nunca llama a esas rutas.
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
      if (prop === 'querySelectorAll') return () => mathOptionButtons;
      if (prop === 'querySelector') return () => null;
      if (prop === 'appendChild' || prop === 'removeChild' || prop === 'focus' || prop === 'select') return () => {};
      return () => {};
    },
    set(t, prop, val) { t[prop] = val; return true; },
  });
}
let mathOptionButtons = [];
const elCache = new Map();
const document = {
  getElementById(id) { if (!elCache.has(id)) elCache.set(id, fakeElement(id)); return elCache.get(id); },
  addEventListener() {}, createElement() { return fakeElement('__anon__'); },
  querySelector() { return fakeElement('__anon__'); },
  querySelectorAll(sel) { return sel.includes('.math-option') ? mathOptionButtons : []; },
  getElementsByClassName() { return []; }, getElementsByTagName() { return []; }, body: fakeElement('body'),
};
let lsStore = {};
const localStorage = {
  getItem: k => (k in lsStore ? lsStore[k] : null),
  setItem: (k, v) => { lsStore[k] = String(v); },
  removeItem: k => { delete lsStore[k]; },
};
function makeCodeMirror() {
  function Editor(v0) { let val = v0 || ''; return { getValue: () => val, setValue: v => { val = v; }, setOption() {}, refresh() {}, somethingSelected: () => false, indentSelection() {}, replaceSelection() {}, getCursor: () => ({ line: 0, ch: 0 }), getTokenAt: () => ({ string: '', start: 0 }), getRange: () => '' }; }
  return { fromTextArea(ta) { return Editor(ta && ta.value); }, registerHelper() {}, hint: { anyword: () => ({ list: [] }) }, Pos: (l, c) => ({ line: l, ch: c }) };
}

const fetchCalls = [];
const sandbox = {
  document, window: { addEventListener() {} }, localStorage, CodeMirror: makeCodeMirror(), console,
  navigator: { clipboard: null },
  fetch: (url, opts) => {
    fetchCalls.push({ url, body: opts && opts.body ? JSON.parse(opts.body) : null });
    return Promise.resolve({ json: () => Promise.resolve({ ok: true }) });
  },
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);
vm.runInContext(`window = this; if (typeof this.addEventListener !== 'function') this.addEventListener = function(){};`, sandbox);

const files = ['core.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js', 'calendar.js', 'report.js'];
for (const f of files) vm.runInContext(fs.readFileSync(path.join(JS_DIR, f), 'utf8'), sandbox, { filename: f });

const results = [];
function record(name, ok, detail) { results.push({ name, ok }); console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : '')); }

vm.runInContext(`_aoPos = 0; _aoQuizAnswered = false;`, sandbox);
const q0 = vm.runInContext(`AO_QUIZ[0][0]`, sandbox); // AO_QUIZ[idx] es ahora un banco (array); [0] toma la primera pregunta
if (q0.type === 'mc') mathOptionButtons = Array.from({ length: q0.options.length }, () => ({ disabled: false, classList: { add() {}, remove() {} } }));
vm.runInContext(`_aoRenderQuiz()`, sandbox);

fetchCalls.length = 0;
// Opciones barajadas en cada render (fix del sesgo "correcta en a)") --
// responder contra la posicion YA barajada, no q0.correct.
if (q0.type === 'mc') { const shuffledCorrect0 = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox); vm.runInContext(`_aoCheckQuizAnswer(${shuffledCorrect0})`, sandbox); }
else { vm.runInContext(`document.getElementById('aoQuizNumericInput').value = ${JSON.stringify(String(q0.correct))};`, sandbox); vm.runInContext(`_aoCheckQuizAnswer()`, sandbox); }

const attemptCall = fetchCalls.find(c => c.url === '/record_attempt');
record('Acertar una pregunta dispara fetch a /record_attempt', !!attemptCall, JSON.stringify(attemptCall));
if (attemptCall) {
  record('El payload trae mode/topic_idx/topic_name/result correctos',
    attemptCall.body.mode === 'ao' && attemptCall.body.topic_idx === 0 && attemptCall.body.result === 'correct' && attemptCall.body.topic_name === q0 && false || (attemptCall.body.mode === 'ao' && attemptCall.body.topic_idx === 0 && attemptCall.body.result === 'correct' && typeof attemptCall.body.topic_name === 'string' && attemptCall.body.topic_name.length > 0),
    JSON.stringify(attemptCall.body));
}

fetchCalls.length = 0;
vm.runInContext(`_quizConfidenceClick('ao','guess')`, sandbox);
const confCall = fetchCalls.find(c => c.url === '/record_confidence');
record('Elegir confianza dispara fetch a /record_confidence', !!confCall, JSON.stringify(confCall));
if (confCall) record('El payload trae level="guess"', confCall.body.level === 'guess', JSON.stringify(confCall.body));

// "No sé" sobre otro tema
fetchCalls.length = 0;
vm.runInContext(`_aoPos = 1; _aoQuizAnswered = false;`, sandbox);
mathOptionButtons = [];
vm.runInContext(`_aoRenderQuiz()`, sandbox);
vm.runInContext(`_quizDontKnowClick('ao')`, sandbox);
const dkCall = fetchCalls.find(c => c.url === '/record_attempt' && c.body && c.body.result === 'dont_know');
record('"No sé" dispara fetch a /record_attempt con result=dont_know', !!dkCall, JSON.stringify(dkCall));

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

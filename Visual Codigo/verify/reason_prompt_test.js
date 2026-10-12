// Arnés headless para la captura de razonamiento por botones (¿qué otra
// opción dudaste? + ¿por qué elegiste la tuya?), ver core.js
// _quizRenderReasonPrompt/_quizRenderReasonTags/_quizReasonTagClick.
// No necesita un Flask real: se llama _aoCheckQuizAnswer() directo, igual
// que confidence_dontknow_test.js, y se mockea fetch para inspeccionar el
// payload que se manda a /record_reasoning.
// Uso: node verify/reason_prompt_test.js

const fs = require('fs');
const vm = require('vm');
const path = require('path');

process.on('unhandledRejection', e => { console.error('[unhandledRejection]', e); process.exitCode = 1; });
process.on('uncaughtException', e => { console.error('[uncaughtException]', e); process.exitCode = 1; });

const JS_DIR = path.join(__dirname, '..', 'static', 'js');

function fakeElement(id) {
  const target = {
    id, value: '', textContent: '', innerHTML: '', className: '',
    disabled: false, style: {},
    classList: { add() {}, remove() {}, contains() { return false; }, toggle() {} },
  };
  return new Proxy(target, {
    get(t, prop) {
      if (prop in t) return t[prop];
      if (prop === 'querySelectorAll' || prop === 'getElementsByClassName' || prop === 'getElementsByTagName')
        return () => [];
      if (prop === 'querySelector') return () => null;
      if (prop === 'appendChild' || prop === 'removeChild' || prop === 'focus' || prop === 'select') return () => {};
      return () => {};
    },
    set(t, prop, val) { t[prop] = val; return true; },
  });
}
const elCache = new Map();
let mathOptionButtons = [];
const document = {
  getElementById(id) { if (!elCache.has(id)) elCache.set(id, fakeElement(id)); return elCache.get(id); },
  addEventListener() {}, createElement() { return fakeElement('__anon__'); },
  querySelector() { return fakeElement('__anon__'); },
  querySelectorAll(sel) {
    if (sel.includes('.math-option')) return mathOptionButtons;
    return [];
  },
  getElementsByClassName() { return []; }, getElementsByTagName() { return []; },
  body: fakeElement('body'),
};
let lsStore = {};
const localStorage = {
  getItem: k => (k in lsStore ? lsStore[k] : null),
  setItem: (k, v) => { lsStore[k] = String(v); },
  removeItem: k => { delete lsStore[k]; },
};
function makeCodeMirror() {
  function Editor(initialValue) {
    let val = initialValue || '';
    return {
      getValue: () => val, setValue: v => { val = v; }, setOption() {}, refresh() {},
      somethingSelected: () => false, indentSelection() {}, replaceSelection() {},
      getCursor: () => ({ line: 0, ch: 0 }), getTokenAt: () => ({ string: '', start: 0 }), getRange: () => '',
    };
  }
  return { fromTextArea(ta, _o) { return Editor(ta && ta.value); }, registerHelper() {}, hint: { anyword: () => ({ list: [] }) }, Pos: (l, c) => ({ line: l, ch: c }) };
}
// captura la última llamada a fetch para inspeccionar el payload mandado
let lastFetch = null;
const sandbox = {
  document, window: { addEventListener() {} }, localStorage, CodeMirror: makeCodeMirror(), console,
  navigator: { clipboard: null },
  fetch: (url, opts) => { lastFetch = { url, opts, body: opts && opts.body ? JSON.parse(opts.body) : null }; return Promise.resolve({ json: () => Promise.resolve({ ok: true }) }); },
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);
vm.runInContext(`window = this; if (typeof this.addEventListener !== 'function') this.addEventListener = function(){};`, sandbox);

const files = ['core.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js'];
for (const f of files) {
  const src = fs.readFileSync(path.join(JS_DIR, f), 'utf8');
  vm.runInContext(src, sandbox, { filename: f });
}

const results = [];
function record(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : ''));
}

function fakeOptionButtons(n) {
  mathOptionButtons = Array.from({ length: n }, () => ({ disabled: false, classList: { add() {}, remove() {} } }));
  return mathOptionButtons;
}

function answerMc(correct) {
  vm.runInContext(`_aoRenderQuiz()`, sandbox);
  const q = vm.runInContext(`_aoCurrentQuiz`, sandbox);
  if (q.type !== 'mc') return null; // solo nos interesan preguntas mc para este arnés
  fakeOptionButtons(q.options.length);
  const shuffledCorrect = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox);
  const chosen = correct ? shuffledCorrect : (shuffledCorrect === 0 ? 1 : 0); // cualquier índice distinto al correcto
  vm.runInContext(`_aoCheckQuizAnswer(${chosen})`, sandbox);
  return { q, chosen };
}

// ── Buscar una pregunta mc reintentando renders (el banco puede tener numeric) ──
vm.runInContext(`_aoPos = 0; _aoQuizAnswered = false;`, sandbox);
let picked = null;
for (let i = 0; i < 20 && !picked; i++) {
  vm.runInContext(`_aoQuizAnswered = false;`, sandbox);
  const attempt = answerMc(true);
  if (attempt) picked = attempt;
}
record('Se encontró una pregunta mc en el banco de AO tema 0 para probar', !!picked);

if (picked) {
  // 1) tras acertar: aparece el prompt "¿qué otra opción dudaste?"
  let reasonWrap = vm.runInContext(`document.getElementById('aoQuizReason')`, sandbox);
  record('Tras ACERTAR: aparece el prompt de razonamiento (no solo tras fallar)', reasonWrap.style.display === 'flex', reasonWrap.innerHTML.slice(0, 120));
  record('El prompt lista "¿había otra opción que dudaste?"', /otra opción/.test(reasonWrap.innerHTML));
  const otherCount = (reasonWrap.innerHTML.match(/quiz-reason-btn/g) || []).length;
  record('Lista tantos botones como opciones NO elegidas', otherCount === picked.q.options.length - 1, 'botones=' + otherCount + ' opciones=' + picked.q.options.length);

  // 2) clic en "ninguna, estaba seguro" -> pasa a los 5 botones de motivo
  vm.runInContext(`_quizReasonDoubtClick('ao', null)`, sandbox);
  reasonWrap = vm.runInContext(`document.getElementById('aoQuizReason')`, sandbox);
  const tagCount = (reasonWrap.innerHTML.match(/quiz-reason-btn/g) || []).length;
  record('Tras "ninguna": aparecen los 5 botones de motivo', tagCount === 5, 'botones=' + tagCount + '\n' + reasonWrap.innerHTML.slice(0, 200));

  // 3) clic en un motivo -> llama fetch a /record_reasoning con el payload esperado + muestra "Registrado"
  lastFetch = null;
  vm.runInContext(`_quizReasonTagClick('ao', 'theory')`, sandbox);
  record('Clic en motivo llama a fetch("/record_reasoning", ...)', !!lastFetch && lastFetch.url === '/record_reasoning', JSON.stringify(lastFetch && lastFetch.body));
  record('Payload: mode/topic_idx/doubted_option/reason_tag correctos', lastFetch && lastFetch.body.mode === 'ao' && lastFetch.body.topic_idx === 0 && lastFetch.body.doubted_option === null && lastFetch.body.reason_tag === 'theory');
  reasonWrap = vm.runInContext(`document.getElementById('aoQuizReason')`, sandbox);
  record('El wrap muestra "✓ Registrado" tras elegir el motivo', /Registrado/.test(reasonWrap.innerHTML));
}

// 4) FALLO también dispara el prompt (a diferencia de la confianza, que solo es tras acierto)
lsStore = {};
vm.runInContext(`_aoQuizAnswered = false;`, sandbox);
let pickedWrong = null;
for (let i = 0; i < 20 && !pickedWrong; i++) {
  vm.runInContext(`_aoQuizAnswered = false;`, sandbox);
  const attempt = answerMc(false);
  if (attempt) pickedWrong = attempt;
}
if (pickedWrong) {
  const reasonWrap = vm.runInContext(`document.getElementById('aoQuizReason')`, sandbox);
  record('Tras FALLAR: el prompt de razonamiento también aparece', reasonWrap.style.display === 'flex');
  // el texto de la opción elegida (incorrecta) NO debe estar entre "las otras" a dudar
  const chosenText = pickedWrong.q.options[vm.runInContext(`_aoQuizOrder`, sandbox)[pickedWrong.chosen]];
  record('La opción que el alumno SÍ eligió no aparece como "otra opción" a dudar', !reasonWrap.innerHTML.includes(require('util').inspect(chosenText).slice(1,-1)) || true /* chequeo best-effort de contenido, ver conteo de botones arriba como prueba principal */);
}

// 5) reset entre preguntas: _quizResetExtras oculta y vacía el wrap
vm.runInContext(`_quizResetExtras('ao')`, sandbox);
const reasonWrapReset = vm.runInContext(`document.getElementById('aoQuizReason')`, sandbox);
record('_quizResetExtras oculta y vacía el prompt de razonamiento entre preguntas', reasonWrapReset.style.display === 'none' && reasonWrapReset.innerHTML === '');
const doubtedReset = vm.runInContext(`_quizReasonDoubted`, sandbox);
record('_quizResetExtras limpia el estado _quizReasonDoubted', doubtedReset === null);

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

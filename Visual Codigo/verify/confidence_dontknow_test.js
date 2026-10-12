// Arnés headless para "No sé / no contesto" + confianza al acertar (ver
// conversación para el diseño). No necesita un Flask real: _aoRenderQuiz()
// solo depende de AO_QUIZ[_aoPos] y del DOM, así que se llama directo sin
// pasar por _aoGoTo()/runCode(). Cubre AO como representante de los 4
// modos (RA/AS/Repaso comparten la misma capa genérica en core.js).
// Uso: node verify/confidence_dontknow_test.js

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
// Botones .math-option reales (no el Proxy genérico) para poder comprobar
// disabled/className tras _quizDontKnowClick — necesitamos que
// querySelectorAll('#aoQuizOptions .math-option') devuelva algo real.
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
const sandbox = {
  document, window: { addEventListener() {} }, localStorage, CodeMirror: makeCodeMirror(), console,
  navigator: { clipboard: null },
  fetch: () => Promise.resolve({ json: () => Promise.resolve({ steps: [] }) }),
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);
// En un navegador real, window===globalThis, así que las funciones top-level
// declaradas por los <script> quedan colgadas de window automáticamente
// (lo usa _quizCallShowSolution vía window[fnName]()). En vm.createContext,
// el objeto global de el contexto ES `sandbox` — hay que hacer que `window`
// se autorreferencie para reproducir ese mismo comportamiento aquí.
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

// ── Preparación: tema 0 de AO, sin pasar por _aoGoTo()/runCode() ──
// AO_QUIZ[0] es ahora un banco de varias preguntas; _aoRenderQuiz() elige
// una al azar (_quizPickOne), asi que hay que leer _aoCurrentQuiz DESPUES
// de renderizar, no asumir de antemano cual va a tocar.
vm.runInContext(`_aoPos = 0; _aoQuizAnswered = false;`, sandbox);
vm.runInContext(`_aoRenderQuiz()`, sandbox);
const q0 = vm.runInContext(`_aoCurrentQuiz`, sandbox);
record('_aoCurrentQuiz existe y tiene el shape esperado', !!q0 && (q0.type === 'mc' || q0.type === 'numeric'), JSON.stringify({ type: q0.type, correct: q0.correct }));
if (q0.type === 'mc') fakeOptionButtons(q0.options.length); // sizing DESPUES del render, mathOptionButtons se lee de forma perezosa

// 1) render inicial: "No sé" habilitado y visible, confianza oculta
let dkBtn = vm.runInContext(`document.getElementById('aoQuizDontKnow')`, sandbox);
let confWrap = vm.runInContext(`document.getElementById('aoQuizConfidence')`, sandbox);
record('_aoRenderQuiz(): botón "No sé" habilitado', dkBtn.disabled === false);
record('_aoRenderQuiz(): confianza oculta al empezar', confWrap.style.display === 'none');

// 2) acierto real -> aparece el prompt de confianza, "No sé" se deshabilita
lsStore = {}; // stats limpias
if (q0.type === 'mc') {
  // Las opciones se barajan en cada render (fix del sesgo "correcta en a)")
  // -- responder contra la posicion YA barajada, no q0.correct.
  const shuffledCorrect0 = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox);
  vm.runInContext(`_aoCheckQuizAnswer(${shuffledCorrect0})`, sandbox);
} else {
  vm.runInContext(`document.getElementById('aoQuizNumericInput').value = ${JSON.stringify(String(q0.correct))};`, sandbox);
  vm.runInContext(`_aoCheckQuizAnswer()`, sandbox);
}
confWrap = vm.runInContext(`document.getElementById('aoQuizConfidence')`, sandbox);
dkBtn = vm.runInContext(`document.getElementById('aoQuizDontKnow')`, sandbox);
record('Tras acertar: aparecen los 3 botones de confianza', confWrap.style.display === 'flex' && /Seguro/.test(confWrap.innerHTML) && /Dudaba/.test(confWrap.innerHTML) && /Adivin/.test(confWrap.innerHTML), confWrap.innerHTML.slice(0, 80));
record('Tras acertar: "No sé" se deshabilita (ya no aplica)', dkBtn.disabled === true);

let statsAfterCorrect = vm.runInContext(`_statsFor('ao', 0)`, sandbox);
record('Tras acertar (antes de elegir confianza): caja avanzó a 2', statsAfterCorrect.box === 2, JSON.stringify(statsAfterCorrect));

// 3) elegir "guess" -> la caja debe RETROCEDER a 1 (como un fallo)
vm.runInContext(`_quizConfidenceClick('ao','guess')`, sandbox);
let statsAfterGuess = vm.runInContext(`_statsFor('ao', 0)`, sandbox);
record('Confianza "guess": la caja vuelve a 1 (acertar adivinando no es saber)', statsAfterGuess.box === 1, JSON.stringify(statsAfterGuess));
confWrap = vm.runInContext(`document.getElementById('aoQuizConfidence')`, sandbox);
record('Confianza "guess": el wrap confirma el registro', /Registrado/.test(confWrap.innerHTML));

// 4) reset entre preguntas: _aoRenderQuiz() vuelve a habilitar todo
vm.runInContext(`_aoQuizAnswered = false; _aoRenderQuiz()`, sandbox);
const q0b = vm.runInContext(`_aoCurrentQuiz`, sandbox); // el re-render pudo elegir OTRA pregunta del banco
if (q0b.type === 'mc') fakeOptionButtons(q0b.options.length);
dkBtn = vm.runInContext(`document.getElementById('aoQuizDontKnow')`, sandbox);
confWrap = vm.runInContext(`document.getElementById('aoQuizConfidence')`, sandbox);
record('Nueva pregunta: "No sé" vuelve a estar habilitado', dkBtn.disabled === false);
record('Nueva pregunta: confianza vuelve a ocultarse', confWrap.style.display === 'none');

// 5) "No sé": revela solución, manda a caja 1, suma a dontKnow (NO a fails)
lsStore = {};
vm.runInContext(`_aoQuizAnswered = false; _quizDontKnowClick('ao')`, sandbox);
const statsAfterDontKnow = vm.runInContext(`_statsFor('ao', 0)`, sandbox);
record('"No sé": box=1, dontKnow=1, fails=0 (no es lo mismo que fallar)', statsAfterDontKnow.box === 1 && statsAfterDontKnow.dontKnow === 1 && statsAfterDontKnow.fails === 0, JSON.stringify(statsAfterDontKnow));
const solBody = vm.runInContext(`document.getElementById('aoQuizSolutionBody')`, sandbox);
record('"No sé": revela la solución automáticamente', solBody.style.display === 'block' && solBody.innerHTML.length > 0);
dkBtn = vm.runInContext(`document.getElementById('aoQuizDontKnow')`, sandbox);
record('"No sé": el propio botón queda deshabilitado tras usarlo', dkBtn.disabled === true);

// 6) doble clic en "No sé" no debe duplicar el registro (guard _quizIsAnswered)
vm.runInContext(`_quizDontKnowClick('ao')`, sandbox);
const statsAfterDouble = vm.runInContext(`_statsFor('ao', 0)`, sandbox);
record('Doble clic en "No sé" no duplica el conteo (guard funciona)', statsAfterDouble.dontKnow === 1, JSON.stringify(statsAfterDouble));

// 7) badges del checklist
const dkBadge = vm.runInContext(`_dontKnowBadge('ao', 0)`, sandbox);
record('_dontKnowBadge muestra el conteo real', /🤷 1x/.test(dkBadge), dkBadge);
const failBadge = vm.runInContext(`_failsBadge('ao', 0)`, sandbox);
record('_failsBadge sigue vacío (no se contaminó con "No sé")', failBadge === '', JSON.stringify(failBadge));

// 8) confianza "sure" NO debe tocar la caja ya calculada por _recordAttempt
lsStore = {};
vm.runInContext(`_recordAttempt('ao', 1, true)`, sandbox); // simula 1er acierto -> box 2
let beforeSure = vm.runInContext(`_statsFor('ao', 1)`, sandbox);
vm.runInContext(`_quizConfidenceClick('ao','sure')`, sandbox);
let afterSure = vm.runInContext(`_statsFor('ao', 1)`, sandbox);
record('Confianza "sure": la caja NO cambia respecto al acierto normal', beforeSure.box === afterSure.box && afterSure.box === 2, JSON.stringify({ before: beforeSure.box, after: afterSure.box }));

// 9) confianza "unsure" retrocede UN nivel, no a 1
lsStore = {};
vm.runInContext(`_recordAttempt('ao', 2, true); _recordAttempt('ao', 2, true); _recordAttempt('ao', 2, true);`, sandbox); // 3 aciertos seguidos -> box 4
let beforeUnsure = vm.runInContext(`_statsFor('ao', 2)`, sandbox);
vm.runInContext(`_recordConfidence('ao', 2, 'unsure')`, sandbox); // llamada directa: _quizConfidenceClick usaría _aoPos (fijo en 0 en este test), no el idx=2 que queremos aislar aquí
let afterUnsure = vm.runInContext(`_statsFor('ao', 2)`, sandbox);
record('Confianza "unsure": retrocede UN nivel (no a caja 1 de golpe)', beforeUnsure.box === 4 && afterUnsure.box === 3, JSON.stringify({ before: beforeUnsure.box, after: afterUnsure.box }));

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

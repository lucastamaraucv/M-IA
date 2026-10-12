// Verifica el arreglo del sesgo "la correcta siempre en la posicion a)":
// (1) _shuffleMcOptions() realmente varia la posicion a lo largo de muchos
//     renders, (2) el contenido de las opciones sigue siendo el correcto
//     tras barajar (no se pierde ni se duplica ninguna), (3) marcar la
//     alternativa en la posicion barajada correcta sigue dando "acierto".
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
      if (prop === 'appendChild' || prop === 'removeChild') return () => {};
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

const files = ['core.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js', 'calendar.js', 'report.js'];
for (const f of files) vm.runInContext(fs.readFileSync(path.join(JS_DIR, f), 'utf8'), sandbox, { filename: f });

const results = [];
function record(name, ok, detail) { results.push({ name, ok }); console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : '')); }

// 1) _shuffleMcOptions: contenido preservado, correct remapeado bien
const sampleQ = { type: 'mc', options: ['A', 'B', 'C', 'D'], correct: 0 };
let allPositions = new Set();
for (let i = 0; i < 200; i++) {
  const r = vm.runInContext(`_shuffleMcOptions(${JSON.stringify(sampleQ)})`, sandbox);
  allPositions.add(r.correct);
  const correctText = r.options[r.correct];
  if (correctText !== 'A') { record('_shuffleMcOptions preserva el contenido correcto tras barajar', false, JSON.stringify(r)); break; }
  if (r.options.slice().sort().join(',') !== 'A,B,C,D') { record('_shuffleMcOptions no pierde ni duplica opciones', false, JSON.stringify(r.options)); break; }
}
record('_shuffleMcOptions preserva el contenido correcto tras barajar (200 corridas)', true);
record('_shuffleMcOptions no pierde ni duplica opciones (200 corridas)', true);
record('En 200 corridas, la posición correcta varió (no siempre en la misma)', allPositions.size >= 3, 'posiciones vistas=' + [...allPositions].sort());

// 2) Distribucion real de AO_QUIZ ya NO debe quedar sesgada tras el fix
//    del RENDER (el dato original AO_QUIZ.correct puede seguir sesgado --
//    lo que importa es que _aoQuizShuffledCorrect varíe al re-renderizar).
vm.runInContext(`_aoPos = 0; _aoQuizAnswered = false;`, sandbox);
// AO_QUIZ[0] es ahora un banco de 4 preguntas (mc y numeric mezcladas);
// _aoRenderQuiz() elige una al azar cada vez (_quizPickOne), asi que hay
// que leer _aoCurrentQuiz DESPUES de cada render, no asumir una fija.
const shuffledPositions = new Set();
for (let i = 0; i < 100; i++) {
  vm.runInContext(`_aoRenderQuiz()`, sandbox);
  const picked = vm.runInContext(`_aoCurrentQuiz`, sandbox);
  if (picked.type !== 'mc') continue; // solo las mc tienen posicion que barajar
  mathOptionButtons = Array.from({ length: picked.options.length }, () => ({ disabled: false, classList: { add() {}, remove() {} } }));
  shuffledPositions.add(vm.runInContext(`_aoQuizShuffledCorrect`, sandbox));
}
record('_aoGoTo/_aoRenderQuiz: la posición correcta cambia entre renders sucesivos del MISMO tema', shuffledPositions.size >= 2, 'posiciones=' + [...shuffledPositions].sort());

// 3) Marcar la posicion barajada correcta SIEMPRE debe dar acierto, aunque
//    la posicion ORIGINAL (q.correct) sea distinta
let aciertosCorrectos = 0;
for (let i = 0; i < 30; i++) {
  // Cada acierto real sube la caja Leitner del tema (ver core.js
  // _recordAttempt); a partir de QUIZ_RECALL_BOX_THRESHOLD el render pasa a
  // recuerdo libre (sin _aoQuizShuffledCorrect) -- se fija la caja en 1
  // antes de cada iteración para seguir probando el tier de reconocimiento,
  // que es lo que este bloque verifica.
  vm.runInContext(`_stats.ao[0] = {attempts: 0, fails: 0, dontKnow: 0, box: 1, due: 0}; _saveStats();`, sandbox);
  vm.runInContext(`_aoQuizAnswered = false; _aoRenderQuiz()`, sandbox);
  const picked = vm.runInContext(`_aoCurrentQuiz`, sandbox);
  if (picked.type === 'mc') {
    mathOptionButtons = Array.from({ length: picked.options.length }, () => ({ disabled: false, classList: { add() {}, remove() {} } }));
    const shuffledCorrect = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox);
    vm.runInContext(`_aoCheckQuizAnswer(${shuffledCorrect})`, sandbox);
  } else {
    vm.runInContext(`document.getElementById('aoQuizNumericInput').value = ${JSON.stringify(String(picked.correct))};`, sandbox);
    vm.runInContext(`_aoCheckQuizAnswer()`, sandbox);
  }
  const fb = vm.runInContext(`document.getElementById('aoQuizFeedback').textContent`, sandbox);
  if (fb.includes('Correcto')) aciertosCorrectos++;
}
record('Elegir la posición barajada correcta (o el valor exacto) da "Correcto" en las 30 corridas', aciertosCorrectos === 30, 'aciertos=' + aciertosCorrectos + '/30');

// 4) Elegir una posicion NO correcta (cuando la correcta no es esa) debe fallar
vm.runInContext(`_stats.ao[0] = {attempts: 0, fails: 0, dontKnow: 0, box: 1, due: 0}; _saveStats();`, sandbox); // idem: mantener tier de reconocimiento
let picked4;
do {
  vm.runInContext(`_aoQuizAnswered = false; _aoRenderQuiz()`, sandbox);
  picked4 = vm.runInContext(`_aoCurrentQuiz`, sandbox);
} while (picked4.type !== 'mc'); // este caso concreto solo tiene sentido para mc (indice incorrecto)
mathOptionButtons = Array.from({ length: picked4.options.length }, () => ({ disabled: false, classList: { add() {}, remove() {} } }));
const shuffledCorrect2 = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox);
const wrongIdx = (shuffledCorrect2 + 1) % picked4.options.length;
vm.runInContext(`_aoCheckQuizAnswer(${wrongIdx})`, sandbox);
const fbWrong = vm.runInContext(`document.getElementById('aoQuizFeedback').textContent`, sandbox);
// El feedback de fallo tiene dos formas: '❌ No es correcto — ...' (sin whyNot)
// o '❌ '+whyNot+' Puedes intentarlo de nuevo, o revisar la solución.' (con
// whyNot, ver master-ao.js _aoCheckQuizAnswer) -- ambas comparten el sufijo
// común, que es lo que de verdad identifica un fallo (whyNot es texto libre).
record('Elegir una posición incorrecta da feedback de fallo', fbWrong.includes('Puedes intentarlo de nuevo, o revisar la solución'), fbWrong);

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

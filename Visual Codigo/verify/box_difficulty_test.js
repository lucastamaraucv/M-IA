// Verifica la dificultad adaptativa por caja Leitner (QUIZ_RECALL_BOX_THRESHOLD,
// core.js): caja < umbral debe seguir mostrando opción múltiple tal cual antes;
// caja >= umbral debe mostrar el bloque de recuerdo libre (textarea + "Ver
// respuesta" + autocalificación "Acerté"/"Fallé"), y la autocalificación debe
// alimentar _recordAttempt igual que un acierto/fallo normal de opción múltiple.
// Mismo patrón de arnés headless (Node vm + DOM stub, sin navegador) que
// shuffle_test.js/confidence_dontknow_test.js.
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

const files = ['core.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js', 'calendar.js', 'report.js'];
for (const f of files) vm.runInContext(fs.readFileSync(path.join(JS_DIR, f), 'utf8'), sandbox, { filename: f });

const results = [];
function record(name, ok, detail) { results.push({ name, ok }); console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : '')); }
function setAoBox(box) {
  vm.runInContext(`_stats.ao[0] = {attempts: 0, fails: 0, dontKnow: 0, box: ${box}, due: 0}; _saveStats();`, sandbox);
}

// 1) Caja por debajo del umbral: comportamiento de reconocimiento sin cambios.
setAoBox(1);
vm.runInContext(`_aoQuizSubPos = 0; _aoQuizAnswered = false; _aoRenderQuiz()`, sandbox);
const optsHtmlLow = vm.runInContext(`document.getElementById('aoQuizOptions').innerHTML`, sandbox);
const shuffledLow = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox);
record('Caja 1: se pintan botones .math-option (reconocimiento)', optsHtmlLow.includes('math-option') && !optsHtmlLow.includes('quiz-recall-block'), optsHtmlLow.slice(0, 80));
record('Caja 1: _aoQuizShuffledCorrect queda fijado (no null)', shuffledLow !== null, 'valor=' + shuffledLow);

// 2) Caja en/sobre el umbral: bloque de recuerdo libre en vez de opciones.
setAoBox(4);
vm.runInContext(`_aoQuizAnswered = false; _aoRenderQuiz()`, sandbox);
const optsHtmlHigh = vm.runInContext(`document.getElementById('aoQuizOptions').innerHTML`, sandbox);
const shuffledHigh = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox);
const orderHigh = vm.runInContext(`_aoQuizOrder`, sandbox);
record('Caja 4: se pinta el bloque de recuerdo libre (quiz-recall-block)', optsHtmlHigh.includes('quiz-recall-block') && !optsHtmlHigh.includes('math-option'), optsHtmlHigh.slice(0, 120));
record('Caja 4: _aoQuizShuffledCorrect/_aoQuizOrder quedan null (nada que comprobar por índice)', shuffledHigh === null && orderHigh === null);

// 3) "Ver respuesta" revela la respuesta + botones de autocalificación.
vm.runInContext(`_quizRevealFreeRecall('ao')`, sandbox);
const revealedHtml = vm.runInContext(`document.getElementById('aoQuizOptions').innerHTML`, sandbox);
record('"Ver respuesta" muestra la respuesta y los botones Acerté/Fallé', revealedHtml.includes('quiz-recall-answer') && revealedHtml.includes('_quizFreeRecallResult'), revealedHtml.slice(0, 120));

// 4) Autocalificación "Acerté": mismo destino que un acierto normal (_recordAttempt, caja sube).
vm.runInContext(`_quizFreeRecallResult('ao', true)`, sandbox);
const afterOkBox = vm.runInContext(`_statsFor('ao', 0).box`, sandbox);
const fbOk = vm.runInContext(`document.getElementById('aoQuizFeedback').textContent`, sandbox);
record('"Acerté": la caja sube (era 4, min(4+1,5)=5)', afterOkBox === 5, 'box=' + afterOkBox);
record('"Acerté": feedback muestra acierto', fbOk.includes('✅'), fbOk);

// 5) Autocalificación "Fallé": vuelve a caja 1 (mismo mecanismo que fallar una mc normal).
setAoBox(4);
vm.runInContext(`_aoQuizAnswered = false; _aoRenderQuiz(); _quizRevealFreeRecall('ao')`, sandbox);
vm.runInContext(`_quizFreeRecallResult('ao', false)`, sandbox);
const afterFailBox = vm.runInContext(`_statsFor('ao', 0).box`, sandbox);
const fbFail = vm.runInContext(`document.getElementById('aoQuizFeedback').textContent`, sandbox);
record('"Fallé": la caja vuelve a 1', afterFailBox === 1, 'box=' + afterFailBox);
record('"Fallé": feedback muestra fallo', fbFail.includes('❌'), fbFail);

// 6) Doble clic no debe registrar el intento dos veces (mismo guard que _quizIsAnswered
//    usa en el resto de los flujos -- _aoQuizAnswered ya quedó en true tras el paso 5).
const attemptsBefore = vm.runInContext(`_statsFor('ao', 0).attempts`, sandbox);
vm.runInContext(`_quizFreeRecallResult('ao', true)`, sandbox); // no debería hacer nada: ya respondida
const attemptsAfter = vm.runInContext(`_statsFor('ao', 0).attempts`, sandbox);
record('Doble autocalificación no duplica el intento (guard _quizIsAnswered)', attemptsBefore === attemptsAfter, 'antes=' + attemptsBefore + ' despues=' + attemptsAfter);

// 7) Prefix 'review' usa sus propios ids (reviewOptions, sin sufijo "Quiz") y
//    también respeta el umbral -- se invoca _quizRenderAnswerArea directamente
//    (sin pasar por el selector de pool aleatorio de _reviewPickNext, que no es
//    parte de este cambio) para una pregunta sintética con mode/idx de un tema
//    en caja alta.
setAoBox(5);
const reviewQ = vm.runInContext(`({type:'mc', options:['a','b','c','d'], correct:1})`, sandbox);
sandbox.__reviewQ = reviewQ;
const reviewRes = vm.runInContext(`_quizRenderAnswerArea('review', 'ao', 0, __reviewQ)`, sandbox);
const reviewOptsHtml = vm.runInContext(`document.getElementById('reviewOptions').innerHTML`, sandbox);
record('prefix "review" con caja alta también pinta recuerdo libre (ids reviewOptions)', reviewOptsHtml.includes('quiz-recall-block') && reviewRes.shuffled === null, reviewOptsHtml.slice(0, 100));

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

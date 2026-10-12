// Verifica la entrada inductiva (bloqueo de teoría hasta el primer intento,
// ver _theoryIsLocked/_theoryGateHtml en core.js): un tema NUNCA intentado
// (_statsFor(mode,idx).attempts===0) debe mostrar la caja de bloqueo en vez
// del texto real de `theory`; tras responder el quiz una vez (acierte o
// falle) la teoría debe desbloquearse sola; un tema con attempts>0 desde el
// arranque debe mostrar la teoría directo, sin bloqueo; y el link manual de
// desbloqueo debe funcionar sin necesidad de responder. Mismo patrón de
// arnés headless (Node vm + DOM stub, sin navegador) que box_difficulty_test.js.
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

const files = ['core.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'master-ns.js', 'master-rn.js', 'master-rf.js', 'review.js', 'calendar.js', 'report.js'];
for (const f of files) vm.runInContext(fs.readFileSync(path.join(JS_DIR, f), 'utf8'), sandbox, { filename: f });

const results = [];
function record(name, ok, detail) { results.push({ name, ok }); console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : '')); }
function setStats(mode, idx, stats) {
  vm.runInContext(`_stats.${mode}[${idx}] = ${JSON.stringify(stats)}; _saveStats();`, sandbox);
}

// 0) Sanity: el tema de prueba realmente trae `theory` (si no, el gate nunca
//    se pinta y el resto de la corrida sería un falso positivo).
const hasTheory = vm.runInContext(`!!(EX_AO[0].theory && EX_AO[0].theory.trim())`, sandbox);
record('Sanity: EX_AO[0] trae `theory` no vacío', hasTheory);

// 1) Tema nunca intentado (sin entrada en _stats.ao[0]) -> teoría bloqueada.
vm.runInContext(`delete _stats.ao[0]; _saveStats();`, sandbox);
vm.runInContext(`_aoPos = 0; _aoRenderTheory();`, sandbox);
let theoryHtml = vm.runInContext(`document.getElementById('aoTheoryBody').innerHTML`, sandbox);
record('Tema nunca intentado: se pinta la caja de bloqueo (theory-locked-box)',
  theoryHtml.includes('theory-locked-box') && theoryHtml.includes('Antes de la teoría'),
  theoryHtml.slice(0, 100));
const realTheorySnippet = vm.runInContext(`EX_AO[0].theory.slice(0, 30)`, sandbox);
record('Tema nunca intentado: NO se pinta el texto real de la teoría',
  !theoryHtml.includes(realTheorySnippet));

// 2) Tras responder el quiz una vez (aunque falle) -> se desbloquea sola.
vm.runInContext(`_aoQuizSubPos = 0; _aoQuizAnswered = false; _aoRenderQuiz();`, sandbox);
// Fuerza una respuesta INCORRECTA (índice fuera de rango nunca coincide con el correcto barajado).
vm.runInContext(`_aoCheckQuizAnswer(-1);`, sandbox);
const attemptsAfterFail = vm.runInContext(`_statsFor('ao', 0).attempts`, sandbox);
record('Tras responder (aunque falle): attempts pasa a ser >=1', attemptsAfterFail >= 1, 'attempts=' + attemptsAfterFail);
theoryHtml = vm.runInContext(`document.getElementById('aoTheoryBody').innerHTML`, sandbox);
record('Tras responder: la teoría se desbloquea sola (ya no hay caja de bloqueo)',
  !theoryHtml.includes('theory-locked-box') && theoryHtml.includes(realTheorySnippet),
  theoryHtml.slice(0, 100));

// 3) Revisita: mismo tema con attempts>0 desde el arranque -> teoría directo, sin bloqueo.
setStats('ao', 1, { attempts: 3, fails: 1, dontKnow: 0, box: 2, due: 0 });
vm.runInContext(`_aoPos = 1; _aoRenderTheory();`, sandbox);
const theoryHtml2 = vm.runInContext(`document.getElementById('aoTheoryBody').innerHTML`, sandbox);
const hasTheory2 = vm.runInContext(`!!(EX_AO[1].theory && EX_AO[1].theory.trim())`, sandbox);
record('Tema ya intentado antes (attempts>0 desde el arranque): teoría directa, sin bloqueo',
  !hasTheory2 || !theoryHtml2.includes('theory-locked-box'),
  'hasTheory2=' + hasTheory2 + ' html=' + theoryHtml2.slice(0, 80));

// 4) Link manual de desbloqueo ("ya sé, mostrame la teoría igual") sin responder el quiz.
vm.runInContext(`delete _stats.ao[2]; _saveStats(); _aoPos = 2; _aoRenderTheory();`, sandbox);
let theoryHtml3 = vm.runInContext(`document.getElementById('aoTheoryBody').innerHTML`, sandbox);
const hadGate3 = theoryHtml3.includes('theory-locked-box');
vm.runInContext(`_theoryUnlockNow('ao', 2, '_aoRenderTheory');`, sandbox);
theoryHtml3 = vm.runInContext(`document.getElementById('aoTheoryBody').innerHTML`, sandbox);
const attemptsStill0 = vm.runInContext(`_statsFor('ao', 2).attempts`, sandbox);
record('Desbloqueo manual: sin responder, revela la teoría igual (respeta autonomía)',
  hadGate3 && !theoryHtml3.includes('theory-locked-box') && attemptsStill0 === 0,
  'hadGate3=' + hadGate3 + ' attemptsStill0=' + attemptsStill0);

// 5) Mismo mecanismo replicado en otra materia (RA) -- confirma que el gate
//    compartido (_theoryIsLocked/_theoryGateHtml en core.js) funciona igual
//    con un prefix/mode distinto, no solo hardcodeado para AO.
vm.runInContext(`delete _stats.ra[0]; _saveStats(); _raPos = 0; _raRenderTheory();`, sandbox);
const raTheoryHtml = vm.runInContext(`document.getElementById('raTheoryBody').innerHTML`, sandbox);
record('Mismo mecanismo en RA: tema nunca intentado también se bloquea',
  raTheoryHtml.includes('theory-locked-box'), raTheoryHtml.slice(0, 80));
vm.runInContext(`_raQuizSubPos = 0; _raQuizAnswered = false; _raRenderQuiz(); _raCheckQuizAnswer(-1);`, sandbox);
const raTheoryHtmlAfter = vm.runInContext(`document.getElementById('raTheoryBody').innerHTML`, sandbox);
record('Mismo mecanismo en RA: se desbloquea tras responder', !raTheoryHtmlAfter.includes('theory-locked-box'), raTheoryHtmlAfter.slice(0, 80));

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

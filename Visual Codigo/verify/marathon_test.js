// Verifica el Maratón de examen (static/js/marathon.js): construcción de la
// cola (nunca-visto -> vencido -> resto, bloque por materia sin intercalar),
// presupuesto dinámico recalculado por ítem (con piso MARATHON_MIN_ITEM_SECONDS),
// timeout real dispara _quizDontKnowClick + arranca la gracia de lectura, y
// guardado/carga en localStorage retoma en el mismo queuePos. Mismo patrón de
// arnés headless (Node vm + DOM stub, sin navegador) que theory_gate_test.js.
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

const files = ['core.js', 'viz-render.js', 'code-annotate.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'master-ns.js', 'master-rn.js', 'master-rf.js', 'review.js', 'calendar.js', 'report.js', 'errors.js', 'exam.js', 'session.js', 'marathon.js'];
for (const f of files) vm.runInContext(fs.readFileSync(path.join(JS_DIR, f), 'utf8'), sandbox, { filename: f });

const results = [];
function record(name, ok, detail) { results.push({ name, ok }); console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : '')); }

// ── 1) Cola: nunca-visto -> vencido -> resto, dentro de UNA materia ──
vm.runInContext(`_stats.ao = {}; _stats.ao[1] = {attempts:1, fails:0, dontKnow:0, box:2, due: Date.now()-1000}; _stats.ao[2] = {attempts:1, fails:0, dontKnow:0, box:2, due: Date.now()+999999999}; _saveStats();`, sandbox);
const aoQueue = vm.runInContext(`_marathonBuildQueue(['ao']).map(it=>it.idx)`, sandbox);
const pos0 = aoQueue.indexOf(0), pos1 = aoQueue.indexOf(1), pos2 = aoQueue.indexOf(2);
record('Cola: tema nunca-visto (0) antes que tema vencido (1)', pos0 >= 0 && pos1 >= 0 && pos0 < pos1, 'pos0=' + pos0 + ' pos1=' + pos1);
record('Cola: tema vencido (1) antes que tema no-vencido (2)', pos1 >= 0 && pos2 >= 0 && pos1 < pos2, 'pos1=' + pos1 + ' pos2=' + pos2);
const aoLen = vm.runInContext(`EX_AO.length`, sandbox);
record('Cola: incluye TODOS los temas de la materia (ninguno se pierde)', aoQueue.length === aoLen, 'len=' + aoQueue.length + ' esperado=' + aoLen);

// ── 2) Cola multi-materia: bloque por materia, sin intercalar ──
vm.runInContext(`_stats.ra = {};`, sandbox);
const multiQueue = vm.runInContext(`_marathonBuildQueue(['ao','ra'])`, sandbox);
const lastAoPos = multiQueue.map(it => it.mode).lastIndexOf('ao');
const firstRaPos = multiQueue.map(it => it.mode).indexOf('ra');
record('Cola multi-materia: TODO ao antes que el primer ra (bloque, no intercalado)', lastAoPos >= 0 && firstRaPos >= 0 && lastAoPos < firstRaPos, 'lastAo=' + lastAoPos + ' firstRa=' + firstRaPos);

// ── 3) Presupuesto dinámico: recalculado por ítem, con piso ──
vm.runInContext(`_marathonQueue = [0,1,2,3,4].map(i=>({mode:'ao', idx:i})); _marathonCourses=['ao'];`, sandbox);
vm.runInContext(`_marathonTotalSeconds = 600; _marathonAccumulatedMs = 0; _marathonQueuePos = 0;`, sandbox);
vm.runInContext(`_marathonStartItemTimer(); _marathonStopItemTimer();`, sandbox); // arranca el cálculo, para el timer real antes de que pueda tickear
let secs = vm.runInContext(`_marathonItemSecondsLeft`, sandbox);
record('Presupuesto: 600s/5 items sin uso previo = 120s', secs === 120, 'secs=' + secs);

vm.runInContext(`_marathonAccumulatedMs = 300000; _marathonQueuePos = 3;`, sandbox); // 300s usados, quedan 2 items (pos 3,4)
vm.runInContext(`_marathonStartItemTimer(); _marathonStopItemTimer();`, sandbox);
secs = vm.runInContext(`_marathonItemSecondsLeft`, sandbox);
record('Presupuesto: se recalcula tras avanzar (300s usados, 2 items = 150s)', secs === 150, 'secs=' + secs);

vm.runInContext(`_marathonAccumulatedMs = 590000; _marathonQueuePos = 4;`, sandbox); // casi agotado, 1 item queda
vm.runInContext(`_marathonStartItemTimer(); _marathonStopItemTimer();`, sandbox);
secs = vm.runInContext(`_marathonItemSecondsLeft`, sandbox);
record('Presupuesto: nunca baja del piso MARATHON_MIN_ITEM_SECONDS', secs === 25, 'secs=' + secs);

// ── 4) Timeout real dispara _quizDontKnowClick (auto "no sé") + arranca la gracia ──
vm.runInContext(`_marathonQueue = [{mode:'ao', idx:5}]; _marathonQueuePos = 0; _marathonCourses=['ao']; _marathonTimeoutCount = 0;`, sandbox);
vm.runInContext(`_marathonOpenCourse('ao'); _focusGoTo('ao', 5);`, sandbox);
const answeredBefore = vm.runInContext(`_quizIsAnswered('ao')`, sandbox);
vm.runInContext(`_marathonTimeoutAdvance();`, sandbox);
const answeredAfter = vm.runInContext(`_quizIsAnswered('ao')`, sandbox);
const timeoutCount = vm.runInContext(`_marathonTimeoutCount`, sandbox);
const itemState = vm.runInContext(`_marathonItemState`, sandbox);
const graceLeft = vm.runInContext(`_marathonGraceSecondsLeft`, sandbox);
record('Timeout: NO estaba respondida antes (sanity)', answeredBefore === false);
record('Timeout: dispara _quizDontKnowClick (queda "respondida" vía no-sé)', answeredAfter === true);
record('Timeout: cuenta el tema como avanzado-por-tiempo', timeoutCount === 1, 'timeoutCount=' + timeoutCount);
record('Timeout: entra en estado de gracia de lectura', itemState === 'grace' && graceLeft === 15, 'state=' + itemState + ' grace=' + graceLeft);
vm.runInContext(`if(_marathonGraceHandle){ clearInterval(_marathonGraceHandle); _marathonGraceHandle=null; }`, sandbox); // no dejar el interval de gracia corriendo

// ── 5) Guardar + recargar retoma en el mismo queuePos, sin volver a pedir materias/horas ──
vm.runInContext(`_marathonCourses=['ao']; _marathonTotalSeconds=3600; _marathonQueue=[0,1,2,3].map(i=>({mode:'ao',idx:i})); _marathonQueuePos=2; _marathonAccumulatedMs=12345; _marathonTimeoutCount=1; _marathonSave();`, sandbox);
const loaded = vm.runInContext(`_marathonLoad()`, sandbox);
record('Guardado/carga: queuePos se preserva', loaded && loaded.queuePos === 2, JSON.stringify(loaded && { queuePos: loaded.queuePos, courses: loaded.courses }));
record('Guardado/carga: accumulatedMs se preserva', loaded && loaded.accumulatedMs === 12345);
vm.runInContext(`_marathonRenderPanel();`, sandbox);
const panelHtml = vm.runInContext(`document.getElementById('marathonBody').innerHTML`, sandbox);
record('Reabrir con maratón sin terminar: muestra vista de progreso, NO la de configuración', panelHtml.includes('Continuar donde quedé') && !panelHtml.includes('Empezar el maratón'), panelHtml.slice(0, 100));

// ── 6) accumulatedMs no crece mientras no hay un tramo activo (panel cerrado / pausado) ──
vm.runInContext(`_marathonResumedAt = 0; _marathonAccumulatedMs = 5000;`, sandbox);
vm.runInContext(`_marathonFlushElapsed();`, sandbox);
const accAfterFlushInactive = vm.runInContext(`_marathonAccumulatedMs`, sandbox);
record('accumulatedMs no crece si no hay tramo activo (_marathonResumedAt=0)', accAfterFlushInactive === 5000, 'acc=' + accAfterFlushInactive);

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

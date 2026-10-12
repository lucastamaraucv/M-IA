// Arnés headless para calendar.js: no necesita un Flask real porque el
// calendario no llama a /prepare directamente (solo delega en
// toggleMasterAo/Ra/As/toggleReviewMode, ya verificados en sus propios
// smoke tests). Aquí se comprueba: cobertura exacta de índices reales,
// lectura de progreso desde localStorage, y que el panel/banner renderizan
// sin lanzar excepciones.
// Uso: node verify/calendar_smoke_test.js

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
const document = {
  getElementById(id) { if (!elCache.has(id)) elCache.set(id, fakeElement(id)); return elCache.get(id); },
  addEventListener() {}, createElement() { return fakeElement('__anon__'); },
  querySelector() { return fakeElement('__anon__'); }, querySelectorAll() { return []; },
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

const files = ['core.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js', 'calendar.js'];
for (const f of files) {
  const src = fs.readFileSync(path.join(JS_DIR, f), 'utf8');
  vm.runInContext(src, sandbox, { filename: f });
}

const results = [];
function record(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : ''));
}

// 1) cobertura exacta de índices reales (mismo cálculo ya hecho con node -e,
//    repetido aquí dentro del arnés para que quede documentado)
const totals = { ao: vm.runInContext('EX_AO.length', sandbox), ra: vm.runInContext('EX_RA.length', sandbox), as: vm.runInContext('EX_AS.length', sandbox) };
const plan = vm.runInContext('CAL_PLAN', sandbox);
// 24 = 21 dias originales (AO/RA/AS) + 3 dias del piloto NS/RN/RF (2026-08-18)
record('CAL_PLAN tiene 24 días', plan.length === 24, `len=${plan.length}`);
for (const ph of ['ao', 'ra', 'as']) {
  const entries = plan.filter(e => e.phase === ph);
  const covered = new Set();
  entries.forEach(e => { for (let i = e.range[0]; i <= e.range[1]; i++) covered.add(i); });
  const missing = []; for (let i = 0; i < totals[ph]; i++) if (!covered.has(i)) missing.push(i);
  record(`${ph}: CAL_PLAN cubre los ${totals[ph]} temas reales de EX_${ph.toUpperCase()} sin huecos`, missing.length === 0, `missing=${JSON.stringify(missing)}`);
}

// 2) lectura de progreso real desde localStorage
// Clave real V2 (temario aplanado 41->164, ver master-ao.js MASTER_AO_KEY y
// calendar.js CAL_PHASE_KEY) -- CAL_PLAN[0].range es [0,35] (36 temas
// aplanados), no [0,8].
lsStore['pyvizMasterAoProgressV2'] = JSON.stringify({ done: Array.from({length:36}, (_,i)=>i) });
let d = vm.runInContext(`_calRangeDone(CAL_PLAN[0])`, sandbox);
record('_calRangeDone: día 1 de AO (rango 0-35) completo => 36/36', d.done === 36 && d.total === 36, JSON.stringify(d));

lsStore['pyvizMasterAoProgressV2'] = JSON.stringify({ done: [0,2,4] });
d = vm.runInContext(`_calRangeDone(CAL_PLAN[0])`, sandbox);
record('_calRangeDone: progreso parcial => 3/36', d.done === 3 && d.total === 36, JSON.stringify(d));

// 3) repaso manual (días sin rango)
const repasoEntry = plan.find(e => e.phase === 'rp');
const key = vm.runInContext(`_calDateKey(CAL_PLAN.find(e=>e.phase==='rp'))`, sandbox);
let before = vm.runInContext(`_calRepasoDone(${JSON.stringify(key)})`, sandbox);
vm.runInContext(`_calToggleRepaso(${JSON.stringify(key)})`, sandbox);
let after = vm.runInContext(`_calRepasoDone(${JSON.stringify(key)})`, sandbox);
record('_calToggleRepaso: marca un día de repaso como hecho', before === false && after === true, `before=${before} after=${after}`);

// 3b) deuda de repaso (_reviewDueCount, de review.js): el banner debe
//     seguir mostrándose por la deuda aunque el contenido de hoy ya esté
//     hecho o el banner de hoy esté descartado.
lsStore['pyvizMasterStats'] = JSON.stringify({ ao: { 0: { attempts: 1, fails: 0, box: 1, due: 1 } }, ra: {}, as: {}, py: {}, math: {}, aoclassify: {} });
lsStore['pyvizMasterAoProgressV2'] = JSON.stringify({ done: [0] });
vm.runInContext(`_loadAoProgress()`, sandbox); // _reviewBuildPool lee el Set en memoria _aoDone, no localStorage directo
const dueCount = vm.runInContext(`_reviewDueCount()`, sandbox);
record('_reviewDueCount() detecta un tema vencido (due=1, ya pasado)', dueCount >= 1, `dueCount=${dueCount}`);
try {
  vm.runInContext(`_calRenderBanner()`, sandbox);
  const bannerHtml = vm.runInContext(`document.getElementById('planTodayBanner').innerHTML`, sandbox);
  const bannerDisplay = vm.runInContext(`document.getElementById('planTodayBanner').style.display`, sandbox);
  record('El banner se muestra y menciona la deuda de repaso cuando hay algo vencido', bannerDisplay !== 'none' && /repaso/i.test(bannerHtml), `display=${bannerDisplay} html="${bannerHtml.slice(0,120)}..."`);
} catch (e) { record('_calRenderBanner() con deuda de repaso no lanza excepción', false, String(e)); }

// 3c) el punto clave del diseño: la deuda de repaso NO debe desaparecer
//     solo porque el contenido de hoy ya esté descartado (✕) o completo —
//     simulamos "hoy" totalmente hecho Y descartado, la deuda debe seguir.
try {
  const todayEntry = vm.runInContext(`_calTodayEntry()`, sandbox);
  if (todayEntry) {
    vm.runInContext(`_calDismissToday()`, sandbox);
    const htmlAfterDismiss = vm.runInContext(`document.getElementById('planTodayBanner').innerHTML`, sandbox);
    const displayAfterDismiss = vm.runInContext(`document.getElementById('planTodayBanner').style.display`, sandbox);
    record('Tras descartar "hoy", el banner sigue visible por la deuda de repaso', displayAfterDismiss !== 'none' && /repaso/i.test(htmlAfterDismiss) && !/Hoy toca/.test(htmlAfterDismiss), `display=${displayAfterDismiss} html="${htmlAfterDismiss.slice(0,150)}..."`);
  } else {
    record('Tras descartar "hoy", el banner sigue visible por la deuda de repaso', true, 'sin entrada de plan para la fecha real del sistema, se omite');
  }
} catch (e) { record('Descartar "hoy" no oculta la deuda de repaso', false, String(e)); }

// 4) las funciones a las que el banner/detalle delegan existen de verdad
for (const [ph, fnName] of Object.entries({ ao: 'toggleMasterAo', ra: 'toggleMasterRa', as: 'toggleMasterAs', rp: 'toggleReviewMode' })) {
  const t = vm.runInContext(`typeof ${fnName}`, sandbox);
  record(`CAL_PHASE_MODE.${ph} (${fnName}) existe como función`, t === 'function', `typeof=${t}`);
}

// 5) el banner y el panel completo renderizan sin lanzar excepción, sea
//    cual sea la fecha real del sistema al ejecutar este test
try {
  vm.runInContext(`_calRenderBanner()`, sandbox);
  record('_calRenderBanner() no lanza excepción', true);
} catch (e) { record('_calRenderBanner() no lanza excepción', false, String(e)); }

try {
  vm.runInContext(`toggleCalendar()`, sandbox);
  const on = vm.runInContext(`_calOn`, sandbox);
  vm.runInContext(`_calSelectDay(CAL_PLAN[0].d)`, sandbox);
  const detailHtml = vm.runInContext(`document.getElementById('calDetail').innerHTML`, sandbox);
  vm.runInContext(`toggleCalendar()`, sandbox); // cierra
  const offAfter = vm.runInContext(`_calOn`, sandbox);
  record('toggleCalendar() abre y _calSelectDay() rellena el detalle', on === true && detailHtml.length > 0, `on=${on} detailLen=${detailHtml.length}`);
  record('toggleCalendar() otra vez cierra (_calOn=false)', offAfter === false);
} catch (e) { record('toggleCalendar()/_calSelectDay() no lanzan excepción', false, String(e)); }

const failed = results.filter(r => !r.ok);
console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
process.exit(failed.length ? 1 : 0);

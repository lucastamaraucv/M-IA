// Arnés headless para el Modo Maestro AO: mismo patrón que as_smoke_test.js,
// pero recorriendo los 41 temas de EX_AO (18 originales + 23 de los batches
// 3-5 insertados 2026-08-09) contra un Flask real.
// Uso: BASE_URL=http://127.0.0.1:5098 node verify/ao_smoke_test.js

const fs = require('fs');
const vm = require('vm');
const path = require('path');

process.on('unhandledRejection', e => { console.error('[unhandledRejection]', e); process.exitCode = 1; });
process.on('uncaughtException', e => { console.error('[uncaughtException]', e); process.exitCode = 1; });

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:5098';
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
  fetch: (url, opts) => {
    const full = /^https?:\/\//.test(url) ? url : BASE_URL + url;
    return fetch(full, opts);
  },
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);

const files = ['core.js', 'viz-render.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js'];
for (const f of files) {
  const src = fs.readFileSync(path.join(JS_DIR, f), 'utf8');
  vm.runInContext(src, sandbox, { filename: f });
}

const results = [];
function record(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : ''));
}

function waitFor(fn, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  return new Promise((resolve, reject) => {
    (function poll() {
      if (fn()) return resolve();
      if (Date.now() > deadline) return reject(new Error('timeout'));
      setTimeout(poll, 30);
    })();
  });
}

async function runCodeAndWait() {
  vm.runInContext(`runCode()`, sandbox);
  await waitFor(() => vm.runInContext(`steps && steps.length > 0`, sandbox), 8000);
}

async function main() {
  const nTopics = vm.runInContext(`EX_AO.length`, sandbox);
  const nQuiz = vm.runInContext(`AO_QUIZ.length`, sandbox);
  record('EX_AO y AO_QUIZ tienen la misma longitud', nTopics === nQuiz, `EX_AO=${nTopics} AO_QUIZ=${nQuiz}`);

  vm.runInContext(`toggleMasterAo()`, sandbox);
  const onAfterToggle = vm.runInContext(`_aoOn`, sandbox);
  record('toggleMasterAo() activa _aoOn', onAfterToggle === true);

  for (let i = 0; i < nTopics; i++) {
    vm.runInContext(`_aoGoTo(${i})`, sandbox);
    try {
      await runCodeAndWait();
    } catch (e) {
      record(`Tema ${i}: runCode() completa (via /prepare real)`, false, String(e));
      continue;
    }
    const lastErr = vm.runInContext(`_lastRunError`, sandbox);
    const nSteps = vm.runInContext(`steps.length`, sandbox);
    record(`Tema ${i}: código ejecuta sin error de Python`, !lastErr, lastErr ? JSON.stringify(lastErr) : `steps=${nSteps}`);

    const q = vm.runInContext(`_aoCurrentQuiz`, sandbox); // pregunta YA elegida por _aoRenderQuiz (banco de varias por tema)
    if (q.type === 'mc') {
      // Desde el arreglo del sesgo "correcta siempre en a)", las opciones se
      // barajan en cada render -- hay que comprobar contra la posicion YA
      // barajada (_aoQuizShuffledCorrect), no q.correct (la original).
      const shuffledCorrect = vm.runInContext(`_aoQuizShuffledCorrect`, sandbox);
      vm.runInContext(`_aoCheckQuizAnswer(${shuffledCorrect})`, sandbox);
    } else {
      vm.runInContext(`document.getElementById('aoQuizNumericInput').value = ${JSON.stringify(String(q.correct))};`, sandbox);
      vm.runInContext(`_aoCheckQuizAnswer()`, sandbox);
    }
    const answered = vm.runInContext(`_aoQuizAnswered`, sandbox);
    const fbText = vm.runInContext(`document.getElementById('aoQuizFeedback').textContent`, sandbox);
    record(`Tema ${i}: quiz acepta la respuesta correcta real`, answered === true && fbText.includes('Correcto'),
      `type=${q.type} correct=${q.correct} fb="${fbText}"`);

    vm.runInContext(`aoNext()`, sandbox);
  }

  const doneCount = vm.runInContext(`_aoDone.size`, sandbox);
  record(`Tras recorrer los ${nTopics} temas, _aoDone tiene ${nTopics} entradas`, doneCount === nTopics, `_aoDone.size=${doneCount}`);

  vm.runInContext(`exitMasterAo()`, sandbox);
  record('exitMasterAo() desactiva _aoOn', vm.runInContext(`_aoOn`, sandbox) === false);

  const failed = results.filter(r => !r.ok);
  console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
  process.exit(failed.length ? 1 : 0);
}

main().catch(e => { console.error('ERROR en el arnés:', e); process.exit(1); });
